# Pylance Import Resolution Issue Documentation

## Problem Description

This repository demonstrates a specific issue with Pylance (Microsoft's Python language server) where it cannot resolve imports from packages installed in `site-packages` when there's a namespace collision with local packages in the `src/` directory.

## Reproduction Steps

1. **Create a namespace package structure:**
   ```
   src/
   └── zope/
       ├── __init__.py          # namespace package
       └── mytest/
           └── __init__.py      # imports from zope.interface
   ```

2. **Install a package with the same namespace:**
   ```bash
   pip install zope.interface
   ```

3. **Import from the installed package:**
   ```python
   # In src/zope/mytest/__init__.py
   from zope.interface import Interface, implementer
   ```

4. **Observe the Pylance error:**
   ```
   Não foi possível resolver a importação "zope.interface"Pylance (reportMissingImports)
   ```

## Verification That Code Works

Despite the Pylance error, the code works perfectly:

```bash
# Install and test
make install-dev
make test     # ✅ All tests pass
make example  # ✅ Runs without errors

# Direct verification
source venv/bin/activate
python -c "from zope.mytest import MyImplementation; print(MyImplementation().my_method())"
# Output: Hello from zope.mytest!
```

## Technical Details

### Why It Happens

1. **Namespace Package Mechanics:**
   - `src/zope/__init__.py` creates a namespace package
   - `zope.interface` is also a namespace package installed in site-packages
   - Python's import system correctly handles this at runtime

2. **Pylance Limitation:**
   - Pylance sees the local `src/zope/` directory
   - When resolving `from zope.interface import ...`, it looks within the local namespace first
   - It fails to fall back to `site-packages` for the `zope.interface` module
   - This is a bug/limitation in Pylance's import resolution algorithm

### Runtime vs Static Analysis

- **Runtime (Python interpreter):** ✅ Works correctly
  - Uses proper namespace package resolution
  - Finds `zope.interface` in site-packages
  - Executes without errors

- **Static Analysis (Pylance):** ❌ Shows error
  - Cannot resolve the import path
  - Shows false positive import error
  - Code intelligence features may be limited

## Workarounds

### 1. Type Ignore Comment
```python
from zope.interface import Interface, implementer  # type: ignore
```

### 2. VS Code Settings
Add to `.vscode/settings.json`:
```json
{
  "python.analysis.extraPaths": ["./venv/lib/python3.*/site-packages"],
  "python.analysis.autoImportCompletions": true
}
```

### 3. Pylance Settings
```json
{
  "python.analysis.diagnosticSeverityOverrides": {
    "reportMissingImports": "information"
  }
}
```

## Expected Behavior

Pylance should:
1. Recognize namespace packages correctly
2. Fall back to site-packages when imports are not found locally
3. Not show false positive import errors for correctly installed packages

## Environment Information

- **Python:** 3.10+
- **Pylance:** Current version (as of October 2025)
- **Package Structure:** Namespace packages with `src/` layout
- **Issue:** Import resolution for same-namespace packages in site-packages

## Reproduction Repository

This repository (`zope.mytest`) serves as a minimal reproduction case for this Pylance issue.