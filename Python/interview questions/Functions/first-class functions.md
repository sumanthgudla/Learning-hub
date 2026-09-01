## First-Class Functions

In Python, **functions are first-class objects**.

This means you can treat a function **like any other value/object**.

You can:

1. Store a function in a variable
2. Pass a function as an argument
3. Return a function from another function
4. Store functions in a list/dictionary

---

### 1. Store a function in a variable

```python id="y0q8v2"
def greet():
    print("Hello")

x = greet

x()
```

Output:

```text
Hello
```

Notice:

```python
x = greet
```

We didn't use `()`.

* `greet` → the function itself
* `greet()` → calls the function

---

### 2. Pass a function as an argument

This is very common.

```python id="z6k1kq"
def square(x):
    return x * x

def apply_function(func, value):
    return func(value)

result = apply_function(square, 5)

print(result)
```

Output:

```text
25
```

Here:

```text
square → passed as an argument
5      → passed as a value
```

This is also why things like `map()` work:

```python id="xj1p7n"
numbers = [1, 2, 3]

result = map(square, numbers)
```

`map()` receives the `square` function.

---

### 3. Return a function

A function can also **return another function**.

```python id="e4yq2a"
def outer():
    def inner():
        print("Hello")

    return inner

func = outer()

func()
```

Output:

```text
Hello
```

`outer()` returns the `inner` function.

This concept is important for understanding **closures and decorators**.

---

### 4. Store functions in a collection

```python id="2gjxk4"
def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

operations = [add, multiply]

print(operations[0](2, 3))
print(operations[1](2, 3))
```

Output:

```text
5
6
```

---

### Why is this called "first-class"?

Because functions are treated like **ordinary values**.

For example, you can do:

```text
function → assign to variable
function → pass to another function
function → return from function
function → store in list/dictionary
```

### Interview answer ⭐

> **Python treats functions as first-class objects, meaning functions can be assigned to variables, passed as arguments, returned from other functions, and stored in collections.**

This concept is the foundation for **lambda functions, `map()`, `filter()`, callbacks, closures, and decorators**.
