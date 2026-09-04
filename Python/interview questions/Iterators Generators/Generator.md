# Topic 6 — Generators + `yield` ⭐

This is the **most important part of iterators and generators**.

The big idea:

> **A generator is an easy way to create an iterator.**

Instead of manually writing:

```python
__iter__()
__next__()
StopIteration
```

Python can handle all of that for us.

---

# 1. First, remember our custom iterator

Earlier we wrote:

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

That's quite a lot of code just to produce:

```text
0
1
2
```

With a generator, we can write:

```python
def counter(limit):
    for i in range(limit):
        yield i
```

That's it.

---

# 2. What is `yield`?

`yield` is similar to `return`, but **not the same**.

Consider:

```python
def test():
    return 10
```

When we call:

```python
result = test()
```

the function executes and finishes.

```text
test()
  ↓
return 10
  ↓
function ends
```

But with:

```python
def test():
    yield 10
```

calling:

```python
result = test()
```

does **not execute the function body normally**.

Instead, Python creates a **generator object**.

```text
test()
  ↓
Generator object
```

---

# 3. Let's see it

```python
def numbers():
    yield 10
    yield 20
    yield 30
```

Now:

```python
result = numbers()

print(result)
```

You'll get something like:

```text
<generator object numbers at 0x...>
```

Notice:

**It hasn't produced 10, 20, 30 yet.**

It has created a generator.

---

# 4. When does it actually execute?

When you call:

```python
next(result)
```

Python starts executing the generator.

```python
def numbers():
    print("Starting")
    yield 10
    yield 20
    yield 30
```

Now:

```python
result = numbers()

print("Before next")

print(next(result))
```

Execution:

```text
Before next
Starting
10
```

The function starts executing only when `next()` is called.

---

# 5. The BIG difference between `return` and `yield`

Consider:

```python
def test():
    print("A")
    return 10
    print("B")
```

Calling:

```python
test()
```

Output:

```text
A
```

Function ends at `return`.

But:

```python
def test():
    print("A")
    yield 10
    print("B")
    yield 20
```

Now:

```python
g = test()
```

Nothing happens yet.

Then:

```python
print(next(g))
```

Output:

```text
A
10
```

The generator **pauses at `yield`**.

This is the key concept.

---

# 6. What happens on the second `next()`?

Continue:

```python
print(next(g))
```

Python **doesn't start the function from the beginning**.

It resumes from where it previously paused.

So:

```text
First next()
    ↓
print("A")
    ↓
yield 10
    ↓
PAUSE
```

Second `next()`:

```text
RESUME
   ↓
print("B")
   ↓
yield 20
   ↓
PAUSE
```

Output:

```text
A
10
B
20
```

---

# 7. Third `next()`

```python
print(next(g))
```

The generator resumes after:

```python
yield 20
```

and reaches the end of the function.

So:

```text
Generator
   ↓
yield 10
   ↓
pause
   ↓
yield 20
   ↓
pause
   ↓
function ends
   ↓
StopIteration
```

Therefore:

```python
next(g)
```

after the final yield raises:

```text
StopIteration
```

---

# 8. Why is this called a generator?

Because the function **generates values one at a time**.

For example:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

It doesn't create:

```text
[1, 2, 3]
```

all at once.

Instead:

```text
next()
 ↓
1

next()
 ↓
2

next()
 ↓
3
```

---

# 9. Generator = Iterator

This is a very important interview point.

When you do:

```python
g = numbers()
```

`g` is a generator object.

And a generator is an **iterator**.

So:

```python
next(g)
```

works.

And:

```python
for x in g:
    print(x)
```

works too.

Conceptually:

```text
Generator
    │
    ├── iterable
    │
    └── iterator
```

---

# 10. Why are generators useful?

### Memory efficiency ⭐

Compare:

```python
numbers = [x for x in range(10000000)]
```

This creates a huge list and stores all those values in memory.

With:

```python
numbers = (x for x in range(10000000))
```

or:

```python
def numbers():
    for x in range(10000000):
        yield x
```

values are produced **one at a time**.

Conceptually:

```text
List:

10 million values
       ↓
    Memory
████████████████████


Generator:

value → process → discard
value → process → discard
value → process → discard
```

This is why generators are useful for:

* large files
* database records
* streaming data
* pipelines
* large datasets
* processing data that doesn't need to stay in memory

---

# 11. Real-world example: reading a huge file

Imagine a file with **10 GB** of data.

Bad approach:

```python
with open("huge_file.txt") as f:
    data = f.readlines()
```

This attempts to load all the lines into memory.

Instead, you can process it incrementally:

```python
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line
```

Then:

```python
for line in read_lines("huge_file.txt"):
    process(line)
```

Conceptually:

```text
File
 │
 ├── line 1 → process
 ├── line 2 → process
 ├── line 3 → process
 ├── ...
 └── line 10 million → process
```

You don't need all 10 million lines in memory simultaneously.

---

# 12. Generator execution — remember this

This is probably the **single most important thing** to understand:

```python
def numbers():
    print("A")
    yield 10

    print("B")
    yield 20

    print("C")
    yield 30
```

Then:

```python
g = numbers()
```

### Nothing prints.

Then:

```python
next(g)
```

prints:

```text
A
```

and returns:

```text
10
```

Generator pauses.

Then:

```python
next(g)
```

prints:

```text
B
```

and returns:

```text
20
```

Generator pauses.

Then:

```python
next(g)
```

prints:

```text
C
```

and returns:

```text
30
```

Then another:

```python
next(g)
```

→ `StopIteration`

---

# 🎯 Interview question

### "What is a generator?"

Strong answer:

> **A generator is a special type of iterator created using a function containing `yield`. It produces values lazily, one at a time, and maintains its execution state between calls, which makes it memory-efficient for processing large or streaming data.**

### "What is the difference between `return` and `yield`?"

> **`return` terminates the function and returns a value. `yield` produces a value and pauses the generator, preserving its state so execution can resume from that point on the next `next()` call.**

---

## 🧠 The mental model

Don't think:

```text
yield = return
```

Think:

```text
return:
    give value
    FINISH

yield:
    give value
    PAUSE
    remember state
    RESUME later
```

That's the heart of generators.

---

### Progress

```text
1. Iterable vs Iterator       ✅
2. for loop internally        ✅
3. Iterator Protocol           ✅
4. Custom Iterator             ✅
5. StopIteration               ✅
6. Generators + yield          ✅
7. Generator vs Iterator       ⬅️ NEXT
8. Generator Expressions
9. yield from
10. Real-world + Interview
```

Next we'll make the **generator vs iterator distinction crystal clear**, including the question interviewers often ask: **"If a generator is an iterator, then what's the actual difference?"**
