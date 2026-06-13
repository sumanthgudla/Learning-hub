Here's **Phase 2 — Topic 10: Dunder Methods** in notes-friendly format:

---

# Phase 2 — Topic 10: Dunder Methods (`__str__`, `__repr__`, `__len__`, etc.)

## What is it?
Dunder methods (double underscore, "magic methods") let your custom objects integrate with Python's built-in syntax and functions — `print()`, `len()`, `+`, `==`, `for` loops, and more. This is how Python achieves its "everything is consistent" feel. Senior devs use these to make custom classes behave like built-in types.

---

## 1. `__init__` and `__new__` — Object Creation

```python
# __new__ creates the object (rarely overridden)
# __init__ initializes it (commonly overridden)

class Point:
    def __new__(cls, *args, **kwargs):
        print("Creating instance...")
        return super().__new__(cls)

    def __init__(self, x, y):
        print("Initializing...")
        self.x = x
        self.y = y

p = Point(1, 2)
# Creating instance...
# Initializing...

# __new__ is used for: singletons, immutable types (str, int subclasses)
# 99% of the time you only need __init__
```

---

## 2. `__str__` vs `__repr__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"           # for users

    def __repr__(self):
        return f"Point({self.x}, {self.y})"      # for developers


p = Point(1, 2)
print(p)          # (1, 2)              ← __str__
print(str(p))     # (1, 2)              ← __str__
print(repr(p))    # Point(1, 2)         ← __repr__
print([p])        # [Point(1, 2)]       ← lists always use __repr__

# Rule: if __str__ is missing, Python falls back to __repr__
# ALWAYS define __repr__ at minimum
```

---

## 3. `__len__` — Make `len()` Work

```python
class Playlist:
    def __init__(self, songs):
        self.songs = songs

    def __len__(self):
        return len(self.songs)


playlist = Playlist(["Song A", "Song B", "Song C"])
print(len(playlist))   # 3  ← calls __len__ internally

# Without __len__:
# len(playlist)  → TypeError: object of type 'Playlist' has no len()
```

---

## 4. `__eq__`, `__lt__`, `__gt__` — Comparisons

```python
class Product:
    def __init__(self, name, price):
        self.name  = name
        self.price = price

    def __eq__(self, other):
        return self.price == other.price

    def __lt__(self, other):
        return self.price < other.price

    def __gt__(self, other):
        return self.price > other.price

    def __repr__(self):
        return f"Product({self.name}, {self.price})"


p1 = Product("Mouse",    500)
p2 = Product("Keyboard", 1500)

print(p1 == p2)   # False
print(p1 < p2)    # True
print(p1 > p2)    # False

# Now sorted() and max()/min() work automatically!
products = [p2, p1, Product("Monitor", 8000)]
print(sorted(products))
# [Product(Mouse, 500), Product(Keyboard, 1500), Product(Monitor, 8000)]

print(max(products))   # Product(Monitor, 8000)
```

---

## 5. `__add__`, `__sub__`, `__mul__` — Operator Overloading

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"


v1 = Vector(1, 2)
v2 = Vector(3, 4)

print(v1 + v2)    # Vector(4, 6)   ← calls __add__
print(v1 - v2)    # Vector(-2, -2) ← calls __sub__
print(v1 * 3)     # Vector(3, 6)   ← calls __mul__

# Full operator table:
# +  → __add__       -  → __sub__
# *  → __mul__        /  → __truediv__
# // → __floordiv__   %  → __mod__
# ** → __pow__
```

---

## 6. `__getitem__`, `__setitem__` — Indexing Like a List

```python
class Inventory:
    def __init__(self):
        self.items = {}

    def __getitem__(self, key):
        return self.items.get(key, 0)

    def __setitem__(self, key, value):
        self.items[key] = value

    def __delitem__(self, key):
        del self.items[key]


inv = Inventory()
inv["apples"] = 50          # calls __setitem__
print(inv["apples"])        # 50  ← calls __getitem__
print(inv["bananas"])       # 0   ← default, key doesn't exist
del inv["apples"]           # calls __delitem__
```

---

## 7. `__iter__` and `__next__` — Make a Custom Iterable

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self          # the object itself is the iterator

    def __next__(self):
        if self.current <= 0:
            raise StopIteration   # signals end of iteration
        self.current -= 1
        return self.current + 1


for num in Countdown(5):
    print(num)
# 5
# 4
# 3
# 2
# 1


# Now your object works with:
# for loops, list(), sum(), any built-in expecting iterables
print(list(Countdown(3)))   # [3, 2, 1]
```

---

## 8. `__call__` — Make Object Callable Like a Function

```python
class Multiplier:
    def __init__(self, factor):
        self.factor = factor

    def __call__(self, number):
        return number * self.factor


double = Multiplier(2)
print(double(5))      # 10   ← double is an object but used like a function!
print(double(10))     # 20

# Real use case — decorators are often classes with __call__
```

---

## 9. `__contains__` — Make `in` Work

```python
class Range:
    def __init__(self, start, end):
        self.start = start
        self.end   = end

    def __contains__(self, value):
        return self.start <= value <= self.end


