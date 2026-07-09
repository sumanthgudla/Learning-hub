# Dataclasses (Senior/Interview Level)

## 1. What is it

`@dataclass` (introduced in Python 3.7, PEP 557) is a class decorator that **auto-generates boilerplate methods** (`__init__`, `__repr__`, `__eq__`, and optionally `__lt__`, `__hash__`, `__post_init__`, etc.) based on class-level field annotations. At senior level this isn't just "less typing" — it's about understanding **field defaults, mutability, inheritance behavior, `__post_init__` for validation, `field()` for fine-grained control, and how dataclasses compare to alternatives** like `namedtuple`, `TypedDict`, attrs, and Pydantic. Interviewers use this topic to probe your understanding of Python's data modeling patterns and when each tool is the right one.

---

## 2. Core concepts table

| Concept | Description |
|---|---|
| `@dataclass` | Decorator that auto-generates `__init__`, `__repr__`, `__eq__` from annotated fields |
| `field()` | Fine-grained control over individual fields — defaults, factories, repr, compare, etc. |
| `default_factory` | Used in `field()` for mutable defaults (list, dict) — a new instance per object |
| `__post_init__` | Called automatically after `__init__` — used for validation or derived field computation |
| `frozen=True` | Makes instances immutable (sets `__setattr__`/`__delattr__` to raise) + enables `__hash__` |
| `eq=True` | Auto-generates `__eq__` based on all fields (default `True`) |
| `order=True` | Auto-generates `__lt__`, `__le__`, `__gt__`, `__ge__` for comparison/sorting |
| `repr=False` | Suppresses a field from appearing in `__repr__` (useful for passwords, tokens) |
| `compare=False` | Excludes a field from `__eq__` and ordering comparisons |
| `init=False` | Field is not included in `__init__` — set only in `__post_init__` |
| `KW_ONLY` | Sentinel marking all following fields as keyword-only in `__init__` |
| `dataclasses.asdict()` | Recursively converts a dataclass to a dict |
| `dataclasses.astuple()` | Recursively converts a dataclass to a tuple |
| `dataclasses.replace()` | Creates a new instance with some fields replaced (like `copy` but immutable-friendly) |
| `dataclasses.fields()` | Returns a tuple of `Field` objects — useful for introspection |
| `ClassVar` | Marks a field as a class-level variable — excluded from `__init__` entirely |

---

## 3. Syntax & code examples

### Basic usage

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p1 = Point(1.0, 2.0)
p2 = Point(1.0, 2.0)

print(p1)           # → Point(x=1.0, y=2.0)   (__repr__ auto-generated)
print(p1 == p2)     # → True                   (__eq__ compares all fields)
print(p1 is p2)     # → False                  (still different objects)

# Without @dataclass you'd need to write __init__, __repr__, __eq__ manually:
# def __init__(self, x, y): self.x = x; self.y = y  ... etc
```

### Common real-world pattern: defaults, `field()`, `__post_init__`, and `frozen`

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Order:
    order_id: int
    items: list = field(default_factory=list)   # CORRECT: fresh list per instance
    status: str = "pending"                     # fine for immutable defaults
    created_at: datetime = field(
        default_factory=datetime.now,
        repr=False,         # hide from __repr__ output
        compare=False       # exclude from __eq__ checks
    )
    _internal_notes: str = field(default="", repr=False, compare=False)

    def __post_init__(self):
        # Runs after __init__ — perfect for validation
        if self.order_id <= 0:
            raise ValueError(f"order_id must be positive, got {self.order_id}")
        self.status = self.status.lower()   # normalize on creation

o1 = Order(order_id=1, items=["apple", "banana"])
o2 = Order(order_id=1)
print(o1)           # → Order(order_id=1, items=['apple', 'banana'], status='pending')
print(o1 == o2)     # → True (created_at excluded from compare — different timestamps!)


# frozen=True — immutable dataclass (safe as dict key or set member)
@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

c = Coordinate(40.7128, -74.0060)
# c.lat = 0.0   # → raises FrozenInstanceError

coords = {c: "New York"}   # hashable because frozen=True enables __hash__
print(coords[Coordinate(40.7128, -74.0060)])  # → "New York"
```

