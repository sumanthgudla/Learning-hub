### 1. `is` vs `==`

This is a **very common Python interview question**.

#### `==` → compares **values**

It asks:

> "Do these two objects contain the same value?"

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a == b)
```

Output:

```text
True
```

Even though `a` and `b` are two different list objects, their **contents are equal**.

---

#### `is` → compares **identity**

It asks:

> "Are these two variables pointing to the exact same object in memory?"

```python
a = [1, 2, 3]
b = [1, 2, 3]

print(a is b)
```

Output:

```text
False
```

Because there are two different list objects.

Think:

```text
a ──────> [1, 2, 3]   ← Object 1

b ──────> [1, 2, 3]   ← Object 2
```

Values are the same → `==` → `True`

Objects are different → `is` → `False`

---

### Same object example

```python
a = [1, 2, 3]
b = a

print(a == b)   # True
print(a is b)   # True
```

Now:

```text
        ┌─────────────┐
a ──────┤             │
        │  [1,2,3]    │
b ──────┤             │
        └─────────────┘
```

Both point to the **same object**.

---

### ⭐ Most important use: `None`

Use:

```python
if value is None:
    print("No value")
```

Not:

```python
if value == None:
```

Why?

`None` is a **singleton** in Python—there is one `None` object—so `is None` explicitly checks whether the value is that exact `None` object.

### Easy interview answer

> **`==` checks whether two objects have equal values, while `is` checks whether they are the exact same object. We commonly use `is None` to check for `None`.**

**Memory trick:**

* `==` → **same value?**
* `is` → **same object?**
