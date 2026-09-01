### 1. Shallow Copy vs Deep Copy

> **Interview answer:**
> The difference is how nested or referenced objects are copied.
>
> A **shallow copy** creates a new outer object, but the nested objects inside it are still **shared** with the original.
>
> A **deep copy** creates a new outer object **and recursively creates copies of the nested objects**, so changes to nested data don't affect the original.

### Example

```python
import copy

original = [[1, 2], [3, 4]]

shallow = copy.copy(original)
deep = copy.deepcopy(original)
```

With shallow copy:

```python
shallow[0].append(5)

print(original)
# [[1, 2, 5], [3, 4]]
```

Why?

```text
original ──→ outer list
                ↓
             [1, 2] ←── shallow
```

The outer lists are different, but the inner `[1, 2]` is **shared**.

With deep copy:

```python
deep[0].append(6)

print(original)
# [[1, 2, 5], [3, 4]]
```

The original doesn't change because the nested list was also copied.

```text
original ──→ [ [1, 2], [3, 4] ]

deep     ──→ [ [1, 2], [3, 4] ]
                 ↑
             different object
```

### Easy way to remember

**Shallow copy:**

> New outer object + **same nested objects**

**Deep copy:**

> New outer object + **new nested objects**

### How do we create them?

```python
import copy

shallow = copy.copy(original)
deep = copy.deepcopy(original)
```

You can also create a shallow copy using:

```python
shallow = original.copy()
```

or:

```python
shallow = original[:]
```

for lists.

### Interview follow-up

**Q: Is shallow copy always a problem?**

> No. If the data is flat, such as `[1, 2, 3]`, there are no nested mutable objects to share, so shallow copying is usually sufficient. Deep copy is mainly important when the structure contains nested mutable objects.

**One-line answer to remember:**

> **"Shallow copy copies only the outer object and shares nested references; deep copy recursively copies the entire object structure."**




Absolutely. The easiest way to understand it is with a **nested list**.

### 1. Shallow Copy

```python
import copy

original = [[1, 2], [3, 4]]

shallow = copy.copy(original)

shallow[0][0] = 100

print(original)
print(shallow)
```

Output:

```text
[[100, 2], [3, 4]]
[[100, 2], [3, 4]]
```

### Why did `original` also change?

Think of the structure like this:

```text
original
   |
   v
 [  ───────────────  ]
   |              |
   v              v
 [1, 2]         [3, 4]
```

When we do:

```python
shallow = copy.copy(original)
```

Python creates a **new outer list**, but the inner lists are still shared:

```text
original ───────> [outer list]
                     |
                     +----> [1, 2]
                     |
                     +----> [3, 4]

shallow ────────> [new outer list]
                     |
                     +----> [1, 2]  ← SAME object
                     |
                     +----> [3, 4]  ← SAME object
```

So:

```python
shallow[0][0] = 100
```

modifies the **shared inner list**.

---

### 2. Deep Copy

```python
import copy

original = [[1, 2], [3, 4]]

deep = copy.deepcopy(original)

deep[0][0] = 100

print(original)
print(deep)
```

Output:

```text
[[1, 2], [3, 4]]
[[100, 2], [3, 4]]
```

Here, Python creates copies of the **outer list AND the nested lists**:

```text
original ───────> [outer list]
                     |
                     +----> [1, 2]
                     |
                     +----> [3, 4]

deep ───────────> [new outer list]
                     |
                     +----> [100, 2]  ← different object
                     |
                     +----> [3, 4]    ← different object
```

Therefore, changing `deep` doesn't affect `original`.

---

### Very important interview example

Consider:

```python
a = [1, 2, [3, 4]]

b = a.copy()

b.append(5)
b[2].append(6)

print(a)
print(b)
```

Output:

```text
[1, 2, [3, 4, 6]]
[1, 2, [3, 4, 6], 5]
```

Why?

`b.append(5)` affects only `b` because the **outer list is different**.

But:

```python
b[2].append(6)
```

affects both because `a[2]` and `b[2]` point to the **same nested list**.

### One-line interview answer

> **Shallow copy creates a new outer object but keeps references to nested objects, whereas deep copy creates independent copies of the nested objects as well.**

A good way to remember:

**Shallow = new box, same things inside.**
**Deep = new box, new things inside.**
