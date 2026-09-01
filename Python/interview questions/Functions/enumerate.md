## `enumerate()` in Python

`enumerate()` is used when you want to **loop through a collection while also getting the index** of each element.

### Without `enumerate()`

```python
names = ["Alice", "Bob", "Charlie"]

for i in range(len(names)):
    print(i, names[i])
```

Output:

```text
0 Alice
1 Bob
2 Charlie
```

### With `enumerate()`

Much cleaner:

```python
names = ["Alice", "Bob", "Charlie"]

for index, name in enumerate(names):
    print(index, name)
```

Output:

```text
0 Alice
1 Bob
2 Charlie
```

Think:

> **`enumerate()` = give me the index + value while looping.**

---

### Starting from a different index

By default, indexing starts at `0`.

You can change it:

```python
names = ["Alice", "Bob", "Charlie"]

for index, name in enumerate(names, start=1):
    print(index, name)
```

Output:

```text
1 Alice
2 Bob
3 Charlie
```

---

### What does `enumerate()` return?

Like `zip()`, `enumerate()` returns an **iterator**.

```python
result = enumerate(["a", "b", "c"])

print(result)
```

You'll see something like:

```text
<enumerate object at 0x...>
```

You can convert it:

```python
print(list(result))
```

Output:

```python
[(0, 'a'), (1, 'b'), (2, 'c')]
```

---

### Common interview example

Find the index of a particular value:

```python
names = ["Alice", "Bob", "Charlie"]

for index, name in enumerate(names):
    if name == "Bob":
        print("Found at index:", index)
```

Output:

```text
Found at index: 1
```

### `enumerate()` vs `zip()`

| Function      | Purpose                         |
| ------------- | ------------------------------- |
| `enumerate()` | Gives **index + value**         |
| `zip()`       | Combines **multiple iterables** |

```python
enumerate(["A", "B"])
# (0, "A"), (1, "B")

zip(["A", "B"], [10, 20])
# ("A", 10), ("B", 20)
```

### Interview answer

> **`enumerate()` allows us to iterate over an iterable while getting both the index and the value. It returns an iterator of `(index, value)` pairs, and we can optionally specify the starting index using `start`.**
