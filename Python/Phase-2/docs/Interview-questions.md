*Q1: What is `self` and why is it needed?**
> `self` is a reference to the current instance. Python doesn't automatically know which object's data to use when a method is called — `self` makes it explicit. It's passed automatically by Python when you call `instance.method()`.

**Q2: What's the difference between class attribute and instance attribute?**
> Class attributes are defined on the class and **shared across all instances**. Instance attributes are defined in `__init__` using `self` and are **unique to each object**. If you set a class attribute via an instance, Python creates a new instance attribute that shadows the class attribute for that instance only.

**Q3: What's the difference between `__str__` and `__repr__`?**
> `__str__` is for **human-readable** output — used by `print()`. `__repr__` is for **developer/debugging** output — should ideally be a string that can recreate the object. If `__str__` is not defined, Python falls back to `__repr__`.

**Q4: What does `__dict__` contain?**
> `instance.__dict__` contains all **instance attributes** as a dictionary. `Class.__dict__` contains class attributes and methods. This is Python's internal namespace for the object.

**Q5: What's the difference between `@classmethod` and `@staticmethod`?**
> `@classmethod` receives the **class** as first argument (`cls`) — used for alternative constructors or factory methods. `@staticmethod` receives **nothing** automatically — it's a utility function that logically belongs to the class but doesn't need instance or class data.

Q6: why __str__ amd __repr__ two methods for the same purpose?

even they both serve the same purpose, 
__repr__ → for developers (debugging, logging)

Goal: unambiguous, ideally something you could paste back into Python to recreate the object
Called by the REPL, repr(), inside containers (lists, dicts)

__str__ → for end users (display, UI)

Goal: readable and human-friendly
Called by print(), str(), f-strings



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
