## 8. Inheritance

**Inheritance means one class can acquire the attributes and methods of another class.**

The existing class is called the **parent/base class**.

The new class is called the **child/derived class**.

### Simple example

```python
class Employee:
    def display(self):
        print("Employee")


class Developer(Employee):
    pass
```

Now:

```python
dev = Developer()

dev.display()
```

Output:

```text
Employee
```

Why?

Because `Developer` inherits from `Employee`.

```text
Employee
   ↑
   |
Developer
```

So `Developer` automatically gets `display()`.

---

## Why do we need inheritance?

Imagine we have different types of employees:

```text
Employee
   |
   ├── Developer
   ├── Manager
   └── Tester
```

All employees might have common behavior:

```python
class Employee:
    def login(self):
        print("Employee logged in")

    def logout(self):
        print("Employee logged out")
```

Instead of repeating the code:

```python
class Developer(Employee):
    pass


class Manager(Employee):
    pass


class Tester(Employee):
    pass
```

All three automatically get:

```python
login()
logout()
```

This gives us **code reuse**.

---

# Child class can add its own functionality

```python
class Employee:
    def login(self):
        print("Login")


class Developer(Employee):
    def write_code(self):
        print("Writing code")
```

Now:

```python
dev = Developer()

dev.login()
dev.write_code()
```

Output:

```text
Login
Writing code
```

So the child gets the parent's functionality **and can add its own**.

---

# Child class can also override a method

This is very important because it leads directly to **polymorphism**.

```python
class Employee:
    def work(self):
        print("Employee working")


class Developer(Employee):
    def work(self):
        print("Developer writing code")
```

Now:

```python
dev = Developer()
dev.work()
```

Output:

```text
Developer writing code
```

The child provides its own implementation of `work()`.

This is called **method overriding**.

We'll cover it separately in detail.

---

# Types of inheritance

Python supports several forms:

### 1. Single inheritance

One parent → one child.

```python
class A:
    pass

class B(A):
    pass
```

```text
A
↓
B
```

---

### 2. Multilevel inheritance

```python
class A:
    pass

class B(A):
    pass

class C(B):
    pass
```

```text
A
↓
B
↓
C
```

`C` can inherit functionality from both `B` and indirectly `A`.

---

### 3. Multiple inheritance

A class can inherit from multiple parents.

```python
class A:
    pass

class B:
    pass

class C(A, B):
    pass
```

```text
A     B
 \   /
   C
```

Python supports multiple inheritance.

This is where **MRO (Method Resolution Order)** becomes important. We'll get to that later.

---

## Interview answer

If asked:

> **What is inheritance?**

Say:

> "Inheritance is an OOP mechanism where a child class derives properties and behaviors from a parent class. It promotes code reuse and allows the child class to extend or override the parent's behavior."

Example:

```python
class Employee:
    def login(self):
        print("Login")


class Developer(Employee):
    def write_code(self):
        print("Writing code")
```

`Developer` inherits `login()` from `Employee` and adds `write_code()`.

---

### One important distinction

Inheritance is **not simply copying code**.

When we write:

```python
class Developer(Employee):
    pass
```

Python doesn't just copy-paste the methods from `Employee` into `Developer`.

When we access:

```python
dev.login()
```

Python performs **attribute/method lookup**, which eventually finds `login` in the parent class.

That lookup mechanism becomes especially important with **MRO** later.

---

Next → **Polymorphism**: the same method/interface can behave differently depending on the object.
