# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/detection_test.py -v

# Run a specific test by name
pytest tests/ -v -k "test_shadowed_by_assignment"

# Run tests with coverage
tox -e py

# Run tests across all Python versions (3.10-3.14)
tox
```

## Architecture

This is a single-module Python linter (`unused_import_linter.py`) that detects and autofixes unused imports using AST analysis.

### Core Components

**Import Extraction** (`ImportExtractor`): AST visitor that collects all imports, tracking the bound name (considering aliases), module, and line numbers. Skips `__future__` imports.

**Usage Collection** (`NameUsageCollector`): AST visitor that finds all name usages. Only counts `ast.Load` contexts (not `Store`) to correctly handle shadowed imports. Explicitly visits function decorators, annotations, default arguments, and class bases.

**String Annotation Handling** (`StringAnnotationVisitor`): Parses string literals as type annotations to detect forward reference usage.

**`__all__` Handling** (`collect_dunder_all_names`): Extracts names from `__all__` assignments so exported names aren't flagged as unused.

**Autofix** (`remove_unused_imports`): Removes unused imports while preserving valid Python. Key behavior:
- Partial removal from multi-import statements (`from X import a, b, c` → `from X import a`)
- Inserts `pass` when removing imports would leave a block empty (uses `_find_block_only_imports`)

### Test Organization

Tests follow pyupgrade patterns: one file per feature, heavy use of `pytest.param()` with descriptive IDs, `_noop` suffix for "should NOT flag" tests.
