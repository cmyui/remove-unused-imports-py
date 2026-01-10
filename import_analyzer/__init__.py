from __future__ import annotations

from import_analyzer._autofix import import_analyzer
from import_analyzer._cross_file import CrossFileResult
from import_analyzer._cross_file import analyze_cross_file
from import_analyzer._data import ImplicitReexport
from import_analyzer._data import ImportEdge
from import_analyzer._data import ImportInfo
from import_analyzer._data import ModuleInfo
from import_analyzer._detection import find_unused_imports
from import_analyzer._graph import ImportGraph
from import_analyzer._graph import build_import_graph
from import_analyzer._graph import build_import_graph_from_directory
from import_analyzer._main import check_cross_file
from import_analyzer._main import check_file
from import_analyzer._main import collect_python_files
from import_analyzer._main import main
from import_analyzer._resolution import ModuleResolver

__all__ = [
    # Data types
    "ImportInfo",
    "ModuleInfo",
    "ImportEdge",
    "ImplicitReexport",
    "CrossFileResult",
    # Single-file analysis
    "find_unused_imports",
    "import_analyzer",
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
]
