Here's **Phase 2 — Topic 13: Exception Handling** in notes-friendly format:

---

# Phase 2 — Topic 13: Exception Handling (`try`, `except`, `finally`, `raise`)

## What is it?
Exception handling lets your program **gracefully handle errors** instead of crashing. Python uses `try/except` blocks to catch exceptions, `finally` to always run cleanup code, and `raise` to throw exceptions intentionally. Senior devs are expected to know the full exception hierarchy, how to handle multiple exceptions, and when to catch vs when to let exceptions propagate.

---

## 1. Basic `try/except`

```python
# Without exception handling — program crashes
result = 10 / 0   # ZeroDivisionError: division by zero


# With exception handling — graceful recovery
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero!")
    result = 0

print(result)   # 0


# try block — code that might fail
# except block — runs ONLY if specific error occurs
```

---

## 2. Catching Multiple Exceptions

```python
def process(value):
    try:
        result = 10 / int(value)
        return result

    except ZeroDivisionError:
        print("Cannot divide by zero")

    except ValueError:
        print("Invalid value — not a number")

    except TypeError:
        print("Wrong type passed")


process("2")     # 5.0
process("0")     # Cannot divide by zero
process("abc")   # Invalid value — not a number
process(None)    # Wrong type passed


# Catch multiple in ONE except
try:
    result = int("abc") / 0
except (ValueError, ZeroDivisionError) as e:
    print(f"Error: {e}")


# Catch ALL exceptions — use sparingly
try:
    risky_operation()
except Exception as e:
    print(f"Something went wrong: {e}")
    # Exception is base class for most built-in exceptions
```

---

## 3. `else` and `finally`

```python
try:
    result = 10 / 2
except ZeroDivisionError:
    print("Division by zero!")
else:
    # runs ONLY if NO exception occurred
    print(f"Success! Result: {result}")
finally:
    # ALWAYS runs — exception or not
    print("This always runs")


# Output:
# Success! Result: 5.0
# This always runs


# With exception:
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Division by zero!")
else:
    print("This won't run")   # skipped
finally:
    print("This always runs") # still runs

# Output:
# Division by zero!
# This always runs


# finally — perfect for cleanup
def read_file(path):
    f = None
    try:
        f = open(path)
        return f.read()
    except FileNotFoundError:
        print(f"File not found: {path}")
    finally:
        if f:
            f.close()   # ALWAYS closes, even if exception
```

---

## 4. `raise` — Throwing Exceptions

```python
# Raise a built-in exception
def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Denominator cannot be zero")
    return a / b

divide(10, 0)   # ZeroDivisionError: Denominator cannot be zero


# Raise with custom message
def set_age(age):
    if age < 0:
        raise ValueError(f"Age cannot be negative: {age}")
    if age > 150:
        raise ValueError(f"Age too large: {age}")
    return age


# Re-raise — catch, log, then re-raise same exception
def process():
    try:
        result = risky()
    except Exception as e:
        print(f"Logging error: {e}")
        raise    # re-raises the same exception


# Raise different exception from caught one
try:
    data = int("abc")
except ValueError as e:
    raise TypeError("Expected an integer") from e
    #                                        ↑
    #                              chains exceptions — shows original cause
```

---

## 5. Exception Chaining — `raise from`

```python
# raise X from Y — chains exceptions, shows full context

def connect_db():
    try:
        raise ConnectionError("DB timeout")
    except ConnectionError as e:
        raise RuntimeError("Service unavailable") from e


try:
    connect_db()
except RuntimeError as e:
    print(e)              # Service unavailable
    print(e.__cause__)    # DB timeout  ← original exception preserved


# raise X from None — suppress original exception
try:
    int("abc")
except ValueError:
    raise TypeError("Need integer input") from None
    # hides original ValueError — shows only TypeError
```

---

## 6. Python Exception Hierarchy

```
BaseException
├── SystemExit               ← sys.exit()
├── KeyboardInterrupt        ← Ctrl+C
├── GeneratorExit            ← generator closed
└── Exception                ← catch-all for normal errors
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   ├── OverflowError
    │   └── FloatingPointError
    ├── LookupError
    │   ├── IndexError       ← list[999]
    │   └── KeyError         ← dict["missing"]
    ├── TypeError
    ├── ValueError
    ├── AttributeError
    ├── NameError
    ├── OSError
    │   ├── FileNotFoundError
    │   ├── PermissionError
    │   └── TimeoutError
    ├── RuntimeError
    ├── StopIteration
    └── ImportError
```

```python
# Catching parent class catches all children too
try:
    my_list = [1, 2, 3]
    print(my_list[10])
except LookupError:        # catches BOTH IndexError and KeyError
    print("Lookup failed")

# Order matters — specific BEFORE general
try:
    risky()
except ZeroDivisionError:  # specific first
    print("Division error")
except ArithmeticError:    # general second
    print("Arithmetic error")
except Exception:          # most general last
    print("Unknown error")
```

---

## 7. `as e` — Accessing Exception Details

```python
try:
    result = int("abc")
except ValueError as e:
    print(type(e))      # <class 'ValueError'>
    print(e)            # invalid literal for int() with base 10: 'abc'
    print(e.args)       # ("invalid literal for int()...",)
    print(str(e))       # same as print(e)

    # Exception attributes
    import traceback
    traceback.print_exc()   # prints full stack trace


# Log full traceback to file
import traceback
import logging

logging.basicConfig(filename="errors.log")

try:
    risky_operation()
except Exception as e:
    logging.error(traceback.format_exc())   # full trace to log file
```

