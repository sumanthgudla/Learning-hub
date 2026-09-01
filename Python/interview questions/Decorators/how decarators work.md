## How does `@decorator` work?

The `@decorator` syntax is just **Python's shorter syntax for replacing a function with the decorated version**.

Consider:

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper


@decorator
def greet():
    print("Hello")
```

When Python sees:

```python
@decorator
def greet():
    print("Hello")
```

it essentially converts it to:

```python
def greet():
    print("Hello")

greet = decorator(greet)
```

So **`greet` no longer refers directly to the original function**.

It now refers to:

```text
greet
  ↓
wrapper function
  ↓
original greet()
```

Therefore, when you call:

```python
greet()
```

Python actually executes:

```python
wrapper()
```

which does:

```python
print("Before")
func()       # original greet()
print("After")
```

Output:

```text
Before
Hello
After
```

### Interview answer

> **"`@decorator` is syntactic sugar for `function = decorator(function)`. The decorator receives the original function, creates a wrapper around it, and returns that wrapper. When we call the decorated function, we're actually calling the wrapper."**

One important point: **the decoration happens when the function is defined, not every time you call it.**

Next: **multiple decorators** and the order in which they execute.
