# Iterators & Generators (Senior/Interview Level)

## 1. What is it

An **iterator** is any object implementing the iterator protocol (`__iter__` + `__next__`) that produces values one at a time and remembers its position between calls. A **generator** is the easiest way to build an iterator — a function using `yield` that automatically pauses/resumes its execution state. At senior level, this matters because generators are the foundation of **lazy evaluation** — processing huge or infinite data streams without loading everything into memory — and interviewers use this topic to probe whether you understand memory/performance tradeoffs, not just syntax.

## 2. Core concepts table

| Concept | Description |
|---|---|
| Iterable | Any object with `__iter__()` that returns an iterator (lists, dicts, strings, files, etc.) |
| Iterator | Object with `__iter__()` (returns self) and `__next__()` (returns next value or raises `StopIteration`) |
| `iter(obj)` | Calls `obj.__iter__()` to get an iterator from an iterable |
| `next(it)` | Calls `it.__next__()`; raises `StopIteration` when exhausted |
| Generator function | A function with `yield`; calling it returns a generator object (doesn't run the body yet) |
| Generator expression | `(x*2 for x in range(10))` — lazy version of a list comprehension |
| `yield` | Pauses function, returns a value, preserves local state for resumption |
| `yield from` | Delegates iteration to a sub-iterable/sub-generator |
| `.send(value)` | Resumes a generator and feeds a value into the paused `yield` expression |
| `.throw(exc)` | Raises an exception inside the generator at the paused point |
| `.close()` | Raises `GeneratorExit` inside the generator, used for cleanup |
| `StopIteration` | Signal (not error in normal use) that iteration is complete |
| Lazy evaluation | Values computed on demand, not all upfront — core memory benefit of generators |
| Generator vs Iterator class | Generators are a concise shortcut for writing the iterator protocol manually |

## 3. Syntax & code examples

### Basic usage

```python
# Manual iterator protocol
nums = [1, 2, 3]
it = iter(nums)          # get an iterator from the list
print(next(it))           # → 1
print(next(it))           # → 2
print(next(it))           # → 3
# print(next(it))         # → raises StopIteration

# Generator function — the easy way
def count_up_to(n):
    i = 1
    while i <= n:
        yield i           # pauses here, returns i
        i += 1

gen = count_up_to(3)
print(next(gen))          # → 1
print(next(gen))          # → 2
print(list(gen))          # → [3]  (consumes the rest; note: 1 and 2 already consumed)

# Generator expression (lazy, like a list comprehension but no memory upfront)
squares = (x**2 for x in range(5))
print(next(squares))      # → 0
print(sum(squares))       # → 1+4+9+16 = 30 (0 already consumed)
```

### Common real-world pattern: streaming large data without loading it all into memory

```python
def read_large_file(path):
    """Yields one line at a time instead of loading the whole file into memory."""
    with open(path) as f:
        for line in f:
            yield line.rstrip("\n")

def filter_errors(lines):
    """Generator pipeline — only pulls from `lines` as needed."""
    for line in lines:
        if "ERROR" in line:
            yield line

# Nothing is read from disk until you actually iterate:
for error_line in filter_errors(read_large_file("app.log")):
    print(error_line)
    # → processes file lazily, line by line, constant memory regardless of file size
```

### Senior-level / non-obvious usage: `yield from`, `send()`, and building a custom iterator class

```python
# yield from delegates to a sub-generator — flattens nested generators cleanly
def inner():
    yield 1
    yield 2

def outer():
    yield "start"
    yield from inner()     # delegates: yields 1, then 2, transparently
    yield "end"

print(list(outer()))       # → ['start', 1, 2, 'end']


# Coroutine-style generator using send() — two-way communication
def running_average():
    total = 0
    count = 0
    avg = None
    while True:
        value = yield avg       # pauses, waits to receive a value via send()
        total += value
        count += 1
        avg = total / count

avg_gen = running_average()
next(avg_gen)                   # prime the generator (advance to first yield)
print(avg_gen.send(10))         # → 10.0
print(avg_gen.send(20))         # → 15.0
print(avg_gen.send(30))         # → 20.0


# Custom iterator class (what generators do for you automatically)
class CountUpTo:
    """Manually implementing the iterator protocol — shows what's under the hood."""
    def __init__(self, n):
        self.n = n
        self.i = 1

    def __iter__(self):
        return self           # an iterator must return itself from __iter__

    def __next__(self):
        if self.i > self.n:
            raise StopIteration
        val = self.i
        self.i += 1
        return val

for x in CountUpTo(3):
    print(x)                  # → 1, 2, 3
```

**ASCII view — generator pause/resume vs a list:**

```
List comprehension (eager):
[x for x in range(1_000_000)]
  └─► builds ALL 1,000,000 ints in memory immediately

Generator (lazy):
(x for x in range(1_000_000))
  └─► holds only: current state (i=0) + the code object
        next() called ──► resumes at last yield ──► computes ONE value ──► pauses again
```

## 4. Internals / how it works

- A generator function, when called, does **not** execute any code — it immediately returns a generator object wrapping a **frame object** (the function's local variables, instruction pointer, and stack) in a suspended state.
- Each call to `next()` resumes that frame exactly where it left off (right after the last `yield`), runs until the next `yield` or `return`/end of function, and then re-suspends. This is implemented at the C level via `PyGen_Type` and the frame's `f_lasti` (last instruction index) — the interpreter literally jumps back into the middle of the function's bytecode.
- When a generator function ends (falls off the end or hits `return`), Python raises `StopIteration` internally — `for` loops catch this automatically; manual `next()` calls will propagate it as a real exception.
- Because only one frame's worth of state is kept (not all values), memory usage is **O(1)** relative to the data size, versus **O(n)** for a fully materialized list — this is the core performance argument senior interviews are fishing for.
- `yield from sub_gen` isn't just sugar for a loop — it properly delegates `.send()`, `.throw()`, and `.close()` calls down to the sub-generator, and propagates the sub-generator's return value as the value of the `yield from` expression. A manual `for x in sub_gen: yield x` loop does **not** do this — it loses send/throw delegation, which is a real, testable difference.
- Generators implement the **iterator protocol** identically to classes with `__iter__`/`__next__`, but the state machine (local variables, where you paused) is managed automatically by the interpreter instead of by hand-written instance attributes — that's the entire value proposition.

## 5. Interview questions

**Q1: What's the practical difference between a generator and a list, and when would you choose one over the other?**
A: A list is eagerly evaluated and stored fully in memory — O(n) space, but supports random access (`lst[5]`), repeated iteration, `len()`, slicing. A generator is lazily evaluated — O(1) space regardless of size, but is single-pass (once exhausted, it's gone), no random access, no `len()`. Choose generators for large/streaming/infinite data or pipelines where you only need to iterate once; choose lists when you need to access elements multiple times or out of order.

**Q2: Why does iterating over a generator twice in a row (e.g., `list(gen)` then `list(gen)` again) give an empty result the second time?**
A: A generator's state (its frame, instruction pointer, locals) is consumed as you iterate — there's no "reset." Once the function body has run to completion (or hit `StopIteration`), the frame is gone. Unlike a list, which is a static container, a generator is a one-shot process. If you need to iterate multiple times, you need a fresh generator (call the generator function again) or materialize it into a list/tuple.

**Q3: What does `yield from` do differently than a plain `for ... yield` loop, and why does that matter?**
A: Beyond flattening iteration, `yield from` properly forwards `.send(value)` and `.throw(exception)` calls into the sub-generator, and it captures and exposes the sub-generator's `return` value as the result of the `yield from` expression (`result = yield from sub_gen()`). A manual loop only forwards yielded values — it silently breaks two-way communication and loses the return value. This matters for coroutine-style generators and for building composable generator pipelines correctly.

**Q4: How would you build an infinite generator safely, and how do you consume it without hanging the program?**
A: Use a `while True:` loop with `yield` inside (e.g., an infinite counter or a polling generator). To consume it safely, never call `list(gen)` on it directly — pair it with something that limits consumption, like `itertools.islice(gen, n)`, a `break` condition inside a `for` loop, or `next()` called a bounded number of times. The key insight: the generator itself doesn't "know" to stop — bounding is the consumer's responsibility.

**Q5: Why is `StopIteration` special, and what changed in Python 3.7 (PEP 479) regarding it?**
A: `StopIteration` is the normal termination signal for iteration — `for` loops catch it silently. Before PEP 479, if a `StopIteration` was accidentally raised *inside* a generator body (e.g., from a bug, like calling `next()` on an exhausted sub-iterator without catching it),  would silently propagate out and the enclosing `for` loop would interpret it as "this generator is done," masking a real bug. PEP 479 changed this: a `StopIteration` raised inside a generator's body is now converted into a `RuntimeError`, so such bugs surface loudly instead of silently truncating iteration.

## 6. Practice problems

**Beginner:**
Write a generator function `even_numbers(n)` that yields all even numbers from 0 up to (and including) `n`. Then use it in a `for` loop to print them, and separately use `sum()` directly on a fresh call to the generator to get their total.
- Suggested filename: `generators_prac01_even_numbers.py`
- Input: `even_numbers(10)` → Output (looped): `0 2 4 6 8 10`; `sum(even_numbers(10))` → `30`

**Senior:**
Build a **lazy ETL pipeline** using chained generators (no lists in between stages — everything must stay lazy until the very end):
1. `read_records(data)` — a generator that yields dicts one at a time from a list of raw strings like `"id:1,amount:50.5,status:valid"` (parse each into a dict).
2. `filter_valid(records)` — a generator that yields only records where `status == "valid"`.
3. `running_total(records)` — a generator that yields each record alongside a *running cumulative total* of `amount` so far, using `yield` (not a pre-computed list) — i.e., it should maintain state across `yield` calls.
4. Chain all three together with `yield from`/composition and consume only the first 3 results using `itertools.islice`, without ever materializing the full pipeline into a list.
it
Print each yielded `(record, running_total)` tuple.
- Suggested filename: `generators_prac02_lazy_etl_pipeline.py`
- Example input: `["id:1,amount:50.5,status:valid", "id:2,amount:30,status:invalid", "id:3,amount:20,status:valid"]`
- Expected output (first 3, but only 2 are actually valid so demonstrate it stops correctly): `({'id': '1', 'amount': 50.5, 'status': 'valid'}, 50.5)`, `({'id': '3', 'amount': 20.0, 'status': 'valid'}, 70.5)`

## 7. Common mistakes & senior traps

- **Calling a generator function thinking it runs immediately.** It doesn't — the body only executes when you start iterating (calling `next()` or looping).
  ```python
  def gen():
      print("starting")
      yield 1

  g = gen()              # WRONG assumption: prints "starting" now — it does NOT
  print("got here")      # actually prints first
  next(g)                 # NOW "starting" prints
  ```

- **Trying to reuse an exhausted generator.** Once consumed, it's permanently empty — there's no rewind.
  ```python
  g = (x for x in range(3))
  print(list(g))   # → [0, 1, 2]
  print(list(g))   # → [] (WRONG assumption that it resets)
  # RIGHT: call the generator expression/function again for a fresh one
  ```

- **Using `yield` and `return value` together incorrectly** — in a generator, `return value` doesn't return `value` to the caller of `next()`; it raises `StopIteration(value)`, and the value is only retrievable via `.value` on the caught `StopIteration`, or through `yield from`.
  ```python
  def gen():
      yield 1
      return "done"

  g = gen()
  next(g)                 # → 1
  try:
      next(g)
  except StopIteration as e:
      print(e.value)       # → "done"
  ```

- **Forgetting to "prime" a generator before calling `.send()`** — the first `next()` (or `.send(None)`) is required to advance the generator to its first `yield` before you can send a real value in.
  ```python
  def gen():
      x = yield
      print(x)

  g = gen()
  # g.send(5)   # WRONG — raises TypeError: can't send non-None value to a just-started generator
  next(g)        # prime it first
  g.send(5)      # RIGHT → prints 5
  ```

- **Materializing a generator pipeline into a list "just to debug it,"** which defeats the entire memory benefit and can crash on huge/infinite inputs — senior code should keep pipelines lazy end-to-end and only materialize the final, bounded result.

- **Not realizing generator expressions inside function calls don't need extra parens**, and conflating that with "they're the same as list comprehensions" performance-wise — `sum(x for x in range(10**8))` is lazy and memory-efficient; `sum([x for x in range(10**8)])` builds a huge intermediate list first.

---

Say **"next"** when you're ready for **Decorators**, or ask for more practice problems on iterators & generators first.