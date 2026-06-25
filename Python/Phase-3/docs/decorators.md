# Decorators (Senior/Interview Level)

## 1. What is it

A decorator is a function that **wraps another function (or class) to extend or modify its behavior without changing its source code**. Under the hood, `@decorator` is just syntactic sugar for `func = decorator(func)`. At senior level, decorators matter because they're the mechanism behind logging, caching, authentication, retries, timing, and validation in almost every production codebase — and interviewers use them to test whether you truly understand closures, `*args`/`**kwargs`, and function metadata preservation, not just the `@` syntax.

## 2. Core concepts table

| Concept | Description |
|---|---|
| Decorator | A callable that takes a function and returns a (usually wrapped) function |
| `@decorator` syntax | Sugar for `func = decorator(func)` applied at definition time |
| Closure | The wrapper function "closes over" the original function via the enclosing scope |
| `*args, **kwargs` | Used in wrappers to accept/forward arbitrary signatures transparently |
| `functools.wraps` | Preserves `__name__`, `__doc__`, `__module__` of the original function on the wrapper |
| Decorator with arguments | A function that returns a decorator (three levels of nesting) |
| Class-based decorators | Implementing `__call__` on a class instead of using nested functions |
| Stacking decorators | Multiple `@decorator`s apply bottom-up, like `f = dec1(dec2(f))` |
| `functools.lru_cache` | Built-in decorator for memoization |
| Decorating methods | Need to account for `self` as the first positional arg |
| Decorating classes | A decorator can wrap a whole class, not just a function |

## 3. Syntax & code examples

### Basic usage

```python
def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{func.__name__} returned {result}")
        return result
    return wrapper

@my_decorator
def add(a, b):
    return a + b

add(2, 3)
# → Calling add
# → add returned 5
```

### Common real-world pattern: timing + logging with `functools.wraps`

```python
import functools
import time

def timed(func):
    @functools.wraps(func)          # preserves func.__name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timed
def slow_square(n):
    """Returns n squared, slowly."""
    time.sleep(0.1)
    return n * n

print(slow_square(5))
# → slow_square took 0.1003s
# → 25

print(slow_square.__name__)   # → slow_square  (WITHOUT functools.wraps this would print "wrapper")
print(slow_square.__doc__)    # → Returns n squared, slowly.
```

### Senior-level / non-obvious usage: parameterized decorator + class-based decorator + stacking

```python
import functools

# Decorator that itself takes arguments — needs THREE levels of nesting
def retry(max_attempts=3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exc = e
                    print(f"Attempt {attempt} failed: {e}")
            raise last_exc
        return wrapper
    return decorator

@retry(max_attempts=2, exceptions=(ValueError,))
def flaky():
    raise ValueError("temporary failure")

# flaky()
# → Attempt 1 failed: temporary failure
# → Attempt 2 failed: temporary failure
# → raises ValueError: temporary failure


# Class-based decorator — useful when the decorator needs internal state
class CallCounter:
    def __init__(self, func):
        functools.update_wrapper(self, func)   # preserves metadata, like functools.wraps
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"Call #{self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CallCounter
def greet(name):
    return f"Hello, {name}"

greet("Sumanth")    # → Call #1 to greet
greet("Sumanth")    # → Call #2 to greet
print(greet.count)  # → 2


# Stacking decorators — order matters! Applied bottom-up.
def bold(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        return f"<b>{func(*a, **kw)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*a, **kw):
        return f"<i>{func(*a, **kw)}</i>"
    return wrapper

@bold
@italic
def text():
    return "Hi"

print(text())
# → <b><i>Hi</i></b>
# Equivalent to: text = bold(italic(text))
# italic wraps FIRST (closest to function), bold wraps SECOND (outermost)
```

**ASCII view — how stacking actually executes:**

```
@bold
@italic
def text(): ...

is equivalent to:

text = bold(italic(text))

Call order when text() is invoked:
  bold's wrapper()  ──► calls ──► italic's wrapper()  ──► calls ──► original text()
        │                                │                             │
        └── wraps result in <b>          └── wraps result in <i>       └── returns "Hi"

Result builds INSIDE-OUT: "Hi" → "<i>Hi</i>" → "<b><i>Hi</i></b>"
```