### Senior-level / non-obvious usage: `order`, `KW_ONLY`, `ClassVar`, `replace()`, inheritance

```python
from dataclasses import dataclass, field, replace, fields, KW_ONLY
from typing import ClassVar

@dataclass(order=True)
class Employee:
    # order=True generates __lt__ etc. — comparison uses fields in declaration order
    # Put sort key FIRST if you want natural ordering to match it
    sort_index: float = field(init=False, repr=False)  # derived, not in __init__
    name: str = field(compare=False)    # excluded from ordering
    salary: float = 0.0

    # ClassVar — shared across all instances, excluded from __init__ and __repr__
    company: ClassVar[str] = "Acme Corp"

    # KW_ONLY sentinel — all fields after this must be passed as keyword args
    _: KW_ONLY
    department: str = "general"

    def __post_init__(self):
        self.sort_index = self.salary   # sort by salary

e1 = Employee(name="Alice", salary=90000, department="engineering")
e2 = Employee(name="Bob",   salary=75000, department="marketing")

print(sorted([e1, e2]))
# → [Employee(name='Bob', salary=75000.0, department='marketing'),
#    Employee(name='Alice', salary=90000.0, department='engineering')]

# replace() — immutable-friendly copy with overrides (like namedtuple._replace)
promoted = replace(e1, salary=110000)
print(promoted)   # → Employee(name='Alice', salary=110000.0, department='engineering')
print(e1.salary)  # → 90000.0  (original unchanged)


# Introspection with fields()
for f in fields(e1):
    print(f.name, "→", getattr(e1, f.name))
# → name → Alice
# → salary → 90000.0
# → department → engineering
# (sort_index is field with init=False, still shows up in fields())


# Dataclass inheritance — child inherits parent fields, appends its own
@dataclass
class Person:
    name: str
    age: int

@dataclass
class Manager(Person):
    reports: list = field(default_factory=list)
    # __init__ becomes: Manager(name, age, reports=[])

m = Manager(name="Carol", age=35, reports=["Dave", "Eve"])
print(m)  # → Manager(name='Carol', age=35, reports=['Dave', 'Eve'])
```

**ASCII view — how `@dataclass` generates methods:**

