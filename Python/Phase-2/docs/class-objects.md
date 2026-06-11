Here's **Phase 2 — Topic 8: Classes & Objects** in notes-friendly format:

---

# Phase 2 — Topic 8: Classes & Objects

## What is it?
A class is a **blueprint** for creating objects. An object is an **instance** of a class — it has its own data (attributes) and behaviors (methods). This is the foundation of Object Oriented Programming. Senior devs must understand not just syntax but how Python creates objects in memory, what `self` really is, and how `__init__` works.

---

## 1. Class vs Object — The Blueprint Analogy

```
Class  → blueprint of a house    → defined ONCE
Object → actual house built       → created MANY times

class Dog:     ← blueprint
    ...

dog1 = Dog()   ← actual object 1
dog2 = Dog()   ← actual object 2
# dog1 and dog2 are INDEPENDENT — separate memory
```

---

## 2. Basic Class Structure

```python
class Dog:
    # class attribute — shared by ALL instances
    species = "Canis familiaris"

    # __init__ — constructor — runs when object is created
    def __init__(self, name, age):
        # instance attributes — unique to EACH object
        self.name = name
        self.age  = age

    # instance method
    def bark(self):
        return f"{self.name} says Woof!"

    def describe(self):
        return f"{self.name} is {self.age} years old"


# Creating objects
dog1 = Dog("Bruno", 3)
dog2 = Dog("Max",   5)

# Accessing attributes
print(dog1.name)        # Bruno
print(dog2.name)        # Max

# Calling methods
print(dog1.bark())      # Bruno says Woof!
print(dog2.describe())  # Max is 5 years old

# Class attribute — same for all
print(dog1.species)     # Canis familiaris
print(dog2.species)     # Canis familiaris
```

---

## 3. What is `self`?

```python
# self is a reference to the CURRENT OBJECT
# Python passes it automatically — you never pass it manually

class Dog:
    def __init__(self, name):
        self.name = name      # self = the object being created

    def bark(self):
        return f"{self.name} says Woof!"
        # self = the object calling the method


dog1 = Dog("Bruno")
dog1.bark()
# Python translates this to:
# Dog.bark(dog1)  ← dog1 is passed as self automatically

# self is just a convention — you could name it anything
# but ALWAYS use self — it's a universal Python convention
class Dog:
    def bark(this):           # ✅ works but terrible practice
        return "Woof"


# self is NOT a keyword — it's just the first parameter name
```

---

## 4. `__init__` — The Constructor

```python
class Person:
    def __init__(self, name, age, city="Unknown"):
        #          ↑ self    ↑ required   ↑ default
        self.name = name
        self.age  = age
        self.city = city

        # can run logic in __init__
        if age < 0:
            raise ValueError("Age cannot be negative")

        # derived attributes
        self.is_adult = age >= 18


p1 = Person("Arjun", 22, "Vijayawada")
p2 = Person("Priya", 17)              # city defaults to "Unknown"

print(p1.is_adult)   # True
print(p2.is_adult)   # False


# __init__ does NOT return anything
# it only SETS UP the object
# return value is always None
```

---

## 5. Class Attributes vs Instance Attributes

```python
class Employee:
    company = "TechCorp"      # class attribute — shared
    count   = 0               # class attribute — tracks instances

    def __init__(self, name, salary):
        self.name   = name    # instance attribute — unique
        self.salary = salary  # instance attribute — unique
        Employee.count += 1   # modify class attribute via class name


e1 = Employee("Arjun", 50000)
e2 = Employee("Priya", 60000)

# Class attribute — same for all
print(e1.company)     # TechCorp
print(e2.company)     # TechCorp
print(Employee.count) # 2

# Instance attribute — unique per object
print(e1.name)        # Arjun
print(e2.name)        # Priya


# TRAP — modifying class attribute via instance
e1.company = "NewCorp"    # creates INSTANCE attribute for e1 only
print(e1.company)         # NewCorp  ← e1's own copy
print(e2.company)         # TechCorp ← class attribute unchanged
print(Employee.company)   # TechCorp ← class attribute unchanged
```

---

## 6. Methods — 3 Types

```python
class Circle:
    pi = 3.14159

    def __init__(self, radius):
        self.radius = radius

    # 1. Instance method — works with instance data
    def area(self):
        return Circle.pi * self.radius ** 2

    # 2. Class method — works with class data
    @classmethod
    def from_diameter(cls, diameter):
        #               ↑ cls = the class itself
        return cls(diameter / 2)   # creates new instance

    # 3. Static method — utility, no access to instance or class
    @staticmethod
    def is_valid_radius(r):
        return r > 0


# Instance method
c1 = Circle(5)
print(c1.area())                    # 78.53975

# Class method — alternative constructor
c2 = Circle.from_diameter(10)
print(c2.radius)                    # 5.0

# Static method
print(Circle.is_valid_radius(5))    # True
print(Circle.is_valid_radius(-1))   # False
```

---

## 7. `__str__` and `__repr__` — String Representation

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age