## 4. Internals / how it works

- `@decorator` is purely **syntactic sugar**, applied at **function definition time** (when the module is loaded/imported), not at call time. `def f(): ...` followed by `@dec` is literally executed as `f = dec(f)` immediately after `f` is defined.
- The wrapper function works because of **closures** — when `wrapper` is defined inside `my_decorator`, it captures `func` (and any other enclosing variables) in its `__closure__` (a tuple of cell objects). You can inspect this: `add.__closure__[0].cell_contents` would show the captured `func`.
- Without `functools.wraps`, the wrapper function *replaces* the original function's identity entirely — `wrapped_func.__name__` becomes `"wrapper"`, `__doc__` becomes `None`, and tools relying on introspection (debuggers, API doc generators, `help()`) break. `functools.wraps` copies over `__name__`, `__doc__`, `__module__`, `__dict__`, and sets `__wrapped__` to point back to the original — this is itself implemented as a decorator (`functools.wraps(func)` returns a partial application of `functools.update_wrapper`).
- A parameterized decorator (`@retry(max_attempts=3)`) requires **three layers** of functions because `retry(max_attempts=3)` must first execute and *return* the actual decorator — which then gets applied to `func`. This is the single most common point of confusion: people forget the outer "factory" layer.
- Class-based decorators work because Python allows any object implementing `__call__` to be used where a callable is expected — `@CallCounter` on `def greet` literally does `greet = CallCounter(greet)`, and then `greet("Sumanth")` invokes `CallCounter.__call__(greet_instance, "Sumanth")`.
- When decorating **methods**, the wrapper's `*args` automatically captures `self` as the first positional argument since methods are just functions that receive the instance as their first parameter at call time — no special handling needed, but it trips people up when they try to type-hint or validate args without accounting for `self`.

## 5. Interview questions

**Q1: Why is `functools.wraps` important, and what specifically breaks if you omit it?**
A: Without it, the wrapper function's metadata (`__name__`, `__doc__`, `__module__`, `__qualname__`) is lost and replaced with the wrapper's own — so `decorated_func.__name__` shows `"wrapper"` instead of the real name. This breaks introspection-dependent tools: debuggers showing wrong function names in stack traces, `help()` showing no docstring, Sphinx/auto-doc generators producing wrong documentation, and `pickle` failing on decorated functions because it can't find them by their (now-wrong) qualified name.

**Q2: How would you write a decorator that itself accepts arguments, like `@retry(max_attempts=3)`? Why does it need an extra layer of nesting compared to a plain decorator?**
A: A plain decorator is `func -> wrapped_func` (one function taking the target function). A parameterized decorator needs to first accept the *decorator's own arguments* (`max_attempts=3`) and **return** a decorator — so it's `(decorator_args) -> (func -> wrapped_func)`, i.e., three nested functions: the outer one captures the decorator's config, the middle one captures the target function, and the inner `wrapper` does the actual work, closing over both.

**Q3: What's the difference between decorating a function with a closure-based decorator versus a class-based decorator (`__call__`)? When would you prefer one over the other?**
A: A closure-based decorator is simpler for stateless behavior (logging, timing) — it's just nested functions. A class-based decorator is preferable when the decorator needs to **maintain state across calls** (like a call counter, a cache, or rate limiter) in a more explicit, inspectable way (`instance.count`), or when the decorator itself needs multiple methods/configuration beyond just wrapping. Class-based decorators also make it easier to add additional public methods (e.g., `cache.clear()`).

**Q4: In `@bold @italic def text(): ...`, what's the execution order — both at definition time and at call time?**
A: At *definition* time, decorators apply bottom-up: `italic` wraps `text` first, then `bold` wraps the result — equivalent to `text = bold(italic(text))`. At *call* time, execution happens outside-in: calling `text()` first enters `bold`'s wrapper, which calls `italic`'s wrapper, which calls the original `text()` — so the **outermost decorator in the call stack is the one closest to `@`, but it's the last one applied at definition time**. The actual function body runs innermost, and results get wrapped on the way back out.

