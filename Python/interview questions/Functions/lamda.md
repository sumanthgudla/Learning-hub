### Lambda Function

A **lambda** is a small, anonymous function written in a single expression.

### Normal function

```python
def square(x):
    return x * x

print(square(5))
```

### Lambda equivalent

```python
square = lambda x: x * x

print(square(5))
```

Output:

```text
25
```

The syntax is:

```python
lambda arguments: expression
```

For example:

```python
add = lambda a, b: a + b

print(add(10, 20))
```

Output:

```text
30
```

### Common interview use: `sorted()`

Suppose:

```python
employees = [
    ("Alice", 50000),
    ("Bob", 75000),
    ("Charlie", 60000)
]
```

Sort by salary:

```python
employees.sort(key=lambda employee: employee[1])
```

Result:

```python
[
    ("Alice", 50000),
    ("Charlie", 60000),
    ("Bob", 75000)
]
```

Here:

```python
lambda employee: employee[1]
```

means:

> Take each employee tuple and use its salary (`employee[1]`) as the sorting key.

### Another common use: `map()`

```python
numbers = [1, 2, 3, 4]

squares = list(map(lambda x: x * x, numbers))

print(squares)
```

Output:

```text
[1, 4, 9, 16]
```

### Important limitation

A lambda can contain **only one expression**.

✅

```python
lambda x: x * 2
```

❌ You cannot write multiple statements like:

```python
lambda x:
    y = x * 2
    return y
```

### Interview answer

> **A lambda is an anonymous, single-expression function. It is useful for short operations, especially as a function argument to functions like `sorted()`, `map()`, and `filter()`.**

**Simple memory trick:**
`lambda x: x * 2` → **take `x`, do something, return the result.**
