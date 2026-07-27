row=[0]*3
res=[]
res=[[row[i]]*4 for i in range(3)]
print(res)
'''
The **nested list bug** usually refers to accidentally creating **multiple references to the same inner list** instead of creating independent inner lists.

## The bug

Suppose you want a 3×4 matrix.

You write:

```python
matrix = [[0] * 4] * 3
```

It looks like:

```python
[
    [0, 0, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
```

But internally it is actually:

```
          +----------------+
matrix -->|                |
          |   * ---------- |----+
          |   * ---------- |----|----+
          |   * ---------- |----|----|
          +----------------+    |    |
                                |    |
                                v    |
                           [0,0,0,0] |
                                     |
                                     |
                                     +
```

All three rows point to **the same list**.

---

## Demonstration

```python
matrix = [[0] * 4] * 3

matrix[0][1] = 99

print(matrix)
```

Output

```python
[
    [0, 99, 0, 0],
    [0, 99, 0, 0],
    [0, 99, 0, 0]
]
```

You changed only one element, but every row changed.

---

## Why does this happen?

The `*` operator **does not copy nested objects**.

It repeats **references**.

```python
row = [0, 0, 0, 0]

matrix = [row, row, row]
```

This is essentially what

```python
[[0] * 4] * 3
```

creates.

---

## Verify using `id()`

```python
matrix = [[0] * 4] * 3

for row in matrix:
    print(id(row))
```

Output (addresses will differ)

```text
140512345678720
140512345678720
140512345678720
```

Every row has the same memory address.

---

## Correct way

Use a list comprehension.

```python
matrix = [[0] * 4 for _ in range(3)]
```

Now each iteration creates a **new inner list**.

```python
matrix[0][1] = 99

print(matrix)
```

Output

```python
[
    [0, 99, 0, 0],
    [0, 0, 0, 0],
    [0, 0, 0, 0]
]
```

Only the first row changes.

---

## Verify again

```python
matrix = [[0] * 4 for _ in range(3)]

for row in matrix:
    print(id(row))
```

Output

```text
140512345678720
140512345678464
140512345678336
```

Each row is a different object.

---

## General rule

This bug occurs whenever you use `*` on a container holding **mutable objects**.

### Bad

```python
a = [[]] * 5
```

or

```python
a = [[1, 2]] * 3
```

### Good

```python
a = [[] for _ in range(5)]
```

or

```python
a = [[1, 2] for _ in range(3)]
```

---

### Interview takeaway

A common interview question is: **Why does `[[0] * m] * n` cause a bug?**

A good answer is:

> `*` repeats references to the same inner list rather than creating new inner lists. Since lists are mutable, modifying one row modifies all rows. The fix is to use a list comprehension (`[[0] * m for _ in range(n)]`), which creates a new inner list on each iteration.
'''