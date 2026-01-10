# remove-unused-imports

[![build status](https://github.com/cmyui/remove-unused-imports-py/actions/workflows/ci.yml/badge.svg)](https://github.com/cmyui/remove-unused-imports-py/actions/workflows/ci.yml)

A Python linter that detects and automatically removes unused imports.

## Installation

```bash
pip install remove-unused-imports
```

Or install from source:

```bash
git clone https://github.com/cmyui/remove-unused-imports-py
cd remove-unused-imports-py
pip install .
```

## Usage

### Cross-file mode (default)

Cross-file mode follows imports from an entry point and tracks re-exports across your codebase. This prevents false positives when imports are used by other files.

```bash
# Analyze from entry point (follows imports)
remove-unused-imports main.py

# Analyze entire directory
remove-unused-imports src/

# Fix all unused imports (including cascaded ones)
remove-unused-imports --fix main.py

# Warn about implicit re-exports (imports used by other files but not in __all__)
remove-unused-imports --warn-implicit-reexports main.py

# Warn about circular imports
remove-unused-imports --warn-circular main.py

# Warn about files that become unreachable after fixing
remove-unused-imports --warn-unreachable main.py

# Quiet mode (summary only)
remove-unused-imports -q main.py
```

### Single-file mode

For simple use cases or when you want to analyze files independently:

```bash
# Check files independently (no cross-file tracking)
remove-unused-imports --single-file myfile.py

# Check multiple files
remove-unused-imports --single-file src/*.py
```

### Exit codes

| Code | Meaning                                       |
| ---- | --------------------------------------------- |
| 0    | No unused imports found (or `--fix` was used) |
| 1    | Unused imports found                          |

## Features

### Cross-file analysis

- **Re-export tracking**: Imports used by other files are preserved
- **Cascade detection**: Finds all unused imports in a single pass, even when removing one exposes another
- **Circular import detection**: Warns about import cycles
- **Implicit re-export warnings**: Identifies re-exports missing from `__all__`
- **Unreachable file detection**: Warns about files that become dead code after fixing imports

### Single-file analysis

- Detects unused `import X` and `from X import Y` statements
- Handles aliased imports (`import X as Y`, `from X import Y as Z`)
- Recognizes usage in:
  - Function calls and attribute access
  - Type annotations (including forward references / string annotations)
  - Decorators and base classes
  - Default argument values
  - `__all__` exports
- Skips `__future__` imports (they have side effects)
- Respects `# noqa: F401` comments (matches flake8 behavior)
- Full scope analysis with LEGB rule:
  - Correctly handles function parameters that shadow imports
  - Handles class scope quirks (class body doesn't enclose nested functions)
  - Supports comprehension scopes and walrus operator bindings
  - Respects `global` and `nonlocal` declarations

### Directory exclusions

The tool automatically skips common non-source directories:
- Virtual environments: `.venv`, `venv`, `.env`, `env`
- Build artifacts: `build`, `dist`, `*.egg-info`
- Cache directories: `__pycache__`, `.mypy_cache`, `.pytest_cache`, `.ruff_cache`
- Version control: `.git`, `.hg`, `.svn`
- Other: `node_modules`, `.tox`, `.nox`, `.eggs`

### Autofix

- Safely handles empty blocks by inserting `pass`
- Partial removal from multi-import statements
- Handles semicolon-separated statements
- Handles backslash line continuations

## Examples

### Single-file example

Before:
```python
import os
import sys  # unused
from typing import List, Optional  # List unused
from pathlib import Path

def get_home() -> Optional[Path]:
    return Path(os.environ.get("HOME"))
```

After (`--fix`):
```python
import os
from typing import Optional
from pathlib import Path

def get_home() -> Optional[Path]:
    return Path(os.environ.get("HOME"))
```

### Cross-file re-export example

```python
# utils.py
from typing import List  # NOT unused - re-exported to main.py

# main.py
from utils import List
x: List[int] = []
```

Running `remove-unused-imports main.py` correctly preserves the `List` import in `utils.py` because it's used by `main.py`.

### Cascade detection example

```python
# main.py
from helpers import List  # unused - not used locally

# helpers.py
from utils import List    # becomes unused when main.py's import is removed

# utils.py
from typing import List   # becomes unused when helpers.py's import is removed
```

Running `remove-unused-imports --fix main.py` removes all three imports in a single pass.

### noqa comments

The tool respects `# noqa` comments matching flake8 behavior:

```python
import os  # noqa: F401  - kept (F401 = unused import)
import sys  # noqa       - kept (bare noqa suppresses all)
import re  # noqa: E501  - flagged (wrong code)
```

For multi-line imports, noqa applies per-line:

```python
from typing import (
    List,  # noqa: F401  - kept
    Dict,  # flagged (no noqa)
)
```

## Known Limitations

- **Star imports**: `from X import *` cannot be analyzed statically
- **Dynamic imports**: `importlib.import_module()` calls are not tracked
- **Namespace packages**: PEP 420 namespace packages are not supported

## Development

### Setup

```bash
git clone https://github.com/cmyui/remove-unused-imports-py
cd remove-unused-imports-py
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Running tests

```bash
# Run with pytest
pytest tests/ -v

# Run with tox (multiple Python versions)
tox

# Run with coverage
tox -e py
```

### Project structure

```
.
├── remove_unused_imports/
│   ├── __init__.py          # Public API exports
│   ├── __main__.py          # Entry point for python -m
│   ├── _main.py             # CLI and orchestration
│   ├── _data.py             # Data classes (ImportInfo, ModuleInfo, etc.)
│   ├── _ast_helpers.py      # AST visitors for import/usage collection
│   ├── _detection.py        # Single-file detection logic
│   ├── _autofix.py          # Autofix logic
│   ├── _resolution.py       # Module resolution (resolves imports to files)
│   ├── _graph.py            # Import graph construction
│   ├── _cross_file.py       # Cross-file analysis with cascade detection
│   └── _format.py           # Output formatting
├── tests/
│   ├── detection_test.py
│   ├── aliased_imports_test.py
│   ├── shadowed_imports_test.py
│   ├── scope_analysis_test.py
│   ├── special_imports_test.py
│   ├── type_annotations_test.py
│   ├── autofix_test.py
│   ├── file_operations_test.py
│   ├── cli_test.py
│   ├── resolution_test.py   # Module resolution tests
│   ├── graph_test.py        # Import graph tests
│   ├── cross_file_test.py   # Cross-file analysis tests
│   └── format_test.py       # Output formatting tests
├── pyproject.toml
├── tox.ini
└── .github/workflows/ci.yml
```

## License

MIT
