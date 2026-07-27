# Phase 3, Topic 7: Writing Packages

## 1. What is it

A Python **package** is a directory containing an `__init__.py` (or, since Python 3.3+, optionally none — a "namespace package") that groups related modules under a single importable name. This matters at senior level because how you structure a package directly affects import behavior, circular-import risk, what gets published to PyPI, and how cleanly your codebase scales past a handful of files — interviewers use this to check whether you've actually *shipped* real Python software versus just written scripts.

## 2. Core concepts table

| Concept | What it does |
|---|---|
| Module | A single `.py` file — the smallest unit of import |
| Package | A directory with `__init__.py`, containing modules/subpackages |
| Regular package | Has an `__init__.py` file (traditional, explicit) |
| Namespace package | No `__init__.py`; Python 3.3+ implicit package spanning multiple dirs |
| `__init__.py` | Runs on package import; controls what's exposed at package level |
| `__all__` | List controlling what `from package import *` exports |
| Absolute import | `from mypackage.utils import helper` |
| Relative import | `from .utils import helper` (`.` = current package, `..` = parent) |
| `sys.path` | List of directories Python searches for modules on import |
| `pyproject.toml` | Modern standard for package metadata/build config (PEP 517/518) |
| `setup.py`/`setup.cfg` | Legacy build config (setuptools), still common in older repos |
| `src/` layout | Package code lives under `src/mypackage/`, not repo root — avoids accidental imports of uninstalled code |
| Entry points | Console scripts / plugin hooks declared in package metadata |
| `pip install -e .` | Editable install — symlinks package so local edits are picked up live |
| `__main__.py` | Lets a package be run via `python -m mypackage` |

## 3. Syntax & code examples

### Basic usage

```
myproject/
    mypackage/
        __init__.py
        core.py
        utils.py
```

```python
# mypackage/utils.py
def add(a, b):
    return a + b
```

```python
# mypackage/core.py
from .utils import add   # relative import — "." means "same package"

def compute(x, y):
    return add(x, y) * 2
```

```python
# mypackage/__init__.py
from .core import compute   # re-export so users can do: from mypackage import compute

__all__ = ["compute"]
```

```python
# main.py (outside the package)
from mypackage import compute
print(compute(2, 3))
# → 10
```

### Common real-world pattern — the `src/` layout with `pyproject.toml`

```
myproject/
    pyproject.toml
    src/
        mypackage/
            __init__.py
            core.py
    tests/
        test_core.py
```

```toml
# pyproject.toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "mypackage"
version = "0.1.0"
dependencies = ["requests>=2.31"]

[project.scripts]
mypackage-cli = "mypackage.cli:main"   # creates a `mypackage-cli` terminal command
```

```bash
# Editable install — changes to src/mypackage are picked up immediately,
# no reinstall needed, but it's still imported as a REAL installed package
pip install -e .

python -c "import mypackage; print(mypackage.__file__)"
# → /myproject/src/mypackage/__init__.py
```

Why `src/` matters: if your package lived at the repo root (`myproject/mypackage/`), running scripts from the repo root would let `import mypackage` accidentally succeed via `sys.path[0]` (the current directory) even *without* installing it — hiding packaging bugs until someone installs it elsewhere and it breaks. The `src/` layout forces you to actually install the package to import it, catching those bugs early.

### Senior-level / non-obvious usage

```python
# mypackage/__main__.py
# Lets your package be executed directly as a program:
#   python -m mypackage --flag value
def main():
    print("Running as a module!")

if __name__ == "__main__":
    main()
```

```python
# Lazy/deferred imports inside __init__.py to avoid heavy startup cost
# and circular imports — common in large SDKs (e.g. boto3, pandas internals)

# mypackage/__init__.py
def __getattr__(name):
    # PEP 562: module-level __getattr__, only called on ATTRIBUTE ACCESS,
    # not at import time — defers the real import until actually needed.
    if name == "heavy_module":
        from . import heavy_module
        return heavy_module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

# Usage:
import mypackage
mypackage.heavy_module   # only NOW does the expensive import happen
```

