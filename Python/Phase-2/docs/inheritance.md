Here's **Phase 2 — Topic 9: Inheritance** in notes-friendly format:

---

# Phase 2 — Topic 9: Inheritance

## What is it?
Inheritance lets a class (**child/subclass**) reuse code from another class (**parent/superclass**). The child gets all attributes and methods of the parent, and can add new ones or override existing ones. Senior devs are expected to deeply understand `super()`, method resolution order (MRO), and when inheritance is the wrong tool.

---

## 1. Basic Inheritance

```python
# Parent class
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

    def info(self):
        return f"I am {self.name}"


# Child class — inherits from Animal
class Dog(Animal):
    def speak(self):                        # OVERRIDE parent method
        return f"{self.name} says Woof!"


class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"


dog = Dog("Bruno")
cat = Cat("Whiskers")

print(dog.speak())   # Bruno says Woof!
print(cat.speak())   # Whiskers says Meow!
print(dog.info())    # I am Bruno  ← inherited from Animal, not overridden
```

---

## 2. `super()` — Call Parent's Methods

```python
class Animal:
    def __init__(self, name, sound):
        self.name  = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}"


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name, "Woof")   # call parent's __init__
        #     ↑
        # super() gives access to parent class
        # without hardcoding "Animal"

        self.breed = "Unknown"           # child's own attribute


dog = Dog("Bruno")
print(dog.speak())   # Bruno says Woof
print(dog.breed)     # Unknown


# Why use super() instead of Animal.__init__(self, ...)?
class Dog(Animal):
    def __init__(self, name):
        Animal.__init__(self, name, "Woof")   # works but hardcodes parent name
        # if parent class is renamed, this breaks
        # super() automatically uses correct parent
```

---

## 3. Extending Parent Methods

```python
class Employee:
    def __init__(self, name, salary):
        self.name   = name
        self.salary = salary

    def details(self):
        return f"Name: {self.name}, Salary: {self.salary}"


class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)    # reuse parent's init
        self.team_size = team_size

    def details(self):
        # EXTEND parent's method — call it AND add more
        base_info = super().details()
        return f"{base_info}, Team Size: {self.team_size}"


m = Manager("Arjun", 90000, 5)
print(m.details())
# Name: Arjun, Salary: 90000, Team Size: 5
```

---

## 4. Types of Inheritance

```python
# 1. Single Inheritance — one parent
class Animal: pass
class Dog(Animal): pass


# 2. Multiple Inheritance — multiple parents
class Flyable:
    def fly(self):
        return "Flying!"

class Swimmable:
    def swim(self):
        return "Swimming!"

class Duck(Flyable, Swimmable):    # inherits from BOTH
    pass

duck = Duck()
print(duck.fly())    # Flying!
print(duck.swim())   # Swimming!


# 3. Multilevel Inheritance — chain of inheritance
class Animal:
    def eat(self): return "Eating"

class Mammal(Animal):
    def walk(self): return "Walking"

class Dog(Mammal):
    def bark(self): return "Barking"

dog = Dog()
print(dog.eat())    # Eating   ← from Animal
print(dog.walk())   # Walking  ← from Mammal
print(dog.bark())   # Barking  ← from Dog


# 4. Hierarchical Inheritance — multiple children from one parent
class Animal: pass
class Dog(Animal): pass
class Cat(Animal): pass
class Bird(Animal): pass
```

---

## 5. Method Resolution Order (MRO)

```python
# When multiple parents have the SAME method
# which one gets called?

class A:
    def greet(self):
        return "Hello from A"

class B:
    def greet(self):
        return "Hello from B"

class C(A, B):    # A comes FIRST
    pass

c = C()
print(c.greet())   # Hello from A  ← A is checked first

# See the full resolution order
print(C.__mro__)
# (<class 'C'>, <class 'A'>, <class 'B'>, <class 'object'>)
# Python searches LEFT TO RIGHT in inheritance list


# Diamond Problem — classic interview question
class A:
    def greet(self):
        return "A"

class B(A):
    def greet(self):
        return "B"

class C(A):
    def greet(self):
        return "C"

class D(B, C):    # inherits from both B and C, which both inherit A
    pass

d = D()
print(d.greet())   # B  ← follows MRO: D -> B -> C -> A -> object
print(D.__mro__)
# (D, B, C, A, object)

# Python uses C3 Linearization algorithm to compute MRO
# guarantees: child before parent, left-to-right order preserved
```

---

## 6. `isinstance()` vs `type()`

```python
class Animal: pass
class Dog(Animal): pass

dog = Dog()

# isinstance — checks INHERITANCE chain too
print(isinstance(dog, Dog))      # True
print(isinstance(dog, Animal))   # True  ← Dog IS-A Animal
print(isinstance(dog, object))   # True  ← everything inherits object

# type — checks EXACT type only
print(type(dog) == Dog)          # True
print(type(dog) == Animal)       # False ← exact type doesn't match

# Senior rule — always use isinstance() for type checking
# type() == comparison breaks with inheritance
```

