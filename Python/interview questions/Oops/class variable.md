## 4. Class Variables

A **class variable belongs to the class itself**, rather than to one particular object.

Example:

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name
```

Here:

```python
company
```

is a **class variable**.

While:

```python
self.name
```

is an **instance variable**.

---

### Why use a class variable?

Suppose every employee belongs to the same company:

```python
class Employee:
    company = "ABC"

    def __init__(self, name):
        self.name = name
```

Create multiple objects:

```python
emp1 = Employee("John")
emp2 = Employee("Alice")
emp3 = Employee("Bob")
```

They can all access:

```python
print(emp1.company)  # ABC
print(emp2.company)  # ABC
print(emp3.company)  # ABC
```

There is no need to store `"ABC"` separately for every employee.

Conceptually:

```text
             Employee CLASS
                  |
            company = "ABC"
             /      |      \
           emp1    emp2    emp3
           John   Alice    Bob
```

The objects can access the class variable.

---

## Instance variable vs Class variable

```python
class Employee:
    company = "ABC"          # class variable

    def __init__(self, name, salary):
        self.name = name      # instance variable
        self.salary = salary  # instance variable
```

Now:

```python
emp1 = Employee("John", 50000)
emp2 = Employee("Alice", 60000)
```

Think:

```text
Class Employee
└── company = "ABC"

emp1
├── name = "John"
└── salary = 50000

emp2
├── name = "Alice"
└── salary = 60000
```

So:

|                            | Instance variable | Class variable                |
| -------------------------- | ----------------- | ----------------------------- |
| Belongs to                 | Object            | Class                         |
| Created with               | `self.x`          | Inside class, outside methods |
| Separate value per object? | Yes               | Normally shared               |
| Example                    | `self.name`       | `company`                     |

---

## Important interview trap ⚠️

What happens here?

```python
class Employee:
    company = "ABC"

emp1 = Employee()
emp2 = Employee()

emp1.company = "XYZ"

print(emp1.company)
print(emp2.company)
```

Output:

```text
XYZ
ABC
```

Why?

Because:

```python
emp1.company = "XYZ"
```

**doesn't modify the class variable.**

Instead, Python creates an **instance variable named `company` on `emp1`**.

Now conceptually:

```text
Employee class
└── company = "ABC"

emp1
└── company = "XYZ"   ← instance variable

emp2
└── no company        ← gets ABC from class
```

This is a very common interview question.

---

### What if we modify it through the class?

```python
class Employee:
    company = "ABC"

emp1 = Employee()
emp2 = Employee()

Employee.company = "XYZ"

print(emp1.company)
print(emp2.company)
```

Output:

```text
XYZ
XYZ
```

Because both objects are looking up `company` from the class.

---

## Another common example: counting objects

Class variables are useful when you want to maintain information shared across instances.

```python
class Employee:
    count = 0

    def __init__(self, name):
        self.name = name
        Employee.count += 1
```

Now:

```python
emp1 = Employee("John")
emp2 = Employee("Alice")
emp3 = Employee("Bob")

print(Employee.count)
```

Output:

```text
3
```

`count` belongs to the **class**, not to an individual employee.

---

### Interview answer

If they ask:

> **What is a class variable?**

Say:

> "A class variable is an attribute defined at the class level and is shared by instances unless an instance overrides it with an attribute of the same name. It's useful for data that logically belongs to the class rather than to individual objects."

---

### One thing to remember

```python
class Employee:
    company = "ABC"       # CLASS variable

    def __init__(self, name):
        self.name = name  # INSTANCE variable
```

**Class variable → shared/common information**

**Instance variable → object-specific information**

---

**Next → Instance Method.** This is where we'll understand exactly why methods have `self` and what happens when you call `emp.display()`.
