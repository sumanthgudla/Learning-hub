### 1. Positional vs Keyword Arguments

The difference is **how Python matches the value to the parameter**.

### Positional arguments

Values are assigned based on their **position/order**.

```python
def introduce(name, age):
    print(name, age)

introduce("Sumanth", 27)
```

Here:

```text
name → "Sumanth"   # 1st position
age  → 27          # 2nd position
```

So the order matters:

```python
introduce(27, "Sumanth")
```

This is valid Python, but the values are assigned incorrectly:

```text
name → 27
age  → "Sumanth"
```

---

### Keyword arguments

Values are assigned using the **parameter name**.

```python
def introduce(name, age):
    print(name, age)

introduce(age=27, name="Sumanth")
```

The order doesn't matter because Python knows exactly which parameter each value belongs to.

```text
age  → 27
name → "Sumanth"
```

---

### You can combine both

```python
def introduce(name, age, city):
    print(name, age, city)

introduce("Sumanth", age=27, city="Vizag")
```

Here:

* `"Sumanth"` → positional
* `age=27` → keyword
* `city="Vizag"` → keyword

**Important interview rule:** positional arguments must come **before** keyword arguments.

❌ Invalid:

```python
introduce(name="Sumanth", 27, "Vizag")
```

✅ Valid:

```python
introduce("Sumanth", 27, city="Vizag")
```

### Interview answer

> **Positional arguments are matched to parameters based on their order, whereas keyword arguments are matched based on the parameter name. Positional arguments must come before keyword arguments when both are used.**
