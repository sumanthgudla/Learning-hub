## `map`, `filter`, `reduce`

These are **functional programming tools** commonly used to process collections.

### 1. `map()` → Transform every element

`map()` applies a function to **every item** in an iterable.

```python
numbers = [1, 2, 3, 4]

result = list(map(lambda x: x * 2, numbers))

print(result)
```

Output:

```text
[2, 4, 6, 8]
```

Think:

> **map = transform**

Equivalent `for` loop:

```python
result = []

for x in numbers:
    result.append(x * 2)
```

---

### 2. `filter()` → Keep matching elements

`filter()` keeps only the elements for which the condition is `True`.

```python
numbers = [1, 2, 3, 4, 5, 6]

result = list(filter(lambda x: x % 2 == 0, numbers))

print(result)
```

Output:

```text
[2, 4, 6]
```

Think:

> **filter = select**

Equivalent:

```python
result = []

for x in numbers:
    if x % 2 == 0:
        result.append(x)
```

---

### 3. `reduce()` → Combine into one value

`reduce()` repeatedly applies a function to the elements and produces **one final result**.

You need to import it:

```python
from functools import reduce
```

Example: sum all numbers.

```python
numbers = [1, 2, 3, 4]

result = reduce(lambda x, y: x + y, numbers)

print(result)
```

Output:

```text
10
```

How it works:

```text
1 + 2 = 3
3 + 3 = 6
6 + 4 = 10
```

Think:

> **reduce = combine**

---

### Easy way to remember

```text
map     → change every item
filter  → remove items that don't match
reduce  → combine everything into one value
```

| Function   | Purpose   | Example             |
| ---------- | --------- | ------------------- |
| `map()`    | Transform | `[1,2,3] → [2,4,6]` |
| `filter()` | Select    | `[1,2,3,4] → [2,4]` |
| `reduce()` | Aggregate | `[1,2,3,4] → 10`    |

### Interview question: Why use `map` instead of a list comprehension?

Both can do the same thing:

```python
list(map(lambda x: x * 2, numbers))
```

or

```python
[x * 2 for x in numbers]
```

For Python code, **list comprehensions are often more readable** for simple transformations.

### One important interview point

`map()` and `filter()` return **iterators**, not lists directly in Python 3.

```python
result = map(lambda x: x * 2, [1, 2, 3])

print(result)
```

To get a list:

```python
list(result)
```

### Interview answer

> **`map()` transforms each element, `filter()` selects elements based on a condition, and `reduce()` combines multiple elements into a single result. `map` and `filter` return iterators in Python 3, while `reduce` is available from the `functools` module.**
