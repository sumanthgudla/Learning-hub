### 1. `*args` and `**kwargs`

They are used when you **don't know in advance how many arguments** a function will receive.

#### `*args` → positional arguments

```python
def add(*args):
    print(args)

add(10, 20, 30)
```

Output:

```python
(10, 20, 30)
```

`args` is a **tuple**.

You can iterate over it:

```python
def add(*args):
    total = 0
    for num in args:
        total += num
    return total

print(add(10, 20, 30))  # 60
```

---

#### `**kwargs` → keyword arguments

```python
def user_info(**kwargs):
    print(kwargs)

user_info(name="Sumanth", age=27, role="AI Engineer")
```

Output:

```python
{'name': 'Sumanth', 'age': 27, 'role': 'AI Engineer'}
```

`kwargs` is a **dictionary**.

```python
def user_info(**kwargs):
    for key, value in kwargs.items():
        print(key, value)

user_info(name="Sumanth", role="Developer")
```

---

### Using both together

```python
def func(*args, **kwargs):
    print(args)
    print(kwargs)

func(10, 20, name="Sumanth", role="Developer")
```

Output:

```python
(10, 20)
{'name': 'Sumanth', 'role': 'Developer'}
```

### Interview answer

> **`*args` allows a function to accept a variable number of positional arguments, which Python collects into a tuple. `**kwargs` allows a function to accept a variable number of keyword arguments, which Python collects into a dictionary.**

**Easy way to remember:**

| Syntax     | Accepts              | Stored as  |
| ---------- | -------------------- | ---------- |
| `*args`    | Positional arguments | Tuple      |
| `**kwargs` | Keyword arguments    | Dictionary |

Also remember that `args` and `kwargs` are just **conventional names**. The `*` and `**` are what matter.