p = Person("Arjun", 22)
print(p)        # <__main__.Person object at 0x...>  ← not useful


# Add __str__ — for print() and str()
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age  = age

    def __str__(self):
        return f"Person(name={self.name}, age={self.age})"

    def __repr__(self):
        return f"Person('{self.name}', {self.age})"


p = Person("Arjun", 22)
print(p)        # Person(name=Arjun, age=22)  ← __str__
print(repr(p))  # Person('Arjun', 22)         ← __repr__


# __str__  → human readable    → for end users
# __repr__ → unambiguous       → for developers/debugging
#            ideally can be eval'd to recreate the object
```

---

## 8. Object Memory — How Python Creates Objects

```python
class Dog:
    def __init__(self, name):
        self.name = name

dog1 = Dog("Bruno")
dog2 = Dog("Max")

# Each object has its OWN namespace
print(dog1.__dict__)    # {'name': 'Bruno'}
print(dog2.__dict__)    # {'name': 'Max'}

# They are completely separate in memory
print(id(dog1))         # some memory address
print(id(dog2))         # different memory address
print(dog1 is dog2)     # False


# Methods are shared — stored on the CLASS not each object
# dog1.bark and dog2.bark point to the SAME function
print(dog1.bark)        # <bound method Dog.bark of <Dog object>>
```

---

## 9. Comparing Objects

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


p1 = Point(1, 2)
p2 = Point(1, 2)

# By default — compares IDENTITY (memory address)
print(p1 == p2)     # False ← different objects even with same values
print(p1 is p2)     # False

# Fix — define __eq__
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)     # True ← now compares values
```

---

## Interview Questions They Actually Ask

**Q1: What is `self` and why is it needed?**
> `self` is a reference to the current instance. Python doesn't automatically know which object's data to use when a method is called — `self` makes it explicit. It's passed automatically by Python when you call `instance.method()`.

**Q2: What's the difference between class attribute and instance attribute?**
> Class attributes are defined on the class and **shared across all instances**. Instance attributes are defined in `__init__` using `self` and are **unique to each object**. If you set a class attribute via an instance, Python creates a new instance attribute that shadows the class attribute for that instance only.

**Q3: What's the difference between `__str__` and `__repr__`?**
> `__str__` is for **human-readable** output — used by `print()`. `__repr__` is for **developer/debugging** output — should ideally be a string that can recreate the object. If `__str__` is not defined, Python falls back to `__repr__`.

**Q4: What does `__dict__` contain?**
> `instance.__dict__` contains all **instance attributes** as a dictionary. `Class.__dict__` contains class attributes and methods. This is Python's internal namespace for the object.

**Q5: What's the difference between `@classmethod` and `@staticmethod`?**
> `@classmethod` receives the **class** as first argument (`cls`) — used for alternative constructors or factory methods. `@staticmethod` receives **nothing** automatically — it's a utility function that logically belongs to the class but doesn't need instance or class data.

---

## Practice Problems

**Beginner — `p2_t08_prac01_bank_account.py`**
Create a `BankAccount` class with:
- Attributes: `owner`, `balance` (default 0)
- Methods: `deposit(amount)`, `withdraw(amount)`, `get_balance()`
- `withdraw` should print "Insufficient funds" if balance too low
- `__str__` should return `"Account[Arjun]: ₹5000"`

```python
acc = BankAccount("Arjun", 1000)
acc.deposit(500)
acc.withdraw(200)
print(acc)            # Account[Arjun]: ₹1300
acc.withdraw(5000)    # Insufficient funds
```

---

**Senior level — `p2_t08_prac02_student_registry.py`**
Create a `Student` class with:
- Instance attributes: `name`, `scores` (list)
- Class attribute: `all_students` (list of all created students)
- Methods: `add_score(score)`, `average()`, `grade()`
- Class method: `top_student()` — returns student with highest average
- `__str__` and `__repr__`

```python
s1 = Student("Arjun")
s2 = Student("Priya")

s1.add_score(85)
s1.add_score(90)
s2.add_score(92)
s2.add_score(88)

print(s1.average())         # 87.5
print(s1.grade())           # B
print(Student.top_student()) # Priya (90.0)
```

---

## Common Mistakes & Senior Traps

- **Mutable default in `__init__`** — same trap as functions:
```python
# WRONG
class Student:
    def __init__(self, name, scores=[]):   # ❌ shared across all instances!
        self.scores = scores

# RIGHT
class Student:
    def __init__(self, name, scores=None):
        self.scores = scores if scores is not None else []
```
- **Modifying class attribute via instance** — `instance.class_attr = value` creates a new instance attribute, it doesn't modify the class attribute. Use `ClassName.attr = value` to modify class attribute.
- **Forgetting `self`** — calling `self.method` without `()` returns the method object, not the result. `self.bark` ≠ `self.bark()`.
- **`__str__` must return a string** — returning anything else raises `TypeError`.
- **Comparing objects with `==`** — without `__eq__`, two objects with same data are NOT equal by default. Python compares memory addresses.

---

Say **next** for Topic 9: Inheritance!