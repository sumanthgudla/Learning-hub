## 10. Encapsulation

**Encapsulation means bundling data and the methods that operate on that data together, while controlling how that data is accessed or modified.**

In Python, this is mainly done using **classes and access conventions**.

---

### Simple example

Suppose we have a bank account:

```python
class BankAccount:
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
```

Here:

```text
BankAccount
├── balance
├── deposit()
└── withdraw()
```

The data (`balance`) and operations (`deposit`, `withdraw`) are bundled together.

That's the first part of encapsulation.

---

## But what's the "control access" part?

Suppose we don't want users of the class to directly modify the balance:

```python
account.balance = -100000
```

That could create an invalid state.

We can use a **private-style attribute**:

```python
class BankAccount:
    def __init__(self, balance):
        self.__balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def get_balance(self):
        return self.__balance
```

Now:

```python
account = BankAccount(1000)

account.deposit(500)

print(account.get_balance())
```

Output:

```text
1500
```

The class controls how the balance is changed.

---

# What does `__balance` mean?

Python uses naming conventions and **name mangling**.

```python
self.__balance
```

is treated roughly as:

```text
_BankAccount__balance
```

So this:

```python
account.__balance
```

will normally fail:

```text
AttributeError
```

But importantly:

> Python doesn't provide true private fields in the same way as languages such as Java or C++.

Name mangling mainly prevents accidental access/name collisions; it isn't a security mechanism.

---

# Three common access conventions in Python

### 1. Public

```python
self.balance
```

Can be accessed normally:

```python
account.balance
```

---

### 2. Protected convention

```python
self._balance
```

A single `_` means:

> "This is intended for internal/subclass use."

Python doesn't technically prevent access.

You can still do:

```python
account._balance
```

---

### 3. Private-style

```python
self.__balance
```

Python performs name mangling.

```python
account.__balance
```

normally won't work.

---

## Why is encapsulation useful?

Imagine this:

```python
class BankAccount:
    def __init__(self):
        self.__balance = 0

    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount

    def withdraw(self, amount):
        if 0 < amount <= self.__balance:
            self.__balance -= amount
```

Now the class can enforce rules:

```text
          BankAccount
               |
       __balance = 1000
               |
       -----------------
       |               |
    deposit()       withdraw()
       |               |
    validation       validation
```

The caller doesn't directly manipulate the internal state.

---

# Encapsulation ≠ just "private variables"

This is an important interview point.

A weak answer would be:

> "Encapsulation means making variables private."

A better answer:

> **"Encapsulation means bundling data and the methods that operate on that data together, while controlling access to the internal state and protecting the object from invalid modifications."**

Python achieves this through:

* classes
* methods
* `_` and `__` naming conventions
* properties (`@property`) when appropriate

---

## Real-world analogy

Think about an ATM.

You don't directly manipulate the bank's database:

```text
❌ account.balance = 500000
```

Instead, you interact through controlled operations:

```text
Deposit
Withdraw
Check Balance
```

The internal implementation is hidden from you.

That's the idea behind encapsulation.

---

## Interview question: Encapsulation vs Abstraction

These two are often confused.

### Encapsulation

> **How do I protect/control the object's internal state?**

Example:

```python
self.__balance
```

### Abstraction

> **How do I hide unnecessary implementation details and expose only what the user needs?**

For example, you call:

```python
account.withdraw(500)
```

without needing to know how the withdrawal is internally implemented.

We'll cover **abstraction** next.
