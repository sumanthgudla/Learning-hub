## 14. MRO — Method Resolution Order

This is the **last topic in your OOP list**.

MRO answers a simple question:

> **When a class inherits from multiple classes, which class should Python search first for a method?**

MRO = **Method Resolution Order**.

---

## Start with simple inheritance

```python
class A:
    def show(self):
        print("A")


class B(A):
    pass
```

If we do:

```python
b = B()
b.show()
```

Python searches:

```text
B → A → object
```

It doesn't find `show()` in `B`, so it looks in `A`.

We can see this using:

```python
print(B.__mro__)
```

Conceptually:

```text
B
↓
A
↓
object
```

---

# Now the interesting case: Multiple Inheritance

```python
class A:
    def show(self):
        print("A")


class B:
    def show(self):
        print("B")


class C(A, B):
    pass
```

Here:

```text
      A       B
       \     /
          C
```

Now:

```python
c = C()
c.show()
```

Which `show()` should Python use?

Python follows the MRO:

```text
C → A → B → object
```

Therefore:

```text
A
```

is printed.

You can check:

```python
print(C.__mro__)
```

---

# Why does MRO matter?

Consider this:

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

Now:

```python
print(D.__mro__)
```

The MRO is:

```text
D → B → C → A → object
```

Now call:

```python
D().show()
```

Let's trace it.

### Step 1

Python starts at `D`:

```text
D.show()
```

prints:

```text
D
```

Then:

```python
super().show()
```

moves to the **next class in MRO** → `B`.

---

### Step 2

`B.show()`:

```text
B
```

Then:

```python
super().show()
```

moves to the next class in MRO → `C`.

---

### Step 3

`C.show()`:

```text
C
```

Then:

```python
super().show()
```

moves to → `A`.

---

### Step 4

`A.show()`:

```text
A
```

Final output:

```text
D
B
C
A
```

This is why I emphasized earlier:

> `super()` doesn't simply mean "call my parent."

It means:

> **Continue method lookup according to the MRO.**

---

# How does Python calculate MRO?

Python uses an algorithm called **C3 linearization**.

For most interviews, you don't need to explain the complete mathematical algorithm unless they specifically ask.

You should know:

> Python uses C3 linearization to create a consistent MRO, especially for multiple inheritance.

The MRO has to satisfy certain rules, including preserving the order of parent classes where possible.

---

# Classic Diamond Problem

This is a very common interview question.

```text
       A
      / \
     B   C
      \ /
       D
```

Code:

```python
class A:
    def show(self):
        print("A")


class B(A):
    pass


class C(A):
    pass


class D(B, C):
    pass
```

The hierarchy is:

```text
       A
      / \
     B   C
      \ /
       D
```

What happens?

```python
D().show()
```

Python doesn't call `A` twice.

The MRO is:

```text
D → B → C → A → object
```

So `show()` is eventually found in `A`.

---

# How to check MRO

Two common ways:

### `__mro__`

```python
print(D.__mro__)
```

### `mro()`

```python
print(D.mro())
```

Both show the resolution order.

---

# MRO + `super()` — remember this combination

This is probably the most important thing from this topic:

```python
class D(B, C):
    def show(self):
        super().show()
```

Don't think:

```text
super()
 ↓
B
```

simply because `B` is the first parent.

Think:

```text
D
↓
MRO
↓
B
↓
C
↓
A
↓
object
```

`super()` moves to the **next class in that sequence**.

---

# Interview answer

If asked:

> **What is MRO in Python?**

Say:

> "MRO, or Method Resolution Order, defines the order in which Python searches classes for attributes and methods, especially when inheritance and multiple inheritance are involved. Python uses C3 linearization to calculate the MRO. We can inspect it using `ClassName.__mro__` or `ClassName.mro()`."

If they ask:

> **What does `super()` do in multiple inheritance?**

Say:

> "`super()` follows the MRO and delegates the method call to the next class in that resolution order. It doesn't necessarily mean the immediate parent."

---

# 🎯 Your complete OOP map

You've now covered everything you listed:

```text
CLASS
  ↓
OBJECT
  ↓
CONSTRUCTOR (__init__)
  ↓
INSTANCE VARIABLES
  ↓
CLASS VARIABLES
  ↓
INSTANCE METHODS
  ↓
CLASS METHODS
  ↓
STATIC METHODS
  ↓
INHERITANCE
  ↓
POLYMORPHISM
  ↓
ENCAPSULATION
  ↓
ABSTRACTION
  ↓
METHOD OVERRIDING
  ↓
super()
  ↓
MRO
```

The **next useful step** isn't another new concept. For your interview preparation, I'd recommend doing a **single Python program that uses all of these concepts together**, and then I'll ask you interview-style questions from that program.
