## ⚠️ Pylance Import Resolution Issue

This package demonstrates a known issue with Pylance where it cannot resolve imports from packages that are installed in site-packages when there's a namespace collision with packages in the `src/` folder.

**The Problem:**
- This package uses the `zope` namespace
- We import `from zope.interface import Interface` in `src/zope/mytest/__init__.py`
- Even though `zope.interface` is properly installed in site-packages, Pylance shows the error:
  ```
  Import "zope.interface" could not be resolved Pylance (reportMissingImports)
  ```

**Why it happens:**
- Pylance gets confused when there's a local `src/zope/` directory and tries to resolve `zope.interface` within the local namespace
- It doesn't properly fall back to site-packages for the `zope.interface` import
- The code runs perfectly fine despite the Pylance error

**Verification that it works:**
```bash
# The package installs and works correctly
make install-dev
make test    # All tests pass
make example # Runs without errors
```

This is a limitation of Pylance's import resolution algorithm with namespace packages.

## Installation

### Quick Setup with Makefile

The easiest way to set up the development environment:

```bash
# Create virtual environment and install in development mode
make install-dev

# Activate the virtual environment
source venv/bin/activate
```

### Manual Installation

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install zope.interface

# Install package in development mode
pip install -e .
```

## Usage

```python
from zope.mytest import IMyInterface, MyImplementation

# Usage example
obj = MyImplementation()
print(obj.my_method())
```

## Makefile Commands

The project includes a Makefile with the following commands:

- `make help` - Show available commands
- `make venv` - Create Python virtual environment
- `make install` - Install package dependencies
- `make install-dev` - Install package in development mode
- `make test` - Run tests
- `make example` - Run usage example
- `make lint` - Run code linting (installs pylint)
- `make format` - Format code with black
- `make check-format` - Check code formatting
- `make build` - Build package for distribution
- `make clean` - Remove virtual environment and build artifacts
- `make activate` - Show activation command
- `make verify-pylance-issue` - Demonstrate that code works despite Pylance errors

## Dependencies

- zope.interface

## Project Structure

```
zope.mytest/
├── src/
│   └── zope/
│       ├── __init__.py
│       └── mytest/
│           └── __init__.py
├── setup.py
├── pyproject.toml
└── README.md
```

## Development

For local development:

```bash
# Clone the repository
git clone <repo-url>
cd zope.mytest

# Quick setup with Makefile
make install-dev

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -e .
```

### Running Tests

```bash
# Using Makefile
make test

# Or manually
python tests.py
```

### Code Quality

```bash
# Format code
make format

# Check formatting
make check-format

# Run linting
make lint
```

### Build and Distribution

```bash
# Build package for distribution
make build

# Check dependencies
make check-deps
```

### Cleanup

```bash
# Remove virtual environment and build artifacts
make clean
```

## Troubleshooting

### Pylance Import Errors

If you see the error `Import "zope.interface" could not be resolved` in VS Code:

1. **This is a known Pylance limitation** - the code works fine despite the error
2. **Verify it works:** Run `make test` and `make example` - they will pass
3. **Alternative solutions:**
   ```python
   # Option 1: Add type: ignore comment
   from zope.interface import Interface, implementer  # type: ignore
   
   # Option 2: Use try/except (not recommended for this case)
   try:
       from zope.interface import Interface, implementer
   except ImportError:
       pass
   ```

4. **VS Code settings workaround:**
   Add to your `.vscode/settings.json`:
   ```json
   {
     "python.analysis.extraPaths": ["./venv/lib/python3.*/site-packages"]
   }
   ```

### Why This Happens

This repository specifically demonstrates this Pylance bug:
- Local `src/zope/` namespace conflicts with `zope.interface` in site-packages
- Pylance cannot resolve the import correctly
- Python runtime resolves it fine using proper namespace package mechanics

## Quick Start

1. Clone the repository
2. Run `make install-dev` to set up the development environment
3. Run `make example` to see the package in action
4. Run `make test` to verify everything works
5. Activate the virtual environment: `source venv/bin/activate`

## License

MIT License