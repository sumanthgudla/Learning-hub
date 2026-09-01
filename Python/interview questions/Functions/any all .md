## `any()` and `all()`

Both are used to check **conditions across multiple values** and return `True` or `False`.

### 1. `any()` → Is at least ONE true?

```python
numbers = [1, 3, 5, 8]

result = any(x % 2 == 0 for x in numbers)

print(result)
```

Output:

```text
True
```

Why? Because `8` is even.

Think:

> **`any()` = Does at least one satisfy the condition?**

Example:

```python
numbers = [1, 3, 5]

print(any(x % 2 == 0 for x in numbers))
```

Output:

```text
False
```

None of them are even.

---

### 2. `all()` → Are ALL true?

```python
numbers = [2, 4, 6, 8]

result = all(x % 2 == 0 for x in numbers)

print(result)
```

Output:

```text
True
```

Every number is even.

But:

```python
numbers = [2, 4, 5, 8]

print(all(x % 2 == 0 for x in numbers))
```

Output:

```text
False
```

Because `5` is not even.

Think:

> **`all()` = Does every element satisfy the condition?**

---

### Easy comparison

```text
any() → at least ONE is True
all() → EVERY one is True
```

| Values                  | `any()` | `all()` |
| ----------------------- | ------: | ------: |
| `[True, True, True]`    |  `True` |  `True` |
| `[True, False, True]`   |  `True` | `False` |
| `[False, False, False]` | `False` | `False` |

### Very common interview example

Check whether a list contains a negative number:

```python
numbers = [10, 20, -5, 30]

if any(x < 0 for x in numbers):
    print("Negative number exists")
```

Check whether **all** numbers are positive:

```python
if all(x > 0 for x in numbers):
    print("All numbers are positive")
```

### Interview answer

> **`any()` returns `True` if at least one element in the iterable is truthy, while `all()` returns `True` only if every element is truthy. Both can be used with generator expressions to efficiently check conditions.**

One useful point: both **short-circuit**. `any()` stops as soon as it finds `True`; `all()` stops as soon as it finds `False`.