**Q5: How does `functools.lru_cache` work as a decorator, and what are its caveats?**
A: `lru_cache` wraps a function with a dict-based memoization cache keyed by the function's arguments (which must be hashable). On each call, it checks if those exact arguments were seen before; if so, returns the cached result instead of recomputing. Caveats: arguments must be hashable (no lists/dicts), it can cause unbounded memory growth if `maxsize=None` and inputs are highly varied, it doesn't account for mutable default arguments changing behavior, and for instance methods, since `self` is part of the cache key, it keeps instances alive longer than expected (a subtle memory leak in long-lived objects) unless you're careful.

## 6. Practice problems

**Beginner:**
Write a decorator `@uppercase_result` that wraps any function returning a string and converts the result to uppercase. Apply it to a function `greet(name)` that returns `f"hello, {name}"`. Use `functools.wraps` correctly.
- Suggested filename: `decorators_prac01_uppercase_result.py`
- Input: `greet("sumanth")` → Output: `"HELLO, SUMANTH"`

**Senior:**
Build a **parameterized rate-limiting decorator** `@rate_limit(max_calls, period_seconds)` that:
1. Limits how many times a function can be called within a rolling time window (`period_seconds`).
2. If the limit is exceeded, raise a custom exception `RateLimitExceededError` (reuse your custom-exceptions knowledge!) instead of calling the function.
3. Must work correctly when applied to multiple *different* functions independently (i.e., each decorated function tracks its own call history, not a shared global one) — this requires understanding closures carefully.
4. Bonus: make it also work as a class-based decorator, and compare both implementations.
5. Use `functools.wraps` so the wrapped function still reports the correct `__name__`.

Test it by calling a decorated function 5 times rapidly with `max_calls=3, period_seconds=2`, and confirm it raises after the 3rd call, then succeeds again after sleeping past the window.
- Suggested filename: `decorators_prac02_rate_limiter.py`
- Expected behavior: calls 1–3 succeed, call 4 raises `RateLimitExceededError`, after `time.sleep(2.1)` call 5 succeeds again.

## 7. Common mistakes & senior traps

- **Forgetting `*args, **kwargs` in the wrapper**, breaking any decorated function that doesn't match the exact signature you hardcoded.
  ```python
  # WRONG
  def log(func):
      def wrapper(a, b):     # only works for 2-arg functions!
          return func(a, b)
      return wrapper

  # RIGHT
  def log(func):
      def wrapper(*args, **kwargs):
          return func(*args, **kwargs)
      return wrapper
  ```

- **Omitting `functools.wraps`**, silently corrupting introspection, docs, and debugging — a very common senior-interview "spot the bug" question.

- **Mutable default state shared across calls when it shouldn't be** — e.g., putting a cache dict at decorator-definition time instead of per-wrapped-function, accidentally sharing state across unrelated decorated functions.
  ```python
  # WRONG — shared across ALL decorated functions
  cache = {}
  def memoize(func):
      def wrapper(*args):
          if args not in cache:
              cache[args] = func(*args)
          return cache[args]
      return wrapper

  # RIGHT — each decorated function gets its own cache via closure
  def memoize(func):
      cache = {}              # created fresh per decoration
      def wrapper(*args):
          if args not in cache:
              cache[args] = func(*args)
          return cache[args]
      return wrapper
  ```

- **Confusing the order of stacked decorators**, especially when order actually matters (e.g., `@app.route` must be outermost in Flask; `@timed @retry` vs `@retry @timed` give very different timing semantics — one times each retry attempt individually, the other times the whole retry block).

- **Forgetting the extra nesting layer for parameterized decorators**, leading to `TypeError: decorator() missing 1 required positional argument: 'func'` — a classic bug when going from `@my_decorator` to `@my_decorator(some_arg)` and forgetting decorators-with-args need three function layers, not two.

- **Decorating instance methods without accounting for `self`** when doing argument validation/type checking inside the wrapper — `args[0]` will be `self`, not the first "real" argument, which trips up naive implementations.

- **Using a decorator when a simple higher-order function call would do** — over-engineering one-off behavior into a reusable decorator adds indirection without benefit; senior judgment includes knowing when *not* to decorate.

---

Say **"next"** when you're ready for **Context Managers**, or ask for more practice problems on decorators first.