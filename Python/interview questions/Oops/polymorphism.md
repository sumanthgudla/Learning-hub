## 9. Polymorphism

**Polymorphism literally means "many forms."**

In OOP, it means:

> **The same method/interface can produce different behavior depending on which object is using it.**

This is one of the most important OOP concepts for interviews.

---

## Simple example

Suppose we have different types of employees:

```python
class Developer:
    def work(self):
        print("Writing code")


class Tester:
    def work(self):
        print("Testing software")


class Manager:
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

Notice what happened.

We wrote only:

```python
employee.work()
```

We didn't write:

```python
if employee is Developer:
    ...
elif employee is Tester:
    ...
elif employee is Manager:
    ...
```

The **same call**:

```python
employee.work()
```

behaves differently depending on the actual object.

That's polymorphism.

---

# How does this work with inheritance?

Usually you'll see polymorphism together with **method overriding**.

```python
class Employee:
    def work(self):
        print("Employee working")


class Developer(Employee):
    def work(self):
        print("Developer writing code")


class Tester(Employee):
    def work(self):
        print("Tester testing software")
```

Now:

```python
employees = [
    Developer(),
    Tester()
]

for employee in employees:
    employee.work()
```

Output:

```text
Developer writing code
Tester testing software
```

The variable:

```python
employee
```

can refer to different types of objects.

Python determines which `work()` implementation to execute.

---

# Why is this useful?

Imagine you're building a payment system.

You have:

```text
Payment
   |
   ├── CreditCardPayment
   ├── UPIPayment
   └── PayPalPayment
```

Each payment type can implement:

```python
process_payment()
```

For example:

```python
class CreditCardPayment:
    def process_payment(self):
        print("Processing credit card")


class UPIPayment:
    def process_payment(self):
        print("Processing UPI")


class PayPalPayment:
    def process_payment(self):
        print("Processing PayPal")
```

Your application can simply do:

```python
def process(payment):
    payment.process_payment()
```

Then:

```python
process(CreditCardPayment())
process(UPIPayment())
process(PayPalPayment())
```

The caller doesn't need to know the internal implementation.

That's a major benefit of polymorphism:

> **The calling code can work with different object types through a common interface.**

---

# Python has another form: Duck Typing

Python doesn't always require inheritance for polymorphism.

For example:

```python
class Dog:
    def speak(self):
        print("Bark")


class Cat:
    def speak(self):
        print("Meow")
```

Neither inherits from a common class.

But:

```python
def make_sound(animal):
    animal.speak()
```

works:

```python
make_sound(Dog())
make_sound(Cat())
```

Output:

```text
Bark
Meow
```

Python basically says:

> "I don't care what type you are. If you have the required behavior, I can use you."

This is called **duck typing**.

The common phrase is:

> **"If it walks like a duck and quacks like a duck, treat it like a duck."**

---

# Very important distinction

Don't confuse **inheritance** and **polymorphism**.

### Inheritance

Answers:

> **"How can one class acquire behavior from another class?"**

```python
class Developer(Employee):
    pass
```

### Polymorphism

Answers:

> **"How can the same interface/method behave differently for different objects?"**

```python
employee.work()
```

Depending on the object:

```text
Developer → writes code
Tester    → tests software
Manager   → manages team
```

---

## Interview answer

If they ask:

> **What is polymorphism?**

A strong answer:

> "Polymorphism means that the same interface or method call can have different implementations depending on the object. In Python, this is commonly achieved through method overriding and duck typing. It allows client code to work with different object types without needing to know their specific implementation."

### Easy memory trick

```text
Inheritance
    ↓
"What do I inherit?"

Polymorphism
    ↓
"How does the same operation behave differently?"
```

---

Next → **Encapsulation**: how we control access to an object's data and keep its internal implementation protected.
