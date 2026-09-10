## 12. Method Overriding

**Method overriding happens when a child class provides its own implementation of a method that already exists in the parent class.**

This is closely connected to **inheritance and polymorphism**.

### Basic example

```python
class Employee:
    def work(self):
        print("Employee is working")


class Developer(Employee):
    def work(self):
        print("Developer is writing code")
```

Here, `Employee` has:

```python
work()
```

and `Developer` defines another:

```python
work()
```

So `Developer` **overrides** the parent's method.

---

### What happens when we call it?

```python
dev = Developer()

dev.work()
```

Output:

```text
Developer is writing code
```

Python looks for `work()` starting with the actual object's class:

```text
dev
 ↓
Developer
 ↓
work() found
 ↓
execute Developer.work()
```

It doesn't use `Employee.work()` because the child has its own implementation.

---

## Why is overriding useful?

Suppose we have:

```python
class Employee:
    def work(self):
        print("Doing general employee work")
```

Different employees can specialize it:

```python
class Developer(Employee):
    def work(self):
        print("Writing code")


class Tester(Employee):
    def work(self):
        print("Testing software")


class Manager(Employee):
    def work(self):
        print("Managing the team")
```

Now:

```python
employees = [
    Developer(),
    Tester(),
    Manager()
]

for employee in employees:
    employee.work()
```

Output:

```text
Writing code
Testing software
Managing the team
```

This is **polymorphism through method overriding**.

The same:

```python
employee.work()
```

produces different behavior.

---

# What if I want the parent's implementation too?

This is where **`super()`** comes in.

Suppose:

```python
class Employee:
    def work(self):
        print("Employee is working")


class Developer(Employee):
    def work(self):
        print("Developer is writing code")
        super().work()
```

Now:

```python
dev = Developer()
dev.work()
```

Output:

```text
Developer is writing code
Employee is working
```

`super()` allows the child to access the appropriate parent implementation.

We'll go into `super()` deeply next.

---

## Important interview distinction

### Overloading vs Overriding

These are often confused.

**Overriding:**

```python
class Parent:
    def show(self):
        print("Parent")


class Child(Parent):
    def show(self):
        print("Child")
```

Same method name, child replaces/specializes the parent's implementation.

Python does **not** support traditional method overloading by defining multiple methods with the same name and different parameter lists like Java/C++.

For example, this doesn't create two overloads:

```python
class Test:
    def add(self, a):
        ...

    def add(self, a, b):
        ...
```

The second `add()` replaces the first one.

---

## Interview answer

If asked:

> **What is method overriding?**

Say:

> "Method overriding occurs when a child class provides its own implementation of a method that is already defined in the parent class. It allows subclasses to specialize inherited behavior and is commonly used to achieve runtime polymorphism."

### Remember

```text
Inheritance
     ↓
Child gets parent's method

Overriding
     ↓
Child replaces/specializes that method

Polymorphism
     ↓
Same method call → different behavior
```

**Next → `super()`** — we'll understand exactly what `super()` means and why it isn't simply "call the parent class."
