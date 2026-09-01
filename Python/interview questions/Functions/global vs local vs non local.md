It depends on **whether you're only reading the variable or assigning to it**.

### 1. Reading global variable → works without `global`

```python
x = 10

def test():
    print(x)

test()
```

Output:

```text
10
```

Python looks for `x` using LEGB:

```text
Local ❌
Enclosing ❌
Global ✅ → 10
```

---

### 2. Modifying/assigning global variable → `global` is required

```python
x = 10

def test():
    x = 20

test()

print(x)
```

Output:

```text
10
```

**Why didn't the global `x` change?**

Because:

```python
x = 20
```

inside the function creates a **new local variable `x`**.

So there are actually two variables:

```text
Global x → 10

test():
    Local x → 20
```

The local `x` disappears when the function finishes.

---

### 3. To actually modify the global variable

Use `global`:

```python
x = 10

def test():
    global x
    x = 20

test()

print(x)
```

Output:

```text
20
```

### Interview rule ⭐

> **You don't need `global` to read a global variable, but you need `global` if you want an assignment inside a function to modify that global variable.**

One subtle point: operations that mutate a **global mutable object** can work without `global`:

```python
numbers = [1, 2]

def test():
    numbers.append(3)

test()

print(numbers)
```

Output:

```python
[1, 2, 3]
```

Here you're not assigning a new object to `numbers`; you're **mutating the existing list**.
