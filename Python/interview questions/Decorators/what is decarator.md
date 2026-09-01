A **decorator** is something that **adds behavior to an existing thing without changing the thing itself**. The exact meaning depends on the context.

### In Python programming (the most common meaning)

A decorator is a function that wraps another function to extend or modify its behavior.

For example:

```python
def greet():
    print("Hello!")

def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

greet = decorator(greet)

greet()
```

Output:

```
Before
Hello!
After
```

Python provides a cleaner syntax using `@`:

```python
def decorator(func):
    def wrapper():
        print("Before")
        func()
        print("After")
    return wrapper

@decorator
def greet():
    print("Hello!")

greet()
```

This does the same thing.

Decorators are commonly used for:

* Logging function calls
* Authentication and authorization
* Timing how long functions take
* Caching results
* Validating inputs

---

### In software design (Decorator Pattern)

The **Decorator Pattern** is a design pattern that lets you add features to an object dynamically instead of modifying its class.

For example:

* A plain coffee costs $2.
* Add milk → $2.50.
* Add whipped cream → $3.00.

Instead of creating classes like:

* `Coffee`
* `CoffeeWithMilk`
* `CoffeeWithMilkAndWhippedCream`

you "decorate" the coffee with additional features.

---

### In interior design

A decorator is a person who improves the appearance of a space by choosing:

* Furniture
* Paint colors
* Lighting
* Curtains
* Decorations

Unlike an architect or interior designer, a decorator usually doesn't change the building's structure.

---

If you meant **decorators in Python**, I can also explain:

* how the `@` syntax works,
* decorators with arguments,
* class decorators, or
* how decorators are implemented under the hood.
