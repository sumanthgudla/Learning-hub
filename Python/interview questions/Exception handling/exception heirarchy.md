# 6. Exception Hierarchy ⭐

Now let's understand **why `except Exception` can catch many different errors**.

Python exceptions are organized in a **class hierarchy**.

Think of it like inheritance.

```text
BaseException
│
├── Exception
│   │
│   ├── ValueError
│   ├── TypeError
│   ├── KeyError
│   ├── IndexError
│   ├── ZeroDivisionError
│   └── ...
│
├── KeyboardInterrupt
├── SystemExit
└── GeneratorExit
```

The important part for normal application code is:

```text
Exception
├── ValueError
├── TypeError
├── KeyError
├── IndexError
└── ...
```

---

## 1. Why does `except Exception` catch `ValueError`?

Because `ValueError` **inherits from `Exception`**.

Conceptually:

```python
class ValueError(Exception):
    ...
```

So:

```python
try:
    int("abc")

except Exception:
    print("Something went wrong")
```

works because:

```text
ValueError
   ↓
Exception
```

The exception is a child of `Exception`.

---

# 2. Specific vs general exceptions

Consider:

```python
try:
    int("abc")

except ValueError:
    print("Value error")

except Exception:
    print("Some other error")
```

Python checks:

```text
Is it ValueError?
       ↓
      YES
       ↓
"Value error"
```

It doesn't continue to the second `except`.

---

## 3. Why should specific exceptions come first?

Look at this:

```python
try:
    int("abc")

except Exception:
    print("General error")

except ValueError:
    print("Value error")
```

`ValueError` is already an `Exception`.

Therefore:

```text
ValueError
   ↓
Exception
```

The first handler catches it.

The `ValueError` handler will never get the opportunity to handle it.

So always follow:

```text
Specific
   ↓
More general
   ↓
Exception
```

Example:

```python
try:
    ...

except ValueError:
    ...

except TypeError:
    ...

except Exception:
    ...
```

---

# 4. What is `BaseException`?

`BaseException` is at the top of the hierarchy.

```text
BaseException
      ↓
  Exception
      ↓
 ValueError
```

But some exceptions directly inherit from `BaseException`, such as:

```text
KeyboardInterrupt
SystemExit
GeneratorExit
```

That's why this:

```python
except Exception:
```

normally doesn't catch `KeyboardInterrupt`.

For example, when you press:

```text
Ctrl + C
```

Python raises `KeyboardInterrupt`.

It is intentionally not a normal application exception.

---

# 5. Why shouldn't we use `except BaseException`?

Usually, you should **not** do this:

```python
try:
    ...
except BaseException:
    ...
```

because you're also catching things like:

* `KeyboardInterrupt`
* `SystemExit`
* `GeneratorExit`

You generally don't want to prevent the program from being interrupted or terminated.

For normal application error handling:

```python
except Exception:
```

is usually the appropriate broad catch.

---

# 6. `Exception` is a class

This is important.

When you write:

```python
except Exception:
```

`Exception` is a **class**.

Likewise:

```python
except ValueError:
```

`ValueError` is a class.

When Python raises an error, it creates an **exception object** from that class.

For example:

```python
raise ValueError("Invalid input")
```

Conceptually:

```text
ValueError class
      ↓
ValueError object
      ↓
"Invalid input"
```

And:

```python
except ValueError as e:
```

gives you that exception object in `e`.

---

# 7. Interview question ⭐

### Why does `except Exception` catch most exceptions?

Answer:

> "`Exception` is the base class for most standard application-level exceptions in Python. Exceptions such as `ValueError`, `TypeError`, and `KeyError` inherit from it, so an `except Exception` handler can catch them."

---

# 8. Another common interview question

### What is the difference between `Exception` and `BaseException`?

Answer:

> "`BaseException` is the root class of Python's exception hierarchy. `Exception` is its subclass and is the base class for most normal application exceptions. Exceptions such as `KeyboardInterrupt` and `SystemExit` inherit directly from `BaseException`, which is why we generally catch `Exception` rather than `BaseException`."

---

## 🧠 Remember this picture

```text
                BaseException
                /           \
               /             \
        Exception        SystemExit
           /  |  \        KeyboardInterrupt
          /   |   \
   ValueError TypeError KeyError
```

So when you write:

```python
except Exception:
```

you're basically saying:

> **"Catch any normal application exception that derives from `Exception`."**

---

### Progress

You've now covered:

✅ `try/except`
✅ Multiple `except`
✅ `else/finally`
✅ `raise`
✅ Custom exceptions
✅ Exception hierarchy

**Next → Real-world exception handling + best practices**, where we'll connect all of this to APIs, files, databases, logging, and production Python.
