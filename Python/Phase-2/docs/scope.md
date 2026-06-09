Here's **Phase 2 — Topic 6: Scope & Closures** in notes-friendly format:

---

# Phase 2 — Topic 6: Scope & Closures

## What is it?
Scope defines **where a variable is accessible**. Closure is when an inner function **remembers variables from its enclosing function** even after that outer function has finished running. These are heavily tested at senior level because they underpin decorators, callbacks, and factory functions.

---

## 1. LEGB Rule — 4 Levels of Scope

```
L — Local      → inside current function
E — Enclosing  → inside outer function (closures)
G — Global     → module level
B — Built-in   → Python's built-in names (len, print, range...)

Python searches in this exact order: L → E → G → B
```

```python
# Built-in
print(len([1, 2, 3]))   # len is built-in scope

# Global
x = "global"

def outer():
    x = "enclosing"     # enclosing scope

    def inner():
        x = "local"     # local scope
        print(x)        # L → found here → "local"

    inner()
    print(x)            # L → not here, E → found → "enclosing"

outer()
print(x)                # L → not here, E → not here, G → "global"
```

---

## 2. Local Scope

```python
def my_func():
    x = 10          # local variable — only exists inside my_func
    print(x)        # 10

my_func()
print(x)            # ❌ NameError — x doesn't exist outside
```

---

## 3. Global Scope + `global` Keyword

```python
count = 0           # global variable

def increment():
    global count    # tells Python — use the GLOBAL count
    count += 1      # modifies global count

increment()
increment()
print(count)        # 2


# Without global keyword
count = 0

def increment():
    count += 1      # ❌ UnboundLocalError
    # Python sees count on left side of +=
    # assumes it's local — but it's not assigned yet locally

# Why this happens:
def increment():
    print(count)    # ✅ reading global is fine without global keyword
    count += 1      # ❌ modifying needs global keyword
```

---

## 4. Enclosing Scope + `nonlocal` Keyword

```python
def outer():
    count = 0           # enclosing variable

    def inner():
        nonlocal count  # tells Python — use ENCLOSING count
        count += 1      # modifies enclosing count
        print(count)

    inner()   # 1
    inner()   # 2
    inner()   # 3

outer()


# Without nonlocal
def outer():
    count = 0

    def inner():
        count += 1      # ❌ UnboundLocalError — same problem as global
    inner()
```

---

## 5. Closures — The Core Concept

```python
# A closure is created when:
# 1. There is a nested function (function inside function)
# 2. The inner function uses a variable from outer function
# 3. The outer function RETURNS the inner function

def make_multiplier(factor):    # outer function
    def multiply(number):       # inner function
        return number * factor  # uses factor from enclosing scope
    return multiply             # returns inner function — NOT calling it


# Create closures
double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))    # 10
print(triple(5))    # 15
print(double(10))   # 20

# factor=2 and factor=3 are REMEMBERED even though
# make_multiplier() has already finished running
```

---

## 6. How Closures Remember Variables

```python
def make_multiplier(factor):
    def multiply(number):
        return number * factor
    return multiply

double = make_multiplier(2)

# The closure stores the variable in __closure__
print(double.__closure__)
# (<cell at 0x...: int object at 0x...>,)

print(double.__closure__[0].cell_contents)
# 2  ← factor is stored here

# Each closure has its OWN copy of the variable
double = make_multiplier(2)
triple = make_multiplier(3)

print(double.__closure__[0].cell_contents)  # 2
print(triple.__closure__[0].cell_contents)  # 3
```

---

## 7. Closure Trap — Loop Variable Capture

```python
# CLASSIC INTERVIEW TRAP

# WRONG — all closures share the SAME variable i
funcs = []
for i in range(5):
    def func():
        return i        # captures i by REFERENCE not by VALUE
    funcs.append(func)

print([f() for f in funcs])
# [4, 4, 4, 4, 4]  ← all return 4 (last value of i)
# WHY — all functions point to the SAME i
# by the time you call them, loop is done and i=4


# FIX 1 — default argument captures value at definition time
funcs = []
for i in range(5):
    def func(i=i):      # i=i captures current value of i
        return i
    funcs.append(func)

print([f() for f in funcs])
# [0, 1, 2, 3, 4]  ✅


# FIX 2 — use a factory function
def make_func(i):
    def func():
        return i        # i is now in enclosing scope — fixed
    return func

funcs = [make_func(i) for i in range(5)]
print([f() for f in funcs])
# [0, 1, 2, 3, 4]  ✅
```

