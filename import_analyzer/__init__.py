from __future__ import annotations

from importlib.metadata import version

from import_analyzer._autofix import remove_unused_imports
from import_analyzer._detection import find_unused_imports
from import_analyzer._main import check_file
from import_analyzer._main import collect_python_files

__version__ = version("import-analyzer-py")

__all__ = [
    # Data types
    "ImportInfo",
    "ModuleInfo",
    "ImportEdge",
    "ImplicitReexport",
    "CrossFileResult",
    # Single-file analysis
    "find_unused_imports",
    "remove_unused_imports",
    "check_file",
    # Cross-file analysis
    "ModuleResolver",
    "ImportGraph",
    "build_import_graph",
    "build_import_graph_from_directory",
    "analyze_cross_file",
    "check_cross_file",
    # CLI
    "collect_python_files",
    "main",
    # Metadata
    "__version__",
]
