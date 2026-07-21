# Context Managers (Senior/Interview Level)

## 1. What is it

A context manager is any object that defines **what happens when you enter and exit a `with` block** — guaranteeing setup and teardown code runs regardless of whether the block succeeds or raises an exception. At senior level, this isn't just "use `with open()`" — it's about understanding the `__enter__`/`__exit__` protocol, how exception suppression works, how to write your own context managers (both class-based and generator-based via `contextlib`), and why they're the correct tool for managing **any resource with a lifecycle** (files, DB connections, locks, transactions, timers, mock patches).

## 2. Core concepts table

| Concept | Description |
|---|---|
| `with` statement | Enters a context manager, binds `__enter__`'s return to `as` target, calls `__exit__` on exit |
| `__enter__(self)` | Called on entry; its return value is bound to the `as` variable |
| `__exit__(self, exc_type, exc_val, exc_tb)` | Called on exit — always, even if an exception occurred; returns `True` to suppress the exception |
| `as` target | Bound to whatever `__enter__` returns — NOT the context manager object itself (usually) |
| `contextlib.contextmanager` | Decorator turning a generator function into a context manager — `yield` splits enter/exit |
| `contextlib.suppress(*excs)` | Context manager that silently suppresses specified exception types |
| `contextlib.ExitStack` | Dynamically manage a variable number of context managers in one `with` block |
| `contextlib.nullcontext` | A no-op context manager — useful as a conditional placeholder |
| Exception suppression | `__exit__` returning a truthy value swallows the exception; `None`/`False` re-raises it |
| Reentrant context managers | Safe to nest `with` calls on the same object; `threading.RLock` is one example |
| `contextlib.asynccontextmanager` | Same as `contextmanager` but for `async with` blocks |

## 3. Syntax & code examples

### Basic usage

```python
# Built-in example — file handle guaranteed to close even if an exception occurs
with open("data.txt", "w") as f:    # __enter__ returns the file object → f
    f.write("hello")
# __exit__ called here, closes the file automatically
# f.closed → True


# What the with statement ACTUALLY does under the hood:
f = open("data.txt", "w")
f.__enter__()          # returns f itself (for file objects)
try:
    f.write("hello")
finally:
    f.__exit__(None, None, None)   # (None, None, None) = no exception occurred
```

### Common real-world pattern: class-based context manager

```python
import time

class Timer:
    """Measures elapsed time for any block of code."""

    def __enter__(self):
        self.start = time.perf_counter()
        return self                          # bound to `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.elapsed = time.perf_counter() - self.start
        print(f"Elapsed: {self.elapsed:.4f}s")
        return False     # don't suppress exceptions — let them propagate

with Timer() as t:
    time.sleep(0.2)
    result = sum(range(1_000_000))

# → Elapsed: 0.2312s
print(t.elapsed)   # → 0.2312  (still accessible after the block)


# Real-world DB transaction pattern:
class DatabaseTransaction:
    def __init__(self, connection):
        self.conn = connection

    def __enter__(self):
        self.conn.begin()
        return self.conn              # caller uses the connection directly

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()        # no exception → commit
        else:
            self.conn.rollback()      # exception occurred → rollback
        return False                  # never suppress — let caller see the error
```

### Senior-level / non-obvious usage: `@contextmanager`, exception suppression, `ExitStack`

```python
from contextlib import contextmanager, suppress, ExitStack

# @contextmanager turns a generator into a context manager
# Everything BEFORE yield = __enter__
# Everything AFTER yield  = __exit__
@contextmanager
def managed_resource(name):
    print(f"Acquiring {name}")
    resource = {"name": name, "active": True}   # simulated resource
    try:
        yield resource              # value bound to `as` target
    except Exception as e:
        print(f"Error during {name}: {e}")
        raise                       # re-raise so caller still sees it
    finally:
        resource["active"] = False
        print(f"Releasing {name}")  # ALWAYS runs, even if exception occurs

with managed_resource("DB Connection") as res:
    print(f"Using: {res}")
# → Acquiring DB Connection
# → Using: {'name': 'DB Connection', 'active': True}
# → Releasing DB Connection


# Exception suppression — __exit__ returning True swallows the exception
class SuppressKeyError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is KeyError:
            print(f"KeyError suppressed: {exc_val}")
            return True     # ← this is what suppresses it; False/None would re-raise
        return False

with SuppressKeyError():
    d = {}
    print(d["missing"])    # normally raises KeyError
# → KeyError suppressed: 'missing'
# execution continues normally here ↓

# contextlib.suppress does this more cleanly:
with suppress(KeyError, TypeError):
    d = {}
    print(d["missing"])    # silently swallowed


# ExitStack — when you don't know HOW MANY context managers you need until runtime
files = ["a.txt", "b.txt", "c.txt"]

