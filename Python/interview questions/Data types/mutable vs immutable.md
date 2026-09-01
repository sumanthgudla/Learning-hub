
### 1. Mutable vs Immutable in Python

> **Interview answer:**
> The main difference is whether an object's value can be changed **after the object is created**.
>
> **Mutable objects** can be modified in place, whereas **immutable objects cannot be modified after creation**.
>
> Common mutable types are **list, dictionary, and set**. Common immutable types are **int, float, string, tuple, and frozenset**.

### Example

```python
# Mutable
numbers = [1, 2, 3]
numbers.append(4)

print(numbers)
# [1, 2, 3, 4]
```

The same list object was modified.

For an immutable object:

```python
# Immutable
name = "John"
name = name + " Doe"
```

Here, Python doesn't modify the original `"John"` string. It creates a **new string object** and makes `name` reference it.

### Important interview point

**Immutable doesn't mean the variable cannot change.**

For example:

```python
x = 10
x = 20
```

`x` changed, but the integer object `10` itself was not modified. `x` was simply made to reference a different integer object.

Think of it as:

```text
x → 10

x = 20

x → 20
```

The original `10` wasn't changed.

### Why does immutability matter?

One important reason is **hashability**.

Immutable objects such as strings and integers can generally be used as dictionary keys:

```python
d = {
    "name": "John",
    10: "Ten"
}
```

A list cannot:

```python
d = {
    [1, 2]: "value"   # TypeError
}
```

because a mutable list cannot provide a stable hash.

### Quick comparison

|                                  | Mutable               | Immutable             |
| -------------------------------- | --------------------- | --------------------- |
| Can modify object in place?      | ✅                     | ❌                     |
| Examples                         | `list`, `dict`, `set` | `int`, `str`, `tuple` |
| Can generally be dictionary key? | ❌                     | ✅                     |
| Modification creates new object? | Usually no            | Yes                   |

**Likely EPAM follow-up:**
**"Is a tuple always immutable?"**

> The tuple structure itself is immutable, but it can contain mutable objects. For example, `([1, 2], 3)` cannot have its first element replaced, but the list inside it can still be modified.