```
@dataclass
class Point:
    x: float          ← field annotation
    y: float = 0.0    ← field with default

        │
        │  @dataclass reads __annotations__ dict at class-creation time
        ▼

Auto-generates:
┌─────────────────────────────────────────────────────────┐
│ __init__(self, x: float, y: float = 0.0):               │
│     self.x = x                                          │
│     self.y = y                                          │
│     # if __post_init__ exists → self.__post_init__()    │
│                                                         │
│ __repr__(self):                                         │
│     return f"Point(x={self.x!r}, y={self.y!r})"        │
│                                                         │
│ __eq__(self, other):                                    │
│     if other.__class__ is self.__class__:               │
│         return (self.x, self.y) == (other.x, other.y)  │
│     return NotImplemented                               │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Internals / how it works

- `@dataclass` is a **class decorator** that runs at class definition time. It inspects `cls.__annotations__` (an ordered dict of `{field_name: type}`) to discover fields, then **dynamically generates method source code as strings** and `exec()`s them into the class namespace — you can see this by reading CPython's `dataclasses.py` source. This is different from metaclasses; it's a post-hoc mutation of the class object.
- Fields are stored as `Field` objects in `cls.__dataclass_fields__` (a dict). Each `Field` carries metadata: `name`, `type`, `default`, `default_factory`, `repr`, `compare`, `init`, `hash`, `metadata`.
- **Mutable default trap**: Python evaluates default values at class definition time, not at instance creation time. Writing `items: list = []` would share one list object across all instances — the same bug as mutable default arguments in functions. `field(default_factory=list)` fixes this by calling `list()` fresh for each new instance inside the generated `__init__`.
- `frozen=True` works by injecting `__setattr__` and `__delattr__` methods that raise `FrozenInstanceError` — it does **not** use `__slots__` or any C-level trick; it's just runtime attribute assignment interception. This means `frozen` dataclasses have a small performance overhead on attribute access vs slots classes.
- `__hash__` logic follows a specific table: if `eq=True` and `frozen=False`, `__hash__` is set to `None` (making instances unhashable, preventing accidental dict key use on mutable objects). If `frozen=True`, `__hash__` is auto-generated from all fields marked `compare=True`. You can override with `unsafe_hash=True` to force hash generation on mutable dataclasses — but this is explicitly "unsafe" because mutating the object changes its hash, breaking dict/set invariants.
- `__post_init__` is called at the very end of the generated `__init__`, after all fields are set. If you have `field(init=False)` fields that depend on other fields, `__post_init__` is the right place to set them — the generated `__init__` will pass `InitVar` fields as arguments to `__post_init__` rather than setting them as attributes.

---

## 5. Interview questions

**Q1: Why can't you use a mutable default like `items: list = []` in a dataclass, and how does `field(default_factory=...)` solve it?**
A: Default values in `@dataclass` are evaluated **once at class definition time** — just like mutable default arguments in functions. Writing `items: list = []` would store a single list object in the `Field` metadata, and every instance would share that same list — mutating one would mutate all. `field(default_factory=list)` stores a *callable* instead of a value; the generated `__init__` calls `default_factory()` fresh for every new instance, producing a separate list each time. This is actually enforced: `@dataclass` raises `ValueError` at class-creation time if you pass a `list`, `dict`, or `set` directly as a default without `field()`.

**Q2: What's the relationship between `eq`, `frozen`, and `__hash__` in dataclasses?**
A: Python's data model says: if two objects compare equal, they must have the same hash. `@dataclass` enforces this by following a decision table: if `eq=True` (default) and `frozen=False` (default, mutable), it sets `__hash__ = None` — making instances **unhashable** — to prevent hash/equality inconsistency from mutation. If `frozen=True`, it auto-generates `__hash__` from the same fields used in `__eq__`. If `eq=False`, `__hash__` is inherited from the parent class. `unsafe_hash=True` bypasses this safety net, generating a hash on a mutable class — "unsafe" because mutating an instance after inserting it into a set/dict will corrupt the data structure.

**Q3: What does `__post_init__` do, and what are its use cases vs putting logic in `__init__` directly?**
A: `__post_init__` is called automatically at the end of the generated `__init__`, after all fields are set. You can't override `__init__` directly in a dataclass without losing the auto-generation — `__post_init__` is the designated hook. Use cases: field validation (`if self.age < 0: raise ValueError`), deriving computed fields from other fields (`self.full_name = f"{self.first} {self.last}"`), and setting `init=False` fields that depend on other fields. `InitVar[T]` is a companion feature — annotating a field as `InitVar[str]` passes it to `__post_init__` as an argument without storing it as an instance attribute, useful for constructor-only parameters like a database connection used to populate other fields.

**Q4: How does dataclass inheritance work, and what's the "non-default argument follows default argument" pitfall?**
A: Child dataclasses inherit all parent fields (in parent-first order), then append their own. The generated `__init__` has the combined signature. The pitfall: if a parent dataclass has a field with a default value, and a child adds a field **without** a default, Python's `__init__` would have a non-default argument after a default argument — which is a `TypeError`. The fix is to give the child's field a default too, or use `field(default=...)`, or restructure the hierarchy so fields without defaults always come first.
```python
@dataclass
class Parent:
    x: int = 0      # has default

@dataclass
class Child(Parent):
    y: int          # NO default → TypeError: non-default argument 'y' follows default argument
    # Fix: y: int = 0, OR restructure so Parent has no defaults if Child needs non-defaults
