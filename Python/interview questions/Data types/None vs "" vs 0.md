These three are **different kinds of values**, and this is a common Python interview question.

### 1. `None`

`None` means **no value / value is absent**.

```python
name = None

print(name)
```

Output:

```text
None
```

Example:

```python
user = {
    "name": "Sumanth",
    "middle_name": None
}
```

It means the middle name **doesn't have a value**.

Check it using:

```python
if user["middle_name"] is None:
    print("No middle name")
```

✅ Use `is None`, not `== None`.

---

### 2. `""` — Empty String

`""` means the value **is a string**, but the string contains zero characters.

```python
name = ""

print(name)
print(type(name))
```

Output:

```text
<class 'str'>
```

Example:

```python
user = {
    "name": ""
}
```

This usually means:

> "The name field contains a string, but the string is empty."

For example, a user submitted a form but didn't enter a name.

---

### 3. `0` — Zero

`0` is an actual **numeric value**.

```python
age = 0

print(type(age))
```

Output:

```text
<class 'int'>
```

It means the number is actually zero.

Example:

```python
cart = {
    "items": 0
}
```

This means:

> The cart contains **zero items**.

---

### Important difference

```python
x = None
y = ""
z = 0

print(type(x))  # NoneType
print(type(y))  # str
print(type(z))  # int
```

Think of them as:

| Value  | Meaning      | Type       |
| ------ | ------------ | ---------- |
| `None` | No value     | `NoneType` |
| `""`   | Empty text   | `str`      |
| `0`    | Numeric zero | `int`      |

### One tricky interview point

All three are **falsy** in Python:

```python
if not None:
    print("Falsy")

if not "":
    print("Falsy")

if not 0:
    print("Falsy")
```

All three conditions execute.

But **falsy does NOT mean they are the same**.

For example:

```python
if age == 0:
    print("Age is zero")

if name == "":
    print("Name is empty")

if value is None:
    print("Value is missing")
```

### Interview answer

> **`None` represents absence of a value, `""` represents an empty string, and `0` represents the numeric value zero. Although all three are falsy in Python, they have different meanings and types.**

**Easy memory trick:**
`None` → **nothing**
`""` → **empty text**
`0` → **zero quantity**
