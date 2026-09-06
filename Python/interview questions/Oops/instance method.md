## 5. Instance Method

An **instance method is a method that operates on a particular object**.

The key point is:

> **An instance method receives the object itself as its first parameter, usually called `self`.**

Example:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print(self.name, self.salary)
```

Here:

```python
def display(self):
```

is an **instance method**.

---

### What happens when we call it?

```python
emp1 = Employee("John", 50000)

emp1.display()
```

It looks like we're calling:

```python
emp1.display()
```

But conceptually Python does:

```python
Employee.display(emp1)
```

So `self` becomes `emp1`.

Inside:

```python
print(self.name, self.salary)
```

is effectively:

```python
print(emp1.name, emp1.salary)
```

Output:

```text
John 50000
```

---

## Why do we need `self`?

Imagine we have two employees:

```python
emp1 = Employee("John", 50000)
emp2 = Employee("Alice", 60000)
```

When we do:

```python
emp1.display()
```

Python needs to know:

> "Which employee's name and salary should I display?"

`self` answers that question.

```text
emp1.display()
      ↓
self = emp1
      ↓
self.name
      ↓
"John"
```

And:

```python
emp2.display()
```

means:

```text
self = emp2
```

So it prints Alice's information.

---

## Instance method can also modify the object

For example:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def increase_salary(self, amount):
        self.salary += amount
```

Now:

```python
emp = Employee("John", 50000)

emp.increase_salary(5000)

print(emp.salary)
```

Output:

```text
55000
```

Why?

Conceptually:

```python
Employee.increase_salary(emp, 5000)
```

Therefore:

```python
self.salary += amount
```

becomes:

```python
emp.salary += 5000
```

---

## Instance method vs normal function

Without a class:

```python
def increase_salary(employee, amount):
    employee["salary"] += amount
```

With OOP:

```python
class Employee:
    def increase_salary(self, amount):
        self.salary += amount
```

Instead of:

```python
increase_salary(emp, 5000)
```

we can say:

```python
emp.increase_salary(5000)
```

The behavior is attached to the object.

---

## Important interview question

### Why does an instance method need `self`?

A good answer:

> "`self` refers to the current instance. It allows the method to access and modify the attributes and other methods belonging to that particular object."

---

## One common mistake

You might write:

```python
class Employee:
    def display():
        print("Hello")
```

Then:

```python
emp = Employee()
emp.display()
```

You'll get an error because Python automatically passes `emp` to the method, but `display()` doesn't have a parameter to receive it.

Normally:

```python
def display(self):
```

---

### Remember the pattern

```python
emp.display()
```

is conceptually:

```python
Employee.display(emp)
```

That's the most important thing to understand about **instance methods**.

---

**Next → Class Method (`@classmethod`)**. This is where `cls` replaces `self`, and you'll see exactly when you'd use it instead of an instance method.