```python
# Breaking a circular import using a local (function-level) import
# mypackage/a.py
def use_b():
    from .b import helper_b   # imported INSIDE the function, not at module top
    return helper_b()

# mypackage/b.py
def helper_b():
    from .a import use_a      # avoids "ImportError: cannot import name" at load time
    return "b calling a would go here"
```

## 4. Internals — how it works under the hood

```
import mypackage.core
      │
      ▼
1. Python checks sys.modules cache
      — already imported? return cached module object immediately.
      ▼
2. Not cached → search sys.path (a list of directories) using "finders"
      — MetaPathFinder objects try in order: built-in, frozen, then PathFinder
      ▼
3. PathFinder walks sys.path entries looking for:
      mypackage/__init__.py   (regular package)
      OR just mypackage/ with no __init__.py (namespace package, PEP 420)
      ▼
4. Finds it → a "loader" reads and executes the module's code ONCE,
      creating a module object, storing it in sys.modules['mypackage']
      ▼
5. Executing mypackage/__init__.py may itself trigger imports of
      mypackage.core, mypackage.utils, etc. — each also cached in sys.modules
      ▼
6. Attribute access: mypackage.core.compute(...)
      — "mypackage" is just a Python object with attributes;
        submodules become attributes of the parent package object
        once imported.
```

Key internals:

- **`sys.modules` is the real cache and the source of truth.** Importing the same module twice doesn't re-run its code — it returns the cached object. This is why mutable module-level state (e.g., a global config dict) behaves like a singleton across your whole program.
- **Regular packages vs namespace packages**: a package *with* `__init__.py` is loaded from a single directory and that file's code always runs on first import. A package *without* `__init__.py` (namespace package, PEP 420) can be *split across multiple directories on `sys.path`* — Python merges them into one logical package at import time. This is how large ecosystems (e.g., Google's `google.cloud.*` packages) let independently-installed distributions contribute to the same top-level namespace.
- **Relative imports (`from .utils import x`) are resolved via the module's `__package__` attribute**, not the filesystem path directly — this is why relative imports fail with "attempted relative import with no known parent package" when you run a file directly as a script (`python mypackage/core.py`) instead of as part of a package (`python -m mypackage.core`): run directly, `__package__` is `None`/empty, so there's no "parent" to resolve `.` against.
- **`pip install -e .` (editable install)** works by writing a small `.pth` file (or, in modern setuptools, a lightweight import hook) into `site-packages` that points back at your `src/` directory, rather than copying files — so edits to source are reflected without reinstalling.

## 5. Interview questions

**Q1: What's the difference between a module and a package?**
A: A module is a single `.py` file — the unit `import` operates on at the lowest level. A package is a directory that groups multiple modules (and possibly subpackages) under one importable namespace, historically signaled by containing an `__init__.py`. Every package is technically also a module internally (it has a module object with a `__path__` attribute that regular modules lack, which is what lets Python search inside it for submodules).

**Q2: Why would you choose a `src/` layout over putting the package at the repo root?**
A: With the package at the repo root, running any script or test from that directory lets `import mypackage` succeed via the implicit current-directory entry in `sys.path`, even if the package was never properly installed — this can mask real packaging bugs (missing dependencies in `pyproject.toml`, broken `MANIFEST.in`, etc.) that only surface when someone else installs your package elsewhere. The `src/` layout removes that accidental success path, forcing an actual `pip install -e .` for local development, so what you test locally matches what gets installed by users.

**Q3: How do circular imports happen, and how do you fix them?**
A: They happen when module A imports module B at module load time, and B (directly or transitively) imports A back, before A has finished executing — so B tries to access a name in A's partially-initialized module object and gets an `ImportError` or `AttributeError`. Fixes, in order of preference: (1) restructure the code so the shared logic lives in a third module both can import without needing each other; (2) move the import inside the function/method that needs it (deferring it past module-load time); (3) use `TYPE_CHECKING`-guarded imports if it's purely for type hints. Circular imports are usually a signal of tangled module responsibilities, not just an import-ordering nuisance.

