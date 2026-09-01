### 1. Default Arguments

A **default argument** is a parameter that already has a value. If the caller doesn't provide a value, Python uses the default.

```python
def greet(name, city="Hyderabad"):
    print(name, city)

greet("Sumanth")
```

Output:

```text
Sumanth Hyderabad
```

Here, `city="Hyderabad"` is the **default argument**.

If you provide a value, the provided value overrides the default:

```python
greet("Sumanth", "Vizag")
```

Output:

```text
Sumanth Vizag
```

### Why use it?

When a parameter usually has a common/default value, but you still want to allow the caller to change it.

```python
def connect(host, port=8080):
    print(host, port)

connect("localhost")          # localhost 8080
connect("localhost", 5000)    # localhost 5000
```

### Important interview point ⚠️

Default arguments must come **after non-default arguments**.

✅ Correct:

```python
def func(name, age=25):
    pass
```

❌ Incorrect:

```python
def func(age=25, name):
    pass
```

Python gives a `SyntaxError`.

### Interview answer

> **A default argument is a parameter with a predefined value. If the caller doesn't provide that argument, Python uses the default value. If the caller provides a value, it overrides the default.**
