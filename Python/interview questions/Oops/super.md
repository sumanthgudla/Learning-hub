## 13. `super()`

`super()` is used inside a child class to access the **next implementation in the inheritance hierarchy**.

Most commonly, that's the parent class.

### Simple example

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

---

## What exactly does `super()` do?

Inside:

```python
class Developer(Employee):

    def work(self):
        super().work()
```

`super()` gives you a proxy that starts method lookup **after `Developer` in the MRO**.

So conceptually:

```text
Developer
    ↓
super()
    ↓
Employee
    ↓
work()
```

That's why:

```python
super().work()
```

finds `Employee.work()` in this simple example.

---

# Why not just write `Employee.work(self)`?

You technically can:

```python
class Developer(Employee):
    def work(self):
        Employee.work(self)
```

But `super()` is generally better.

Why?

Because it works properly with **inheritance hierarchies and multiple inheritance**.

For example:

```python
class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        print("B")
        super().show()
```

This allows Python's MRO to determine what comes next rather than hard-coding `A`.

---

# `super()` is also commonly used in `__init__`

This is extremely important.

```python
class Employee:
    def __init__(self, name):
        self.name = name


class Developer(Employee):
    def __init__(self, name, language):
        super().__init__(name)
        self.language = language
```

Now:

```python
dev = Developer("John", "Python")
```

What happens?

First:

```python
super().__init__(name)
```

calls the parent initialization:

```python
Employee.__init__(self, name)
```

which creates:

```python
self.name = "John"
```

Then the child continues:

```python
self.language = "Python"
```

So the object has:

```text
Developer object
├── name     → John
└── language → Python
```

---

# Why is `super()` useful here?

Without `super()` you might duplicate the parent's initialization:

```python
class Developer(Employee):
    def __init__(self, name, language):
        self.name = name       # duplicated logic
        self.language = language
```

If `Employee.__init__()` later becomes:

```python
def __init__(self, name):
    self.name = name
    self.employee_id = generate_id()
```

your `Developer` class could miss that new initialization.

Using:

```python
super().__init__(name)
```

automatically reuses the parent's initialization logic.

---

# Important interview question

### Is `super()` always calling the parent?

**Not exactly.**

This is a good advanced point.

A better definition is:

> "`super()` returns a proxy object that delegates attribute/method lookup to the next class in the MRO."

In simple single inheritance:

```text
Developer → Employee
```

the next class is `Employee`, so it looks like "call the parent."

But with multiple inheritance:

```python
class A:
    def show(self):
        print("A")


class B(A):
    def show(self):
        print("B")
        super().show()


class C(A):
    def show(self):
        print("C")
        super().show()


class D(B, C):
    def show(self):
        print("D")
        super().show()
```

The MRO of `D` determines what `super()` finds next.

```python
print(D.__mro__)
```

Conceptually:

```text
D → B → C → A → object
```

So:

```python
D().show()
```

produces:

```text
D
B
C
A
```

That's why understanding `super()` naturally leads us to **MRO**.

---

## Interview answer

If asked:

> **What is `super()` in Python?**

Say:

> "`super()` returns a proxy that allows us to access the next implementation in the class's MRO. It's commonly used to reuse parent initialization or overridden methods without directly hard-coding the parent class."

### Remember this

```text
self
 ↓
current object

super()
 ↓
next class in MRO
```

And the key distinction:

```text
❌ super() = simply "parent"

✅ super() = "next class according to MRO"
```

**Next → MRO (Method Resolution Order)**. This is the last major OOP concept in your list, and we'll trace it step-by-step with multiple inheritance.