**Q4: What does `__init__.py` actually do, and can a package exist without one?**
A: `__init__.py` runs automatically the first time its package is imported, and is commonly used to re-export selected names so users get a clean public API (`from mypackage import Thing` instead of `from mypackage.internal.thing_impl import Thing`), define `__all__`, or do package-level setup. Since Python 3.3 (PEP 420), a directory *without* `__init__.py` can still be imported as a "namespace package" — useful for splitting a single logical package across multiple distributions/directories — but it loses the ability to run init-time code and behaves slightly differently in import resolution (it's found only after regular packages are checked).

**Q5: What's the difference between `pip install .` and `pip install -e .`?**
A: `pip install .` copies your package's files into `site-packages` as a snapshot — any subsequent code changes require reinstalling. `pip install -e .` ("editable"/"develop" mode) instead links back to your source directory (historically via a `.egg-link`/`.pth` file, now via PEP 660 editable wheels), so changes to your source are immediately visible the next time you import the package, without reinstalling — essential for iterative local development and for running your test suite against live code.

## 6. Practice problems

**Beginner** — `packages_prac01_basic_package_structure.py`
Create a package `shapes/` with `__init__.py`, `circle.py` (function `area(radius)`), and `square.py` (function `area(side)`). In `__init__.py`, re-export both as `circle_area` and `square_area`. Write a `main.py` outside the package that imports and calls both.

Expected output:
```python
from shapes import circle_area, square_area
print(circle_area(2))   # → 12.566370614359172
print(square_area(3))   # → 9
```

**Senior** — `packages_prac02_plugin_registry.py`
Build a mini plugin-loading package `plugins/` where:
- `plugins/__init__.py` exposes a `register(name)` decorator and a `run(name, *args)` function, backed by an internal dict registry.
- Individual plugin modules (`plugins/upper.py`, `plugins/reverse.py`) each define one function decorated with `@register("upper")` / `@register("reverse")`, but are **not** imported directly by `__init__.py`'s top-level code — instead, use `pkgutil.iter_modules` (or `importlib`) inside a `load_plugins()` function to dynamically discover and import every module in the `plugins` package at runtime, so adding a new plugin file requires zero edits to `__init__.py`.
- Demonstrate that after calling `load_plugins()`, `run("upper", "hello")` returns `"HELLO"` and `run("reverse", "hello")` returns `"olleh"`.

Expected output:
```python
load_plugins()
run("upper", "hello")     # → "HELLO"
run("reverse", "hello")   # → "olleh"
```

## 7. Common mistakes & senior traps

- **Shadowing standard library / third-party module names.** Naming your own file `json.py` or `requests.py` inside a project can shadow the real library depending on `sys.path` order, causing baffling import errors.

  ```python
  # WRONG: myproject/json.py exists, and myproject/ is on sys.path
  import json
  json.loads(...)   # → AttributeError: module 'json' has no attribute 'loads'
                     #   (imported YOUR json.py, not the stdlib one!)
  ```

- **Using `from package import *` in library code.** It pollutes the caller's namespace unpredictably and ignores explicit control unless `__all__` is defined — fine occasionally in interactive/notebook use, risky in shipped code.

  ```python
  # WRONG (in a library's __init__.py, no __all__ defined)
  from .core import *   # exports EVERYTHING public, including accidental leaks

  # RIGHT
  from .core import compute
  __all__ = ["compute"]   # explicit, controlled public API
  ```

- **Forgetting `__init__.py` re-exports means users need deep import paths.** Without curating the public API, users must write `from mypackage.internal.submodule.impl import Thing` — a sign of a leaky, unpolished package.

- **Confusing "installed package" with "folder that happens to import."** Running scripts from inside a package's parent directory can make imports "work" locally while being completely broken for anyone who actually `pip install`s it — the `src/` layout mistake from Q2 above.

- **Not understanding that module-level code runs exactly once, on first import, ever (per process).** Junior engineers sometimes expect a module to "re-run" configuration logic on each `import` statement elsewhere in the code — it doesn't; only the first import executes the module body, everything after reads from the `sys.modules` cache.

Say "next" when you're ready to move to **JSON & CSV**.