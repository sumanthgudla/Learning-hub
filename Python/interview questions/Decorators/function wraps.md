## `functools.wraps`

This is an important decorator interview topic.

The problem is that when we create a decorator, the **wrapper function replaces the original function**, so Python can lose information about the original function.

### Example without `wraps`

```python
def decorator(func):
    def wrapper():
        """This is the wrapper"""
        return func()

    return wrapper


@decorator
def greet():
    """This function says hello"""
    print("Hello")


print(greet.__name__)
print(greet.__doc__)
```

You might expect:

```text
greet
This function says hello
```

But you get:

```text
wrapper
This is the wrapper
```

Why?

Because after decoration:

```python
greet = decorator(greet)
```

`greet` now points to the **wrapper**, not directly to the original function.

---

## Solution: `functools.wraps`

Python provides:

```python
from functools import wraps
```

Use it like this:

```python
from functools import wraps

def decorator(func):

    @wraps(func)
    def wrapper():
        """This is the wrapper"""
        return func()

    return wrapper


@decorator
def greet():
    """This function says hello"""
    print("Hello")


print(greet.__name__)
print(greet.__doc__)
```

Output:

```text
greet
This function says hello
```

`@wraps(func)` **preserves the metadata of the original function** on the wrapper.

---

### What metadata?

For example:

```python
greet.__name__
greet.__doc__
greet.__module__
```

It also maintains `__wrapped__`, which allows Python/tools to access the original function.

---

## Why is this important in real applications?

Imagine a Flask/FastAPI application:

```python
@app.get("/users")
@authentication
def get_users():
    """Get all users"""
    ...
```

Frameworks, debugging tools, logging systems, documentation generators, and testing tools may inspect function metadata.

Using:

```python
@wraps(func)
```

prevents your decorator from unnecessarily hiding that information.

### Interview answer

> **"`functools.wraps` is used inside a decorator to preserve the metadata of the original function, such as its name and docstring, when it is wrapped by another function. Without `wraps`, the decorated function appears to be the wrapper function."**

---

### One thing to remember

Whenever you write a decorator like:

```python
def decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        ...
    return wrapper
```

**`@wraps(func)` is the standard practice.**

Next is the **real-world use case**—for example, implementing an authentication or retry decorator, which is particularly relevant for your EPAM interview.