```

**Q5: When would you choose a dataclass over a `namedtuple`, `TypedDict`, or Pydantic model?**
A: `namedtuple` — use for simple, immutable, positional data; works anywhere tuples do (unpacking, indexing); but no mutation, no methods, no defaults easily. `dataclass` — use for structured mutable (or optionally immutable with `frozen`) data objects with behavior, defaults, validation via `__post_init__`, and inheritance; no runtime type enforcement. `TypedDict` — use purely for type-hint annotations on plain dicts; no class instances, no enforcement, just static analysis. `Pydantic` — use when you need **runtime type validation and coercion** (e.g., API request parsing, config loading); it validates and converts types automatically, at the cost of a dependency and some overhead. Senior answer: for internal data containers with known structure → dataclass; for API boundaries with external data → Pydantic.

---

## 6. Practice problems

**Beginner:**
Create a `@dataclass` called `Book` with fields: `title: str`, `author: str`, `pages: int`, and `rating: float = 0.0`. Add `__post_init__` validation that raises `ValueError` if `rating` is not between 0.0 and 5.0, or if `pages` is not positive. Create two `Book` instances and demonstrate `==` comparison, `repr`, and `replace()` to create a corrected copy of a book with a wrong rating.
- Suggested filename: `dataclasses_prac01_book.py`
- Input: `Book("Dune", "Herbert", 412, 4.8)` → repr shows all fields; invalid rating raises `ValueError`

**Senior:**
Model a small **e-commerce order system** using a dataclass hierarchy:

1. `@dataclass(frozen=True) class SKU` — `code: str`, `name: str`, `unit_price: float`
2. `@dataclass class LineItem` — `sku: SKU`, `quantity: int`, `discount: float = 0.0`; add a `@property` `subtotal` that computes `sku.unit_price * quantity * (1 - discount)`
3. `@dataclass class Order` — `order_id: int`, `customer: str`, `line_items: list[LineItem] = field(default_factory=list)`, `status: str = "pending"`; add methods: `add_item(sku, qty, discount)`, `total()` (sum of all subtotals), `to_dict()` using `dataclasses.asdict()`
4. Make `Order` sortable by `total()` using `order=True` and a `sort_index` field set in `__post_init__`... but note the problem with this approach (sort key is stale after adding items) and explain in a comment how you'd fix it.
5. Use `dataclasses.replace()` to create a "shipped" copy of a completed order without mutating the original.

- Suggested filename: `dataclasses_prac02_order_system.py`
- Test: build an order with 3 line items, print total, convert to dict, create a shipped copy.

---

## 7. Common mistakes & senior traps

- **Using mutable defaults directly** — the single most common dataclass mistake; `@dataclass` raises `ValueError` at class time to catch it, but people still try.
  ```python
  # WRONG
  @dataclass
  class Bag:
      items: list = []       # → ValueError: mutable default not allowed

  # RIGHT
  @dataclass
  class Bag:
      items: list = field(default_factory=list)
  ```

- **Forgetting that `frozen=True` doesn't deep-freeze** — a frozen dataclass prevents reassigning attributes, but if a field holds a mutable object (like a list), that object can still be mutated.
  ```python
  @dataclass(frozen=True)
  class Frozen:
      items: list = field(default_factory=list)

  f = Frozen()
  # f.items = []        # → FrozenInstanceError (can't reassign)
  f.items.append(1)     # → works fine! The list itself is mutable
  ```

- **Inheritance ordering causing `TypeError`** — parent with defaults, child with non-defaults breaks `__init__` signature (as described in Q4 above).

- **Expecting `@dataclass` to enforce types at runtime** — it does NOT. `Point(x="hello", y=None)` works fine at runtime; annotations are metadata only. Use Pydantic if you need runtime validation.

- **Overriding `__init__` directly** in a dataclass — this silently bypasses all auto-generation, `__post_init__` won't be called, and `field()` defaults won't be applied correctly.
  ```python
  # WRONG — defeats the whole point
  @dataclass
  class Bad:
      x: int
      def __init__(self, x):   # overrides generated __init__
          self.x = x           # __post_init__ never called

  # RIGHT — use __post_init__ for extra logic
  @dataclass
  class Good:
      x: int
      def __post_init__(self):
          if self.x < 0:
              raise ValueError("x must be positive")
  ```

- **Confusing `ClassVar` with regular fields** — a `ClassVar[T]` annotation tells `@dataclass` to skip that attribute entirely (not in `__init__`, `__repr__`, or `__eq__`). Forgetting `ClassVar` makes a shared class attribute appear as an instance field in the constructor.

- **Using `dataclasses.asdict()` on dataclasses containing non-serializable fields** (like `datetime` objects) and then trying to pass straight to `json.dumps()` — `asdict()` recursively converts nested dataclasses but doesn't handle non-JSON-serializable types; you still need a custom serializer.

---

Say **"next"** when you're ready for **Standard Library**, or ask for more practice problems on dataclasses first.