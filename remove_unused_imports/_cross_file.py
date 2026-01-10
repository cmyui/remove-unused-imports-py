"""Cross-file import analysis."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path

from remove_unused_imports._data import ImplicitReexport
from remove_unused_imports._data import ImportInfo
from remove_unused_imports._detection import find_unused_imports
from remove_unused_imports._graph import ImportGraph


@dataclass
class CrossFileResult:
    """Results of cross-file import analysis."""

    # Unused imports per file (after accounting for re-exports)
    unused_imports: dict[Path, list[ImportInfo]] = field(default_factory=dict)

    # Imports used by other files but not in __all__
    implicit_reexports: list[ImplicitReexport] = field(default_factory=list)

    # External module usage across the project: module -> files using it
    external_usage: dict[str, set[Path]] = field(default_factory=dict)

    # Circular import chains
    circular_imports: list[list[Path]] = field(default_factory=list)


class CrossFileAnalyzer:
    """Analyze imports across multiple files."""

    def __init__(self, graph: ImportGraph) -> None:
        self.graph = graph

    def analyze(self) -> CrossFileResult:
        """Run cross-file analysis.

        Steps:
        1. Run single-file analysis on each module
        2. Compute full cascade of unused imports (iterate until stable)
        3. Find implicit re-exports (re-exported but not in __all__)
        4. Aggregate external module usage
        5. Find circular imports

        The cascade computation handles chains like:
        - A imports X from B (unused in A)
        - B imports X from C (only re-exported to A)
        - When A's import is removed, B's import becomes unused too
        """
        result = CrossFileResult()

        # Step 1: Get single-file unused imports for each module
        single_file_unused = self._get_single_file_unused()

        # Step 2: Compute full cascade of unused imports
        all_removed: dict[Path, set[str]] = defaultdict(set)

        changed = True
        while changed:
            changed = False

            # Find re-exports considering current "virtually removed" set
            reexported = self._find_reexported_imports(removed_imports=all_removed)

            # Anything unused locally AND not re-exported → mark for removal
            for file_path, unused in single_file_unused.items():
                reexported_names = reexported.get(file_path, set())
                for imp in unused:
                    if imp.name not in reexported_names:
                        if imp.name not in all_removed[file_path]:
                            all_removed[file_path].add(imp.name)
                            changed = True

        # Build unused_imports from the stable removed set
        for file_path, removed_names in all_removed.items():
            unused_imports = [
                imp for imp in single_file_unused.get(file_path, [])
                if imp.name in removed_names
            ]
            if unused_imports:
                result.unused_imports[file_path] = unused_imports

        # Step 3: Find implicit re-exports (using final reexported state)
        # Re-compute with final removed set to get accurate re-export info
        final_reexported = self._find_reexported_imports(removed_imports=all_removed)
        result.implicit_reexports = self._find_implicit_reexports(final_reexported)

        # Step 4: Aggregate external usage
        result.external_usage = self._aggregate_external_usage()

        # Step 5: Find circular imports
        result.circular_imports = self.graph.find_cycles()

        return result

    def _get_single_file_unused(self) -> dict[Path, list[ImportInfo]]:
        """Run single-file unused detection on each module."""
        result: dict[Path, list[ImportInfo]] = {}

        for file_path, module_info in self.graph.nodes.items():
            try:
                source = file_path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue

            unused = find_unused_imports(source)
            if unused:
                result[file_path] = unused

        return result

    def _find_reexported_imports(
        self,
        removed_imports: dict[Path, set[str]] | None = None,
    ) -> dict[Path, set[str]]:
        """Find imports that are re-exported to other files.

        Args:
            removed_imports: Imports to consider as "virtually removed".
                When checking if file B's import is re-exported via file A,
                skip if A's import of that name is in this set.

        Returns a mapping of file -> set of import names that are used
        by other files importing from this file.
        """
        removed = removed_imports or {}
        reexported: dict[Path, set[str]] = defaultdict(set)

        for edge in self.graph.edges:
            if edge.is_external or edge.imported is None:
                continue

            # edge.imported is being imported by edge.importer
            # edge.names are the names being imported
            imported_file = edge.imported
            imported_names = edge.names

            # Filter out names that are "virtually removed" from the importer
            importer_removed = removed.get(edge.importer, set())
            active_names = imported_names - importer_removed

            if not active_names:
                continue

            if imported_file not in self.graph.nodes:
                continue

            module_info = self.graph.nodes[imported_file]

            # Check which imported names are actually import statements
            # in the imported file (not defined there)
            import_names_in_file = {imp.name for imp in module_info.imports}
            defined_in_file = module_info.defined_names

            for name in active_names:
                # If the name is an import in the target file (not defined),
                # then it's being re-exported
                if name in import_names_in_file and name not in defined_in_file:
                    reexported[imported_file].add(name)

        return dict(reexported)

    def _find_implicit_reexports(
        self, reexported: dict[Path, set[str]],
    ) -> list[ImplicitReexport]:
        """Find imports that are re-exported but not in __all__."""
        result: list[ImplicitReexport] = []

        for file_path, reexported_names in reexported.items():
            if file_path not in self.graph.nodes:
                continue

            module_info = self.graph.nodes[file_path]
            exports = module_info.exports  # Names in __all__

            for name in reexported_names:
                # If re-exported but not in __all__, it's implicit
                if name not in exports:
                    # Find which files use this re-exported name
                    used_by: set[Path] = set()
                    for edge in self.graph.get_importers(file_path):
                        if name in edge.names:
                            used_by.add(edge.importer)

                    result.append(
                        ImplicitReexport(
                            source_file=file_path,
                            import_name=name,
                            used_by=used_by,
                        ),
                    )

        return result

    def _aggregate_external_usage(self) -> dict[str, set[Path]]:
        """Aggregate which files use which external modules."""
        usage: dict[str, set[Path]] = defaultdict(set)

        for edge in self.graph.edges:
            if edge.is_external:
                usage[edge.module_name].add(edge.importer)

        return dict(usage)


def analyze_cross_file(graph: ImportGraph) -> CrossFileResult:
    """Convenience function for cross-file analysis."""
    analyzer = CrossFileAnalyzer(graph)
    return analyzer.analyze()