r = Range(1, 10)
print(5 in r)      # True   ← calls __contains__
print(15 in r)     # False
```

---

## 10. `__enter__`, `__exit__` — Context Managers (preview)

```python
class FileManager:
    def __init__(self, filename, mode):
        self.filename = filename
        self.mode = mode

    def __enter__(self):
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()


with FileManager("test.txt", "w") as f:
    f.write("Hello")
# file automatically closed after the with block
# covered in depth in File I/O topic
```

---

## Complete Dunder Reference Table

| Dunder | Triggered By | Purpose |
|--------|-------------|---------|
| `__init__` | `ClassName()` | Initialize new object |
| `__str__` | `print(obj)`, `str(obj)` | Human-readable string |
| `__repr__` | `repr(obj)`, console | Developer string |
| `__len__` | `len(obj)` | Length |
| `__eq__` | `obj1 == obj2` | Equality |
| `__lt__` / `__gt__` | `obj1 < obj2` | Comparison |
| `__add__` | `obj1 + obj2` | Addition |
| `__getitem__` | `obj[key]` | Indexing/access |
| `__setitem__` | `obj[key] = val` | Index assignment |
| `__iter__` | `for x in obj` | Make iterable |
| `__next__` | `next(obj)` | Get next item |
| `__call__` | `obj()` | Make callable |
| `__contains__` | `x in obj` | Membership test |
| `__enter__`/`__exit__` | `with obj as x` | Context manager |

---

## Interview Questions They Actually Ask

**Q1: Why define `__repr__` even if you have `__str__`?**
> `__repr__` is used in many places `__str__` is not — inside lists/dicts (`print([obj])`), in the interactive console, and in debuggers. If `__str__` is missing, Python falls back to `__repr__`, but not the other way around. Always define `__repr__` at minimum; ideally make it `eval()`-able.

**Q2: What's the difference between `__eq__` and `is`?**
> `__eq__` defines value equality (`==`) — can be customized. `is` checks identity (same object in memory) — cannot be customized, always compares memory addresses.

**Q3: If you define `__eq__`, what else should you consider?**
> If you override `__eq__`, Python sets `__hash__` to `None` by default, making the object **unhashable** — can't be used in sets or as dict keys. If you need both, define `__hash__` too, based on the same fields used in `__eq__`.

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
    def __hash__(self):
        return hash((self.x, self.y))   # must match __eq__ fields
```

**Q4: What is `__call__` used for in real code?**
> Making instances behave like functions — useful for decorators, configurable function factories, and stateful callables (e.g., a class-based cache or rate limiter).

**Q5: What's the difference between `__getitem__` and `__iter__`?**
> `__getitem__` alone makes an object work with indexing (`obj[0]`) and Python can auto-iterate using sequential integer indices until `IndexError`. `__iter__`/`__next__` is the explicit iterator protocol — required for non-indexable iterables (like infinite sequences or custom traversal order).

---

## Practice Problems

**Beginner — `p2_t10_prac01_vector.py`**
Create a `Vector` class with `__init__(x, y)`, `__repr__`, `__add__`, `__sub__`, `__eq__`, and `__abs__` (returns magnitude `sqrt(x²+y²)`).
```python
v1 = Vector(3, 4)
v2 = Vector(1, 2)
print(v1 + v2)    # Vector(4, 6)
print(v1 - v2)    # Vector(2, 2)
print(abs(v1))    # 5.0
print(v1 == Vector(3, 4))   # True
```

---

**Senior level — `p2_t10_prac02_matrix.py`**
Create a `Matrix` class that wraps a 2D list and supports:
- `__getitem__` and `__setitem__` for `matrix[row][col]` style access (or `matrix[(row,col)]`)
- `__add__` for matrix addition
- `__mul__` for scalar multiplication
- `__str__` for pretty printing
- `__eq__` for comparing matrices
- `__iter__` to iterate over rows
```python
m1 = Matrix([[1, 2], [3, 4]])
m2 = Matrix([[5, 6], [7, 8]])

print(m1 + m2)
# [6, 8]
# [10, 12]

print(m1 * 2)
# [2, 4]
# [6, 8]

for row in m1:
    print(row)
# [1, 2]
# [3, 4]
```

---

## Common Mistakes & Senior Traps

- **`__eq__` without `__hash__`** — defining `__eq__` makes the class unhashable by default. If you need to use objects in sets/dicts, define `__hash__` too.
- **`__repr__` should be unambiguous** — ideally `eval(repr(obj))` recreates the object. `__str__` can be casual; `__repr__` should not be.
- **Forgetting `__iter__` returns an iterator** — `__iter__` must return an object with `__next__`. Often `return self` works if the class itself implements `__next__`.
- **`__next__` without `StopIteration`** — causes infinite loops in `for` statements. Always raise `StopIteration` when done.
- **Operator overloading asymmetry** — `v1 + v2` calls `v1.__add__(v2)`. If types differ and `__add__` returns `NotImplemented`, Python tries `v2.__radd__(v1)`. Forgetting this causes `TypeError` in mixed-type operations.

---

Say **next** for Topic 11: Encapsulation!