## LEGB / Scoping in Python

**LEGB** tells us the order Python follows when it looks for a variable.

**L → E → G → B**

1. **L — Local**
2. **E — Enclosing**
3. **G — Global**
4. **B — Built-in**

---

### 1. Local

A variable created **inside a function** is local to that function.

```python
def greet():
    name = "Sumanth"
    print(name)

greet()
```

`name` is local to `greet()`.

You cannot normally access it outside:

```python
print(name)  # NameError
```

---

### 2. Enclosing

This applies when you have a **function inside another function**.

```python
def outer():
    name = "Sumanth"

    def inner():
        print(name)

    inner()

outer()
```

`inner()` doesn't have `name` locally, so Python looks in the **enclosing function**, `outer()`.

```text
inner() → Local ❌
           ↓
        Enclosing ✅
```

---

### 3. Global

A variable defined outside all functions is global.

```python
name = "Sumanth"

def greet():
    print(name)

greet()
```

`greet()` doesn't have a local `name`, so Python looks in the global scope.

---

### 4. Built-in

If Python can't find the variable in local, enclosing, or global scope, it checks Python's **built-in names**.

```python
def test():
    print(len([1, 2, 3]))
```

Where does Python find `len`?

```text
Local       ❌
Enclosing   ❌
Global      ❌
Built-in    ✅
```

`len()` is a built-in Python function.

---

## Complete LEGB example

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)

    inner()

outer()
```

Output:

```text
local
```

Because Python searches:

```text
Local       → "local"       ✅
Enclosing   → "enclosing"
Global      → "global"
Built-in
```

It **stops at the first match**.

---

## What about modifying variables?

This is where `global` and `nonlocal` become important.

### `global`

If you want to modify a global variable inside a function:

```python
count = 10

def update():
    global count
    count = 20

update()

print(count)
```

Output:

```text
20
```

Without `global`, Python would treat `count` as a **local variable** when you assign to it.

---

### `nonlocal`

Used when you want to modify a variable from an **enclosing function**.

```python
def outer():
    count = 10

    def inner():
        nonlocal count
        count += 1

    inner()
    print(count)

outer()
```

Output:

```text
11
```

### Interview answer

> **LEGB is Python's variable name resolution rule: Local, Enclosing, Global, and Built-in. Python searches these scopes in that order and uses the first matching name it finds. `global` is used to modify a global variable from inside a function, while `nonlocal` is used to modify a variable in an enclosing function.**

**Easy memory trick:**

```text
L → Inside current function
E → Outer/nested function
G → Outside functions
B → Python built-ins
```
