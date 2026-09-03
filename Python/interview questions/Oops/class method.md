## 6. Class Method — `@classmethod`

A **class method is a method that works with the class itself rather than a particular object**.

The key difference is:

```text
Instance method → self → object
Class method    → cls  → class
```

You create a class method using `@classmethod`.

### Basic example

```python
class Employee:
    company = "ABC"

    @classmethod
    def change_company(cls, new_company):
        cls.company = new_company
```

Now:

```python
Employee.change_company("XYZ")

print(Employee.company)
```

Output:

```text
XYZ
```

Here, `cls` refers to the `Employee` class.

Conceptually:

```python
Employee.change_company("XYZ")
```

becomes:

```python
Employee.change_company(Employee, "XYZ")
```

So:

```python
cls
```

is essentially:

```python
Employee
```

---

## Why do we need class methods?

Suppose we have:

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name
```

`name` belongs to an individual employee:

```text
emp1 → John
emp2 → Alice
```

So an **instance method** makes sense:

```python
def display(self):
    print(self.name)
```

But `company` belongs to the class:

```text
Employee
   ↓
company = ABC
```

So a **class method** makes sense:

```python
@classmethod
def change_company(cls, company):
    cls.company = company
```

---

## Instance method vs class method

### Instance method

```python
class Employee:
    def display(self):
        print(self.name)
```

Called using an object:

```python
emp.display()
```

Python passes:

```text
self → emp
```

---

### Class method

```python
class Employee:
    @classmethod
    def change_company(cls, company):
        cls.company = company
```

Can be called using the class:

```python
Employee.change_company("XYZ")
```

Python passes:

```text
cls → Employee
```

---

## Can we call a class method through an object?

Yes.

```python
emp = Employee("John")

emp.change_company("XYZ")
```

Python still passes the **class** as `cls`, not `emp`.

So:

```python
emp.change_company("XYZ")
```

effectively works like:

```python
Employee.change_company("XYZ")
```

The class method is associated with the class.

---

# Very important use case: Alternative Constructors

This is one of the **most important reasons to use class methods in Python**.

Suppose:

```python
class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age
```

Normally:

```python
emp = Employee("John", 30)
```

But maybe you receive employee data as a string:

```python
data = "John,30"
```

You can create a class method:

```python
class Employee:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @classmethod
    def from_string(cls, data):
        name, age = data.split(",")
        return cls(name, int(age))
```

Now:

```python
emp = Employee.from_string("John,30")

print(emp.name)
print(emp.age)
```

Output:

```text
John
30
```

Here `from_string()` is an **alternative way of constructing an Employee object**.

That's a very common real-world use of `@classmethod`.

---

## Why use `cls` instead of `Employee`?

You might wonder why we don't simply write:

```python
@classmethod
def from_string(cls, data):
    ...
    return Employee(name, int(age))
```

Instead we write:

```python
return cls(name, int(age))
```

This becomes important with **inheritance**.

If a subclass calls the method, `cls` can refer to the subclass.

That makes the class method more reusable.

---

# Interview answer

If they ask:

> **What is a class method?**

Say:

> "A class method is a method that receives the class as its first argument, conventionally called `cls`, rather than an instance. It is defined using `@classmethod` and is typically used when the operation needs to work with class-level data or when we need alternative constructors."

### Remember:

```text
Instance method
    ↓
self
    ↓
specific object

Class method
    ↓
cls
    ↓
class
```

Next is **static method (`@staticmethod`)**, where there is **neither `self` nor `cls`**.
