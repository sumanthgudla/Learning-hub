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

