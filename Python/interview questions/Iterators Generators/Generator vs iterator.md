# Topic 7 — Generator vs Iterator ⭐

This is a **very common interview question**:

> "If a generator is an iterator, what's the difference between a generator and an iterator?"

The short answer:

> **A generator is one way of creating an iterator.**

Let's understand that properly.

---

## 1. Iterator — you build the machinery yourself

We created this earlier:

```python
class Counter:

    def __init__(self, limit):
        self.current = 0
        self.limit = limit

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < self.limit:
            value = self.current
            self.current += 1
            return value

        raise StopIteration
```

You have to manually implement:

```text
__iter__()
__next__()
state
StopIteration
```

---

## 2. Generator — Python handles that machinery

Instead of all that:

```python
def counter(limit):
    for i in range(limit):
        yield i
```

Python automatically handles the iterator mechanics.

You don't explicitly write:

```python
__iter__()
__next__()
raise StopIteration
```

---

# 3. So both can be used with `next()`

Custom iterator:

```python
counter = Counter(3)

print(next(counter))
print(next(counter))
print(next(counter))
```

Generator:

```python
counter = counter(3)

print(next(counter))
print(next(counter))
print(next(counter))
```

Both produce:

```text
0
1
2
```

So from the user's perspective:

```text
Iterator  → next() → value
Generator → next() → value
```

---

# 4. But a generator IS an iterator

This is important.

```python
def numbers():
    yield 1
    yield 2
    yield 3

g = numbers()
```

You can check:

```python
print(iter(g) is g)
```

Output:

```text
True
```

So:

```text
Generator
    ↓
Iterator
    ↓
Iterable
```

A generator is an iterator.

---

# 5. Then what's the difference?

Think about **how they are created**.

### Custom iterator

You manually create a class:

```python
class Counter:

    def __iter__(self):
        return self

    def __next__(self):
        ...
```

You manage the state yourself.

### Generator

You write a function with `yield`:

```python
def counter():
    yield 1
    yield 2
```

Python manages the state and iteration machinery.

---

# 6. Side-by-side comparison

|                     | Iterator               | Generator                             |
| ------------------- | ---------------------- | ------------------------------------- |
| Creation            | Usually class          | Function with `yield`                 |
| `__iter__()`        | You implement it       | Python provides it                    |
| `__next__()`        | You implement it       | Python provides it                    |
| State management    | You manage it          | Python manages it                     |
| `StopIteration`     | You generally raise it | Python handles it when generator ends |
| Lazy?               | Can be                 | Yes                                   |
| Memory efficient?   | Can be                 | Yes                                   |
| `next()` supported? | Yes                    | Yes                                   |

---

# 7. Very important: Iterator ≠ necessarily generator

This direction is important:

```text
Generator → Iterator
```

But:

```text
Iterator → Generator
```

is **not necessarily true**.

For example:

```python
class MyIterator:

    def __iter__(self):
        return self

    def __next__(self):
        ...
```

This is an iterator.

But it's not a generator.

So:

> **Every generator is an iterator, but not every iterator is a generator.**

🔥 **Remember this for interviews.**

---

# 8. Why would we ever create a custom iterator?

If generators are easier, why bother with classes?

Because sometimes you want an iterator with **more complex behavior/state**.

For example, imagine an object that needs:

```text
configuration
multiple state variables
methods
validation
custom behavior
```

A class can make that structure clearer.

Example:

```python
class EvenNumbers:

    def __init__(self, start, end):
        self.current = start
        self.end = end

    def __iter__(self):
        return self

    def __next__(self):
        while self.current <= self.end:
            value = self.current
            self.current += 1

            if value % 2 == 0:
                return value

        raise StopIteration
```

That's a custom iterator.

---

# 9. The generator version is much simpler

The same idea:

```python
def even_numbers(start, end):
    for number in range(start, end + 1):
        if number % 2 == 0:
            yield number
```

Usage:

```python
for x in even_numbers(1, 10):
    print(x)
```

Output:

```text
2
4
6
8
10
```

Much less code.

---

# 10. Interview question: "Why use generators?"

Don't simply say:

> "Because they save memory."

That's correct, but incomplete.

A stronger answer:

> "Generators provide lazy evaluation. They produce values only when requested, so they don't need to hold the entire result in memory. They're especially useful for large datasets, file processing, database records, and streaming or pipeline-based processing."

---

# 11. One important correction

Don't think:

> "Generators are always faster."

That's not necessarily true.

Generators are primarily about:

**lazy evaluation + memory efficiency + streaming**

For example:

```python
[x * 2 for x in range(100)]
```

may be perfectly appropriate if you actually need all 100 results immediately.

Generator:

```python
(x * 2 for x in range(100))
```

is useful when you want to consume the results progressively.

---

# 🎯 Interview answer

If asked:

### "Difference between iterator and generator?"

You can say:

> "An iterator is an object that follows the iterator protocol by implementing `__iter__()` and `__next__()`. A generator is a simpler way to create an iterator using a function containing `yield`. Generators automatically maintain their execution state and handle the iteration machinery, while with a custom iterator we implement that logic ourselves. Every generator is an iterator, but not every iterator is a generator."

That's a **strong interview-level answer**.

---

## 🧠 Mental model

```text
                    ITERABLE
                       │
                  iter()
                       ↓
                   ITERATOR
                  /         \
                 /           \
       Custom Iterator     Generator
            │                  │
      class + methods      yield function
            │                  │
       You manage state    Python manages state
```

And the key relationship:

```text
Every Generator
       ↓
    Iterator

But

Every Iterator
       ✗
is NOT necessarily a Generator
```

---

### Progress

```text
1. Iterable vs Iterator       ✅
2. for loop internally        ✅
3. Iterator Protocol          ✅
4. Custom Iterator             ✅
5. StopIteration               ✅
6. Generators + yield          ✅
7. Generator vs Iterator       ✅
8. Generator Expressions       ⬅️ NEXT
9. yield from
10. Real-world + Interview
```

Next: **Generator Expressions** — we'll compare:

```python
[x * 2 for x in range(5)]
```

with:

```python
(x * 2 for x in range(5))
```

and understand exactly **what is stored in memory in each case**.
