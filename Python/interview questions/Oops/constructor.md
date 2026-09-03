## 2. Constructor — `__init__`

A **constructor** is used to initialize an object when it is created.

In Python, you'll commonly see:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
```

Then:

```python
emp = Employee("John", 50000)
```

Python automatically calls:

```python
__init__(emp, "John", 50000)
```

So after creation:

```python
emp.name    # "John"
emp.salary  # 50000
```

### What is `self`?

This is very important for interviews.

When you write:

```python
emp = Employee("John", 50000)
```

Python creates an `Employee` object and passes that object as the first argument to `__init__`.

Conceptually:

```python
Employee.__init__(emp, "John", 50000)
```

Therefore:

```python
self.name = name
```

means:

> Store `"John"` inside the `name` attribute of **this particular object**.

---

### Let's see it with two objects

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary


emp1 = Employee("John", 50000)
emp2 = Employee("Alice", 60000)
```

Conceptually:

```text
emp1
 ├── name   → "John"
 └── salary → 50000

emp2
 ├── name   → "Alice"
 └── salary → 60000
```

The same `__init__` code runs for both objects, but `self` refers to a **different object** each time.

---

## Is `__init__` actually the constructor?

This is a common Python interview trick.

Strictly speaking:

* `__new__()` → **creates** the object
* `__init__()` → **initializes** the object

So technically, Python's object creation mechanism involves `__new__`, while `__init__` initializes the already-created object.

For most interviews, saying:

> "`__init__` is the constructor used to initialize an object"

is acceptable, but if they go deeper, mention `__new__`.

---

## What if we don't write `__init__`?

That's completely valid.

```python
class Employee:
    pass

emp = Employee()
```

Python can still create the object.

But you won't automatically have attributes like `name` or `salary`.

---

## Can we have our own constructor parameters?

Yes:

```python
class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Then:

```python
emp = Employee("John", 30)
```

But:

```python
emp = Employee()
```

will give an error because `name` and `age` are required.

---

### One thing to remember

```text
Employee("John", 50000)
        ↓
Object is created
        ↓
__init__() is called
        ↓
self.name = "John"
self.salary = 50000
```

### Interview answer

If they ask:

> **What is `__init__` in Python?**

Say:

> "`__init__` is a special method that is automatically called when an object is initialized. It is commonly used to initialize instance variables. The `self` parameter refers to the newly created instance."

---

**Next → Instance Variables** — this connects directly to `self.name` and `self.salary`, and it's important to understand why each object gets its own values.