---

## 7. Overriding `__init__` — Common Patterns

```python
class Vehicle:
    def __init__(self, brand, wheels):
        self.brand  = brand
        self.wheels = wheels


# Pattern 1 — extend with super()
class Car(Vehicle):
    def __init__(self, brand, doors):
        super().__init__(brand, wheels=4)   # fixed wheels for cars
        self.doors = doors


car = Car("Toyota", 4)
print(car.brand)    # Toyota
print(car.wheels)   # 4
print(car.doors)    # 4


# Pattern 2 — completely override (no super call)
class SpecialCar(Vehicle):
    def __init__(self, brand):
        # doesn't call super().__init__()
        self.brand  = brand
        self.wheels = 3       # different setup entirely
        self.special = True
```

---

## 8. `abstract` Base Classes — Preview (Topic 11 covers fully)

```python
from abc import ABC, abstractmethod

class Shape(ABC):              # ABC = Abstract Base Class
    @abstractmethod
    def area(self):
        pass     # must be implemented by child


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


# Cannot instantiate abstract class directly
shape = Shape()        # ❌ TypeError — can't instantiate abstract class

circle = Circle(5)     # ✅ works — implements area()
print(circle.area())   # 78.53975


class Square(Shape):
    pass    # forgot to implement area()

square = Square()   # ❌ TypeError — abstract method not implemented
```

---

## Interview Questions They Actually Ask

**Q1: What is `super()` and why use it instead of calling the parent class directly?**
> `super()` returns a proxy object that delegates method calls to the parent class, following MRO. It avoids hardcoding parent class names — if the parent class is renamed or the inheritance hierarchy changes, code using `super()` still works correctly.

**Q2: What is Method Resolution Order (MRO)?**
> MRO is the order Python searches through a class hierarchy to find a method or attribute. For single inheritance it's straightforward — child then parent. For multiple inheritance, Python uses **C3 Linearization** which guarantees child-before-parent and preserves the left-to-right order of inheritance declaration.

**Q3: What's the Diamond Problem and how does Python solve it?**
> When a class inherits from two classes that both inherit from a common ancestor, there's ambiguity about which method to use. Python solves this with MRO/C3 linearization — `D(B, C)` where both B and C inherit A, the MRO is `D → B → C → A → object`, so B's version wins.

**Q4: `isinstance()` vs `type() ==` for checking class — which is correct?**
> `isinstance()` is correct because it respects inheritance — a `Dog` object is also an `Animal`. `type(x) == Animal` returns `False` for a `Dog` instance even though Dog IS an Animal. Always use `isinstance()`.

**Q5: When should you NOT use inheritance?**
> When the relationship isn't truly "IS-A". If you're inheriting just to reuse some methods but the classes aren't conceptually related, prefer **composition** — have one class contain an instance of another ("HAS-A" relationship). Overusing inheritance leads to fragile, tightly-coupled hierarchies.

```python
# Inheritance — IS-A relationship
class Dog(Animal): pass   # Dog IS-A Animal ✅

# Composition — HAS-A relationship (often better)
class Car:
    def __init__(self):
        self.engine = Engine()   # Car HAS-A Engine ✅
```

---

## Practice Problems

**Beginner — `p2_t09_prac01_shapes.py`**
Create a base class `Shape` with method `area()` returning 0. Create `Rectangle` and `Circle` subclasses that override `area()`. Create a list of shapes and print total area of all.
```python
shapes = [Rectangle(4, 5), Circle(3), Rectangle(2, 2)]
# print each shape's area, then total
```

---

**Senior level — `p2_t09_prac02_employee_hierarchy.py`**
Create an `Employee` base class with `name`, `base_salary`, and method `calculate_salary()`. Create `Manager` (adds bonus), `Developer` (adds overtime pay), and `TeamLead(Manager, Developer)` using multiple inheritance — handle MRO carefully so `calculate_salary()` combines both bonus and overtime correctly using `super()`.
```python
tl = TeamLead("Arjun", base_salary=50000, bonus=5000, overtime_hours=10, overtime_rate=200)
print(tl.calculate_salary())
# 50000 + 5000 (bonus) + 10*200 (overtime) = 57000
print(TeamLead.__mro__)
```

---

## Common Mistakes & Senior Traps

- **Forgetting `super().__init__()`** — child's `__init__` completely overrides parent's, so parent attributes never get set unless you call `super().__init__()`.
- **Diamond problem confusion** — with multiple inheritance, method resolution follows MRO not "intuitive" order. Always check `Class.__mro__` when debugging.
- **`type()` for type checking** — breaks polymorphism. Always use `isinstance()`.
- **Deep inheritance chains** — more than 2-3 levels becomes hard to follow ("god object" anti-pattern). Consider composition.
- **Overriding without calling super()** — if you override `__init__` but skip `super().__init__()`, parent's setup logic (validation, default attributes) never runs — subtle bugs.

---

Say **next** for Topic 10: Dunder Methods!