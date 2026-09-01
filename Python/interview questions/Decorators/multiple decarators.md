Sure. Let's use a **very small example** and trace exactly what happens.

```python
def decorator1(func):
    def wrapper():
        print("Decorator 1 - Before")
        func()
        print("Decorator 1 - After")
    return wrapper


def decorator2(func):
    def wrapper():
        print("Decorator 2 - Before")
        func()
        print("Decorator 2 - After")
    return wrapper


@decorator1
@decorator2
def greet():
    print("Hello")


greet()
```

### Step 1 — Python reads the decorators

```python
@decorator1
@decorator2
def greet():
```

Python converts this to:

```python
greet = decorator1(decorator2(greet))
```

### Step 2 — `decorator2` runs first

```python
decorator2(greet)
```

Inside `decorator2`:

```python
def wrapper():
    print("Decorator 2 - Before")
    func()
    print("Decorator 2 - After")
```

It returns `wrapper`.

So now:

```text
greet → decorator2's wrapper
```

### Step 3 — `decorator1` receives that wrapper

Now:

```python
greet = decorator1(decorator2's wrapper)
```

So `decorator1` creates another wrapper.

Final structure:

```text
greet
  ↓
Decorator 1 wrapper
  ↓
Decorator 2 wrapper
  ↓
Original greet()
```

### Step 4 — We call `greet()`

```python
greet()
```

We're actually calling **Decorator 1's wrapper**.

It executes:

```python
print("Decorator 1 - Before")
```

Output:

```text
Decorator 1 - Before
```

Then:

```python
func()
```

Here `func` is **Decorator 2's wrapper**.

So it executes:

```text
Decorator 2 - Before
```

Then it calls its `func()`.

Now `func` is the **original `greet()`**:

```text
Hello
```

Then execution returns to Decorator 2:

```text
Decorator 2 - After
```

Then returns to Decorator 1:

```text
Decorator 1 - After
```

### Final output

```text
Decorator 1 - Before
Decorator 2 - Before
Hello
Decorator 2 - After
Decorator 1 - After
```

### Remember this

```python
@A
@B
def func():
```

means:

```python
func = A(B(func))
```

**Applied:** Bottom → Top
**Executed:** Outer → Inner → Back Out

```text
        A wrapper
       /         \
 Before A       After A
       |
       B wrapper
      /          \
 Before B       After B
       |
    func()
```

This execution flow is **very commonly asked in Python interviews**.