with ExitStack() as stack:
    handles = [
        stack.enter_context(open(f, "w"))   # each cm registered dynamically
        for f in files
    ]
    for i, fh in enumerate(handles):
        fh.write(f"content {i}")
# ALL file handles are closed here — ExitStack calls __exit__ on each in reverse order
```

**ASCII view — `with` block execution flow:**

```
with SomeContextManager() as x:
    [block body]

         ┌──────────────────────────────────────────────┐
         │           EXECUTION FLOW                     │
         │                                              │
         │  1. SomeContextManager().__enter__()         │
         │     └─► return value bound to x             │
         │                                              │
         │  2. [block body runs]                        │
         │        │                                     │
         │   ┌────┴─────────────────┐                  │
         │   │                      │                  │
         │  no exception         exception raised      │
         │   │                      │                  │
         │   ▼                      ▼                  │
         │  __exit__(               __exit__(          │
         │    None, None, None)       type,            │
         │                            value,           │
         │                            traceback)       │
         │                            │                │
         │                     returns True? ──► suppress (continue)
         │                     returns False?──► re-raise exception
         └──────────────────────────────────────────────┘
```

## 4. Internals / how it works

- The `with` statement is compiled to bytecode that calls `__enter__()`, wraps the body in an implicit `try/finally`, and always calls `__exit__()` in the `finally` branch — so teardown is **guaranteed** even if the process hits a `return`, `break`, or `continue` inside the `with` block.
- `__exit__` receives three arguments: `exc_type` (the exception class), `exc_val` (the exception instance), and `exc_tb` (the traceback object). All three are `None` if no exception occurred. This is why you should **always check `if exc_type is None`** in transaction-style managers rather than assuming success.
- Exception suppression: the `with` machinery checks the return value of `__exit__` — if it's truthy, it **clears the exception** (sets the interpreter's exception state back to None) and execution continues at the line after the `with` block as if nothing happened. If it's falsy or `None`, the exception propagates normally. This is the single most subtle/senior bit of context manager behavior.
- `@contextmanager` from `contextlib` works by creating a `_GeneratorContextManager` class that wraps your generator. Its `__enter__` calls `next()` on the generator to advance it to the `yield`. Its `__exit__` either calls `next()` again (if no exception) or calls `.throw(exc)` to inject the exception at the `yield` point — which is why you must wrap the `yield` in a `try/except` inside your `@contextmanager` function if you want to handle or suppress exceptions.
- `ExitStack` maintains an internal stack of `(is_context_manager, cm, exit_func)` tuples. When the `with ExitStack()` block exits, it calls each registered `__exit__` in **LIFO order** (last registered = first exited), mirroring normal Python scoping. It also handles the case where one cleanup itself raises — it collects all exceptions and chains them.
- For `async with`, the protocol uses `__aenter__` / `__aexit__` instead, and `@asynccontextmanager` works identically to `@contextmanager` but with `async def` and `async for`.

## 5. Interview questions

**Q1: What arguments does `__exit__` receive, and what's the significance of its return value?**
A: `__exit__(self, exc_type, exc_val, exc_tb)` — all three are `None` if the block exited cleanly, or the exception's class, instance, and traceback if one was raised. The return value controls exception propagation: returning a truthy value **suppresses** the exception (execution resumes after the `with` block normally); returning `False`, `None`, or nothing re-raises it. This is powerful but dangerous — accidentally returning `True` from `__exit__` is a real bug that silently swallows errors, which is why most context managers explicitly `return False`.

**Q2: In a `@contextmanager`-decorated generator, what happens if an exception is raised inside the `with` block and you don't have a `try/except` around the `yield`?**
A: The `_GeneratorContextManager.__exit__` will call `.throw(exc_type, exc_val, exc_tb)` on your generator, injecting the exception at the `yield` point. Without a `try/except`, this kills the generator (it propagates out), and the `@contextmanager` machinery will re-raise it — so the exception still propagates to the caller, and any cleanup code after the `yield` that's **not** in a `finally` block won't run. Best practice is always to wrap the `yield` in `try/finally` so cleanup code runs regardless.

```python
# WRONG — cleanup may not run on exception
@contextmanager
def risky():
    resource = acquire()
    yield resource
    release(resource)    # SKIPPED if exception occurs in the with block!

# RIGHT — cleanup always runs
@contextmanager
def safe():
    resource = acquire()
    try:
        yield resource
    finally:
        release(resource)    # guaranteed to run
