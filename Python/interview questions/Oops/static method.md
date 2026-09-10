## 7. Static Method — `@staticmethod`

A **static method is a method that belongs logically to a class, but does not need either the object (`self`) or the class (`cls`)**.

```python
class Employee:

    @staticmethod
    def is_valid_age(age):
        return age >= 18
```

Call it directly using the class:

```python
print(Employee.is_valid_age(25))
```

Output:

```text
True
```

There is **no `self`** and **no `cls`**.

---

### Why would we put this inside a class?

Because the function is logically related to the class.

For example:

```python
class Employee:

    @staticmethod
    def calculate_bonus(salary, percentage):
        return salary * percentage / 100
```

Usage:

```python
bonus = Employee.calculate_bonus(50000, 10)

print(bonus)
```

Output:

```text
5000.0
```

The calculation doesn't need:

```python
self.name
```

or:

```python
Employee.company
```

So it doesn't need an instance or class.

---

## Compare all three

This is **very important for interviews**:

```python
class Employee:

    def display(self):
        pass

    @classmethod
    def change_company(cls):
        pass

    @staticmethod
    def calculate_bonus(salary):
        pass
```

| Method          | First parameter | Works with |
| --------------- | --------------- | ---------- |
| Instance method | `self`          | Object     |
| Class method    | `cls`           | Class      |
| Static method   | None            | Neither    |

Think:

```text
Instance method
      ↓
    self
      ↓
   Employee object


Class method
      ↓
     cls
      ↓
 Employee class


Static method
      ↓
  no self / cls
      ↓
 just independent logic
```

---

## A realistic example

```python
class Employee:

    company = "ABC"

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    # Instance method
    def display(self):
        print(self.name, self.salary)

    # Class method
    @classmethod
    def change_company(cls, company):
        cls.company = company

    # Static method
    @staticmethod
    def calculate_bonus(salary):
        return salary * 0.10
```

Now:

```python
emp = Employee("John", 50000)
```

### Instance method

```python
emp.display()
```

Needs the **object**.

---

### Class method

```python
Employee.change_company("XYZ")
```

Needs the **class**.

---

### Static method

```python
Employee.calculate_bonus(50000)
```

Needs **neither**.

---

## Common interview question

### "Why not just make `calculate_bonus()` a normal function?"

You absolutely **could**:

```python
def calculate_bonus(salary):
    return salary * 0.10
```

That's perfectly valid.

A static method is useful when the function is **conceptually related to the class** and you want to organize that functionality under the class namespace.

So don't say:

> "Static methods are required when we don't need self."

Better answer:

> "A static method is useful for utility or helper logic that is logically associated with a class but doesn't need access to either instance state or class state."

---

## One subtle point

You can call a static method through an object:

```python
emp.calculate_bonus(50000)
```

It still doesn't receive `emp`.

That's different from an instance method.

```python
emp.display()
```

automatically passes `emp` as `self`.

But:

```python
emp.calculate_bonus(50000)
```

does **not** pass `emp` to the static method.

---

### Easy way to remember

```text
self → "I need this OBJECT"

cls  → "I need this CLASS"

none → "I need neither"
```

So:

**Instance → Class → Static**

is the progression we're learning.

Next up: **Inheritance** — this is where one class can reuse/extend another class.
