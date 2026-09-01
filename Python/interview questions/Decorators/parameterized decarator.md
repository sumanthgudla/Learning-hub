## Parameterized Decorator

A **parameterized decorator** is a decorator where we can pass configuration values to the decorator.

For example:

```python
@retry(3)
def call_api():
    ...
```

Here, `3` is the **parameter**.

### 1. Normal decorator

A normal decorator receives the function directly:

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper


@decorator
def hello():
    print("Hello")
```

Conceptually:

```python
hello = decorator(hello)
```

---

### 2. Parameterized decorator

Now suppose we want:

```python
@retry(3)
def call_api():
    ...
```

We need **one extra level**:

```python
def retry(times):                 # receives 3

    def decorator(func):          # receives call_api

        def wrapper(*args, **kwargs):  # executes call_api
            for i in range(times):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    print("Failed")

        return wrapper

    return decorator
```

Usage:

```python
@retry(3)
def call_api():
    print("Calling API")
    raise Exception("Failed")
```

### What happens?

This:

```python
@retry(3)
def call_api():
```

is equivalent to:

```python
call_api = retry(3)(call_api)
```

First:

```python
retry(3)
```

returns:

```python
decorator
```

Then:

```python
decorator(call_api)
```

returns:

```python
wrapper
```

So the flow is:

```text
@retry(3)
     ↓
retry(3)
     ↓
decorator
     ↓
decorator(call_api)
     ↓
wrapper
     ↓
call_api()
```

### Why 3 functions?

Because there are **3 levels of responsibility**:

```python
def retry(times):                  # 1. configuration
    def decorator(func):           # 2. receive function
        def wrapper(*args, **kwargs): # 3. execute function
            ...
        return wrapper
    return decorator
```

Think:

> **Outer function → gets parameters**
> **Middle function → gets the function**
> **Inner function → executes the function**

### Interview definition

> **"A parameterized decorator is a decorator that accepts configuration arguments, such as retry count or timeout. Because the decorator needs to receive both configuration and the target function, we use an additional outer function."**

For example:

```python
@retry(3)
@timeout(10)
@log
def process():
    pass
```

is a combination of **parameterized and normal decorators**.
