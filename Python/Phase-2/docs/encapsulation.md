Here's **Phase 2 — Topic 11: Encapsulation** in notes-friendly format:

---

# Phase 2 — Topic 11: Encapsulation (Private attrs, `@property`)

## What is it?
Encapsulation means **restricting direct access** to an object's internal data and exposing controlled access through methods. Python doesn't have true "private" like Java/C++ — it uses **naming conventions** and the `@property` decorator to achieve this. Senior devs must know exactly what Python enforces vs what's just convention.

---

## 1. Python's "Privacy" Levels — Convention, Not Enforcement

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner       = owner          # public — no convention
        self._balance    = balance         # protected — single underscore
        self.__pin       = "1234"          # private — double underscore


acc = BankAccount("Arjun", 1000)

# Public — freely accessible
print(acc.owner)         # Arjun

# Protected (_balance) — accessible but signals "internal use"
print(acc._balance)      # 1000  ← works! Python doesn't block this
                          # but tells other devs "don't touch unless necessary"

# Private (__pin) — name-mangled, harder to access
print(acc.__pin)         # ❌ AttributeError
print(acc._BankAccount__pin)   # "1234"  ← still accessible via mangled name!
```

---

## 2. Name Mangling — What `__` Actually Does

```python
class BankAccount:
    def __init__(self):
        self.__pin = "1234"

acc = BankAccount()

# Python renames __pin to _BankAccount__pin internally
print(acc.__dict__)
# {'_BankAccount__pin': '1234'}

# This is called NAME MANGLING
# Purpose: avoid accidental override in subclasses, NOT true security

class SecureBankAccount(BankAccount):
    def __init__(self):
        super().__init__()
        self.__pin = "9999"   # this becomes _SecureBankAccount__pin
                               # does NOT overwrite parent's _BankAccount__pin

acc2 = SecureBankAccount()
print(acc2.__dict__)
# {'_BankAccount__pin': '1234', '_SecureBankAccount__pin': '9999'}
# both exist separately — name mangling prevented collision
```

---

## 3. `@property` — Controlled Access (Getters)

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius     # protected — use property to access

    @property
    def radius(self):
        return self._radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2


c = Circle(5)
print(c.radius)    # 5        ← called like an ATTRIBUTE, not method()
print(c.area)      # 78.53975 ← computed on access, no () needed

# c.radius()    ❌ TypeError — radius is a property, not a method
# c.radius = 10 ❌ AttributeError — no setter defined yet
```

---

## 4. `@property.setter` — Controlled Writes with Validation

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius    # uses the SETTER below (validates input)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @property
    def area(self):
        return 3.14159 * self._radius ** 2


c = Circle(5)
print(c.radius)     # 5
print(c.area)       # 78.53975

c.radius = 10       # calls setter — validates
print(c.radius)     # 10
print(c.area)       # 314.159

c.radius = -5       # ❌ ValueError: Radius must be positive
```

---

## 5. `@property.deleter` — Controlled Deletion

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Radius must be positive")
        self._radius = value

    @radius.deleter
    def radius(self):
        print("Deleting radius...")
        del self._radius


c = Circle(5)
del c.radius       # Deleting radius...
print(c.radius)    # ❌ AttributeError — _radius no longer exists
```

---

## 6. Real World Example — Validated Attributes

```python
class Employee:
    def __init__(self, name, salary):
        self.name   = name
        self.salary = salary   # uses setter

    @property
    def salary(self):
        return self._salary

    @salary.setter
    def salary(self, value):
        if value < 0:
            raise ValueError("Salary cannot be negative")
        self._salary = value

    @property
    def annual_salary(self):       # computed, read-only property
        return self._salary * 12


emp = Employee("Arjun", 50000)
print(emp.salary)          # 50000
print(emp.annual_salary)   # 600000

emp.salary = 60000          # ✅ valid update
print(emp.salary)           # 60000

emp.salary = -1000           # ❌ ValueError

emp.annual_salary = 1000000  # ❌ AttributeError — no setter, read-only
```

---

## 7. Computed Properties — No Storage Needed

```python
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name  = last_name

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @full_name.setter
    def full_name(self, value):
        # allows: person.full_name = "Arjun Kumar"
        first, last = value.split(" ", 1)
        self.first_name = first
        self.last_name  = last


p = Person("Arjun", "Kumar")
print(p.full_name)         # Arjun Kumar  ← computed, not stored

p.full_name = "Priya Sharma"
print(p.first_name)        # Priya
print(p.last_name)         # Sharma
```

---

## 8. Why Use `@property` Instead of Methods?