---

## 8. Context Managers + Exceptions

```python
# with + try/except together
try:
    with open("data.txt", "r") as f:
        data = f.read()
        result = int(data)    # might raise ValueError
except FileNotFoundError:
    print("File not found")
except ValueError:
    print("File doesn't contain a valid integer")


# suppress specific exceptions — from contextlib
from contextlib import suppress

with suppress(FileNotFoundError):
    open("nonexistent.txt").read()
# no crash — FileNotFoundError silently suppressed
# equivalent to try/except FileNotFoundError: pass
```

---

## 9. Common Exception Patterns — Senior Level

```python
# Pattern 1 — EAFP (Easier to Ask Forgiveness than Permission)
# Pythonic style — try and handle failure
try:
    value = my_dict["key"]
except KeyError:
    value = default_value


# Pattern 2 — LBYL (Look Before You Leap)
# Less Pythonic but sometimes clearer
if "key" in my_dict:
    value = my_dict["key"]
else:
    value = default_value


# Pattern 3 — specific then general
try:
    connect()
except ConnectionError as e:
    handle_connection_error(e)
except TimeoutError as e:
    handle_timeout(e)
except Exception as e:
    handle_unknown(e)
    raise   # re-raise if you can't handle it


# Pattern 4 — never silently swallow exceptions
try:
    risky()
except Exception:
    pass    # ❌ NEVER do this in production — hides all errors!

# at minimum log it
try:
    risky()
except Exception as e:
    logger.error(f"Error in risky(): {e}")
    raise   # re-raise after logging


# Pattern 5 — cleanup without suppressing
try:
    process_data()
except Exception:
    cleanup()    # do cleanup
    raise        # then re-raise — don't swallow
```

---

## Interview Questions They Actually Ask

**Q1: What's the difference between `except Exception` and `except BaseException`?**
> `Exception` catches all normal errors but NOT `SystemExit`, `KeyboardInterrupt`, or `GeneratorExit` — these inherit from `BaseException` directly. Catching `BaseException` would swallow `Ctrl+C` and `sys.exit()` — almost never what you want.

**Q2: When should you re-raise an exception?**
> When you want to **log or clean up** but not actually handle the error — let it propagate up to a caller that knows what to do. Re-raise with bare `raise` to preserve the original traceback. Never swallow exceptions silently with `except: pass`.

**Q3: What is the difference between `else` and `finally` in try blocks?**
> `else` runs only when **no exception occurred** — use for code that should run on success. `finally` runs **always** — exception or not — use for cleanup (closing files, releasing locks).

**Q4: What does `raise X from Y` do?**
> It chains exceptions — `X` is the new exception raised, `Y` is stored as `X.__cause__`. The traceback shows both exceptions with "The above exception was the direct cause" message. Use it when converting low-level exceptions to higher-level ones while preserving context.

**Q5: What's the EAFP principle in Python?**
> "Easier to Ask Forgiveness than Permission" — try the operation and catch exceptions if it fails, rather than checking preconditions. More Pythonic than LBYL (Look Before You Leap). Works well with Python's duck typing — check capability by trying, not by inspecting type.

---

## Practice Problems

**Beginner — `p2_t13_prac01_safe_operations.py`**
Write a function `safe_divide(a, b)` and `safe_convert(value, to_type)` with proper exception handling. Handle all edge cases.
```python
safe_divide(10, 2)      # 5.0
safe_divide(10, 0)      # "Error: Cannot divide by zero"
safe_divide("a", 2)     # "Error: Invalid types"

safe_convert("25", int)     # 25
safe_convert("3.14", float) # 3.14
safe_convert("abc", int)    # "Error: Cannot convert 'abc' to int"
```

---

**Senior level — `p2_t13_prac02_robust_pipeline.py`**
Build a data processing pipeline that:
- Reads a CSV file with student records
- Validates each row (name not empty, score between 0-100)
- Raises custom exceptions for invalid data (next topic preview)
- Logs all errors to `errors.log`
- Writes valid records to `valid_students.json`
- Never crashes — handles all exceptions gracefully
- Prints a final summary: total rows, valid, invalid, errors

```python
# Input CSV:
# name,score
# Arjun,85
# ,92        ← empty name
# Ravi,150   ← invalid score
# Sneha,abc  ← not a number
# Kiran,76
```

---

## Common Mistakes & Senior Traps

- **Bare `except:`** — catches EVERYTHING including `KeyboardInterrupt` and `SystemExit` — program can't be stopped with Ctrl+C. Always use `except Exception:` at minimum.
- **Silent swallowing** — `except: pass` hides bugs completely. Always log or re-raise.
- **Wrong exception order** — catching general before specific means specific never runs:
```python
except Exception:          # ❌ catches everything — ZeroDivisionError below never reached
    pass
except ZeroDivisionError:  # never reached
    pass
```
- **Using exceptions for flow control** — catching exceptions you know will happen as normal program logic is slow and unreadable. Use `if/else` for expected conditions.
- **Not using `from` when chaining** — `raise NewError() from original_error` preserves context. Without `from`, the original traceback is still shown but relationship is unclear.
- **Catching too broadly in libraries** — library code should raise specific exceptions and let callers decide how to handle them. Only top-level application code should catch broadly.

---

Say **next** for Topic 14: Custom Exceptions — the final topic!