---

## 8. Real World Closure Use Cases

```python
# Use case 1 — Counter factory
def make_counter(start=0):
    count = [start]         # list so nonlocal not needed (mutable)

    def counter():
        count[0] += 1
        return count[0]

    return counter

counter1 = make_counter()
counter2 = make_counter(10)

print(counter1())   # 1
print(counter1())   # 2
print(counter2())   # 11
print(counter1())   # 3  ← independent from counter2


# Use case 2 — Memoization (caching)
def make_memoized(func):
    cache = {}

    def memoized(n):
        if n not in cache:
            cache[n] = func(n)
        return cache[n]

    return memoized

def slow_square(n):
    return n ** 2

fast_square = make_memoized(slow_square)
print(fast_square(4))   # 16  ← computed
print(fast_square(4))   # 16  ← from cache


# Use case 3 — Partial application
def make_adder(n):
    def add(x):
        return x + n
    return add

add5  = make_adder(5)
add10 = make_adder(10)

print(add5(3))    # 8
print(add10(3))   # 13
```

---

## 9. Scope of Comprehensions

```python
# Python 3 — comprehensions have their OWN scope
x = 10
result = [x for x in range(5)]
print(x)    # 10  ← x not leaked — comprehension scope is isolated

# Python 2 — comprehension leaked into outer scope
# x would be 4 after the comprehension
# this is a common cross-version interview question
```

---

## Interview Questions They Actually Ask

**Q1: What is the LEGB rule?**
> Python resolves variable names in this order: **L**ocal → **E**nclosing → **G**lobal → **B**uilt-in. It searches each scope in order and uses the first match it finds.

**Q2: What is a closure?**
> A closure is an inner function that remembers variables from its enclosing scope even after the outer function has finished executing. The variables are stored in the function's `__closure__` attribute.

**Q3: What's the difference between `global` and `nonlocal`?**
```python
x = 0
def outer():
    x = 0
    def inner():
        global x    # refers to MODULE level x
        nonlocal x  # refers to ENCLOSING function's x
```

**Q4: What does this print and why?**
```python
funcs = [lambda: i for i in range(5)]
print([f() for f in funcs])
```
> `[4, 4, 4, 4, 4]` — all lambdas capture `i` by reference. When called, `i` is already 4 (loop finished).

**Q5: When would you use a closure over a class?**
> When you need to maintain state with a **single behavior** — closure is simpler. When you need **multiple methods or behaviors**, use a class. Closures are lighter weight but less explicit.

---

## Practice Problems

**Beginner — `p2_t06_prac01_counter.py`**
Write a `make_counter` function that returns a counter function. Each call increments and returns the count. Support optional `step` parameter.
```python
c1 = make_counter()
c2 = make_counter(step=5)

print(c1())   # 1
print(c1())   # 2
print(c2())   # 5
print(c2())   # 10
print(c1())   # 3  ← independent
```

---

**Senior level — `p2_t06_prac02_validator_factory.py`**
Write a closure factory `make_validator` that returns a validator function. Each validator checks a value against rules passed at creation time.
```python
in_range    = make_validator(min_val=0,   max_val=100)
high_score  = make_validator(min_val=90,  max_val=100)
valid_age   = make_validator(min_val=18,  max_val=60)

print(in_range(85))     # True
print(in_range(150))    # False
print(high_score(95))   # True
print(high_score(85))   # False
print(valid_age(25))    # True
print(valid_age(15))    # False
```

---

## Common Mistakes & Senior Traps

- **Loop variable capture** — closures capture variables by **reference**, not value. All closures in a loop see the final value. Fix with default arg `i=i` or a factory function.
- **`global` overuse** — using `global` is a code smell. If you find yourself using it often, your code needs better structure (class or closure).
- **`nonlocal` vs `global`** — `nonlocal` goes one level up to enclosing function. `global` goes all the way to module level. They are not interchangeable.
- **Mutable vs immutable in closures** — you can mutate a list/dict in a closure without `nonlocal`. But you need `nonlocal` to reassign an int/string.
```python
def outer():
    count = 0
    lst = []

    def inner():
        nonlocal count
        count += 1      # needs nonlocal — reassigning int
        lst.append(1)   # no nonlocal needed — mutating list

    inner()
```
- **Closures vs classes** — closures are great for simple stateful functions. But if the state grows complex, a class is more maintainable.

---

Say **next** for Topic 7: Recursion!