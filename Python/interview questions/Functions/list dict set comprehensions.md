## List / Dict / Set Comprehensions

Comprehension is a **short and readable way to create collections from an iterable**, often with a condition.

---

### 1. List Comprehension

Creates a **list**.

Normal approach:

```python
numbers = [1, 2, 3, 4, 5]

squares = []

for num in numbers:
    squares.append(num * num)

print(squares)
```

Using list comprehension:

```python
squares = [num * num for num in numbers]

print(squares)
```

Output:

```text
[1, 4, 9, 16, 25]
```

### With condition

Get only even numbers:

```python
even = [num for num in numbers if num % 2 == 0]

print(even)
```

Output:

```text
[2, 4]
```

Think:

```python
[what_to_store for item in collection if condition]
```

---

### 2. Dictionary Comprehension

Creates a **dictionary**.

```python
numbers = [1, 2, 3, 4]

squares = {num: num * num for num in numbers}

print(squares)
```

Output:

```python
{1: 1, 2: 4, 3: 9, 4: 16}
```

With condition:

```python
even_squares = {
    num: num * num
    for num in numbers
    if num % 2 == 0
}
```

Output:

```python
{2: 4, 4: 16}
```

Think:

```python
{key: value for item in collection if condition}
```

---

### 3. Set Comprehension

Creates a **set**, so duplicate values are automatically removed.

```python
numbers = [1, 2, 2, 3, 3, 4]

unique_squares = {num * num for num in numbers}

print(unique_squares)
```

Output:

```text
{1, 4, 9, 16}
```

Notice that although `2` and `3` appeared twice, their squares appear only once.

Think:

```python
{expression for item in collection if condition}
```

---

### Quick comparison

| Type       | Syntax                              | Result     |
| ---------- | ----------------------------------- | ---------- |
| List       | `[expression for item in iterable]` | List       |
| Dictionary | `{key: value for item in iterable}` | Dictionary |
| Set        | `{expression for item in iterable}` | Set        |

### Interview example

**Question:** Get squares of even numbers from 1–10.

```python
result = [x * x for x in range(1, 11) if x % 2 == 0]
```

Output:

```text
[4, 16, 36, 64, 100]
```

### Interview answer

> **Comprehensions provide a concise way to create lists, dictionaries, or sets from iterables. They can include conditions and are generally more readable than writing a simple loop for collection creation.**

**One thing to remember:** Don't use a comprehension just because you can. If the logic becomes complicated or has multiple steps, a normal `for` loop is usually more readable.