```python
# WITHOUT property — old Java-style getters/setters
class Circle:
    def __init__(self, radius):
        self._radius = radius

    def get_radius(self):
        return self._radius

    def set_radius(self, value):
        if value <= 0:
            raise ValueError("Invalid radius")
        self._radius = value


c = Circle(5)
print(c.get_radius())    # 5       ← ugly, not Pythonic
c.set_radius(10)          # ugly


# WITH property — Pythonic, looks like simple attribute access
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Invalid radius")
        self._radius = value


c = Circle(5)
print(c.radius)    # 5    ← clean attribute syntax
c.radius = 10      # clean, but STILL validated behind the scenes


# KEY BENEFIT — you can START with a plain attribute
# and ADD validation LATER without breaking existing code
class Circle:
    def __init__(self, radius):
        self.radius = radius   # plain attribute initially

# later, upgrade to property — external code using c.radius
# doesn't need to change AT ALL
```

---

## 9. `__slots__` — Restricting Attributes (Senior Bonus)

```python
# Normal class — can add ANY attribute dynamically
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 99    # ✅ works — Python allows adding new attributes anytime
print(p.z)  # 99


# __slots__ — restricts which attributes are allowed
class Point:
    __slots__ = ["x", "y"]    # ONLY these attributes allowed

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
p.z = 99    # ❌ AttributeError — 'z' not in __slots__


# Why use __slots__?
# 1. Saves memory — no __dict__ created per instance
# 2. Prevents typos — p.naem = "x" would silently create wrong attr without slots
# 3. Slightly faster attribute access

import sys
class WithDict:
    def __init__(self, x): self.x = x

class WithSlots:
    __slots__ = ["x"]
    def __init__(self, x): self.x = x

print(sys.getsizeof(WithDict(1).__dict__))   # ~104 bytes (dict overhead)
# WithSlots has NO __dict__ — saves memory, especially with many instances
```

---

## Interview Questions They Actually Ask

**Q1: Does Python have true private variables like Java?**
> No. Python uses **convention** — single underscore `_var` means "internal use, don't touch" (not enforced). Double underscore `__var` triggers **name mangling** (`_ClassName__var`) which makes accidental access harder but is NOT true security — it's still accessible if you know the mangled name.

**Q2: What's the point of `@property` if Python doesn't enforce privacy?**
> `@property` lets you control HOW an attribute is accessed/modified — adding validation, computed values, logging, etc. — while keeping the **same attribute-access syntax** (`obj.attr` not `obj.get_attr()`). This means you can refactor a plain attribute into a property later without breaking any code that uses it.

**Q3: What happens if you define `@property` but no setter?**
> The property becomes **read-only**. Attempting `obj.prop = value` raises `AttributeError: can't set attribute`.

**Q4: Why does name mangling exist?**
> To prevent **accidental name collisions** in inheritance. If a subclass defines `self.__data` and the parent also has `self.__data`, name mangling (`_Parent__data` vs `_Child__data`) keeps them separate, avoiding silent overwrites.

**Q5: What's the difference between `_var` and `__var`?**
> `_var` (single underscore) is purely a **convention** — "protected", developers should treat it as internal but Python does nothing special. `__var` (double underscore, no trailing underscores) triggers **name mangling** — Python actually renames it internally.

---

## Practice Problems

**Beginner — `p2_t11_prac01_temperature.py`**
Create a `Temperature` class storing temperature in Celsius internally (`_celsius`). Add properties:
- `celsius` — getter/setter, setter validates `value >= -273.15` (absolute zero)
- `fahrenheit` — computed property (getter AND setter) that converts to/from celsius
```python
t = Temperature(25)
print(t.celsius)        # 25
print(t.fahrenheit)     # 77.0

t.fahrenheit = 32
print(t.celsius)        # 0.0

t.celsius = -300         # ❌ ValueError
```

---

**Senior level — `p2_t11_prac02_inventory_item.py`**
Create an `InventoryItem` class with:
- `_name`, `_price`, `_quantity` (all protected)
- `price` property — setter rejects negative values
- `quantity` property — setter rejects negative values
- `total_value` — read-only computed property (`price * quantity`)
- `__slots__` to restrict attributes
- Override `__repr__`
```python
item = InventoryItem("Widget", 10.5, 100)
print(item.total_value)    # 1050.0

item.price = -5            # ❌ ValueError
item.quantity = -1         # ❌ ValueError

item.discount = 0.1        # ❌ AttributeError — __slots__ restricts this
```

---

## Common Mistakes & Senior Traps

- **Thinking `__var` is truly private** — it's name-mangled, not hidden. `obj._ClassName__var` still works.
- **Forgetting `_` prefix for backing field** — `@property def radius(self): return self.radius` causes **infinite recursion** (property calling itself). Must use a different internal name like `self._radius`.
- **Adding setter when not needed** — if a value should never change after creation, don't add a setter — keep it read-only by design.
- **`__slots__` and inheritance** — if parent has `__slots__` but child doesn't define its own, child instances get a `__dict__` anyway, partially defeating the purpose. Every class in the hierarchy needs `__slots__` for full benefit.
- **Validating in `__init__` but not in setter** — if you validate only in `__init__`, later assignments (`obj.price = -5`) bypass validation. Always route through the property setter:
```python
def __init__(self, price):
    self.price = price   # ✅ goes through setter, gets validated
    # NOT: self._price = price  ← skips validation
```

---

Say **next** for Topic 12: File I/O!    