```

**Q3: What's the difference between `__enter__` returning `self` vs returning something else? When does each make sense?**
A: `return self` (e.g., `threading.Lock`) makes sense when the `as` target should *be* the context manager itself — the caller interacts with the same object. Returning something else (e.g., `open()` returning the file object, or a DB transaction returning the connection) makes sense when the context manager is just a lifecycle controller and the caller needs a different object to actually work with. Returning `None` is fine when the `as` clause isn't needed at all (e.g., `suppress`).

**Q4: When would you use `contextlib.ExitStack`, and what problem does it solve that a plain `with` block can't?**
A: `ExitStack` solves the problem of managing a **dynamically-determined number** of context managers. A plain `with` block requires knowing at write-time how many CMs you need (`with open(a) as f1, open(b) as f2`). When the number of resources depends on runtime data (e.g., opening N files from a list, or conditionally adding a lock depending on a flag), `ExitStack` lets you register them dynamically via `stack.enter_context(cm)`, and guarantees all of them get properly exited in LIFO order when the stack's `with` block exits — even if some of them raised during setup.

**Q5: How would you write a context manager that suppresses only `ValueError` but lets all other exceptions propagate?**
A: Either use `contextlib.suppress(ValueError)` (built-in), or in a class-based implementation, check `exc_type` in `__exit__`:

```python
class SuppressValueError:
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return exc_type is ValueError  # True suppresses; False/None re-raises anything else
```

In a `@contextmanager` version, catch it explicitly around the `yield`:

```python
@contextmanager
def suppress_value_error():
    try:
        yield
    except ValueError:
        pass    # swallowed; anything else propagates naturally
```

## 6. Practice problems

**Beginner:**
Write a class-based context manager `TempDirectory` that creates a temporary directory on `__enter__` (use `tempfile.mkdtemp()`), returns the path as the `as` target, and on `__exit__` deletes the directory and all its contents (use `shutil.rmtree()`), regardless of whether an exception occurred inside the block. Test it by creating a file inside the temp directory and confirming the directory no longer exists after the block.
- Suggested filename: `contextmanagers_prac01_temp_directory.py`
- Expected: directory exists inside the block, is gone after it

**Senior:**
Build a `@contextmanager`-based **database transaction simulator** with the following requirements:

1. `managed_transaction(db, label)` — takes a fake `db` object (a simple class you write) and a label string.
2. On `__enter__`: log `"[label] BEGIN TRANSACTION"`, call `db.begin()`.
3. On successful exit: call `db.commit()`, log `"[label] COMMITTED"`.
4. On exception: call `db.rollback()`, log `"[label] ROLLED BACK — reason: {exc}"`, then **re-raise** the exception.
5. If `db.commit()` itself raises (simulate this with a flag), it must still call `db.rollback()` and re-raise.
6. Use `ExitStack` in a second function `run_multi_transaction(db_list)` that opens a transaction on each DB in `db_list` simultaneously — if any one of them fails mid-way, all already-open transactions must still roll back correctly.

- Suggested filename: `contextmanagers_prac02_db_transaction.py`
- Test with: one normal transaction (commits), one that raises mid-block (rolls back), and one where `commit()` itself raises.

## 7. Common mistakes & senior traps

- **Returning `True` accidentally from `__exit__`** when you meant to return nothing — this silently suppresses every exception the `with` block could raise, masking bugs in production.
  ```python
  # WRONG — True suppresses ALL exceptions
  def __exit__(self, exc_type, exc_val, exc_tb):
      self.release()
      return True         # ← accidental exception vacuum cleaner

  # RIGHT
  def __exit__(self, exc_type, exc_val, exc_tb):
      self.release()
      return False        # or just: return / don't return anything
  ```

- **Not wrapping `yield` in `try/finally` inside `@contextmanager`**, so cleanup is skipped when an exception fires inside the `with` block — the most common `@contextmanager` mistake.

- **Confusing the `as` target with the context manager object** — `as f` is bound to what `__enter__` *returns*, not the CM itself. For `open()`, they happen to be the same object, which reinforces a wrong mental model.

- **Re-using an exhausted `@contextmanager` generator** — a generator-based CM can only be used *once*. Trying to reuse the same object from a second `with` block raises `RuntimeError: generator didn't yield`.
  ```python
  cm = managed_resource("db")
  with cm: pass
  with cm: pass   # WRONG → RuntimeError
  # RIGHT: call the factory function again each time
  with managed_resource("db"): pass
  with managed_resource("db"): pass
  ```

- **Using a `with` block when no resource lifecycle is involved** — not every pair of setup/teardown needs a CM; overusing them for pure logic flow makes code harder to read.

- **Forgetting that `__exit__` is called even on `return` inside the block** — this is a feature, not a bug, but surprises developers who expect `return` to "bypass" teardown.
  ```python
  def risky():
      with open("file.txt") as f:
          return f.read()
      # __exit__ still called here even though we returned — file is properly closed
  ```

- **Not handling the case where `__enter__` itself raises** — if `__enter__` throws, `__exit__` is **never** called (there's nothing to exit). Resource setup that can fail must handle cleanup inside `__enter__` itself (or the resource-acquiring code), not rely on `__exit__`.

---

Say **"next"** when you're ready for **Dataclasses**, or ask for more practice problems on context managers first.