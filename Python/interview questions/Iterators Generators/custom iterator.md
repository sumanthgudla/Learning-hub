# Topic 4 — Building a Custom Iterator

Now let's **build an iterator ourselves**.

This is where the previous 3 topics come together.

Suppose we want an object that produces:

```text
10
20
30
40
50
```

one value at a time.

---

## 1. Create the class

```python
class NumberIterator:

    def __init__(self):
        self.current = 10
```

We need `current` because the iterator must **remember where it is**.

Initially:

```text
current = 10
```

---

## 2. Add `__iter__()`

```python
def __iter__(self):
    return self
```

Why?

Because this object **itself is the iterator**.

```text
iter(iterator)
      ↓
returns itself
```

---

## 3. Add `__next__()`

```python
def __next__(self):
    if self.current <= 50:
        value = self.current
        self.current += 10
        return value

    raise StopIteration
```

Complete code:

```python
class NumberIterator:

    def __init__(self):
        self.current = 10

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 50:
            value = self.current
            self.current += 10
            return value

        raise StopIteration
```

---

# 4. Let's use it

```python
numbers = NumberIterator()

print(next(numbers))
print(next(numbers))
print(next(numbers))
```

Output:

```text
10
20
30
```

Why?

Because `current` changes:

```text
Initial:
current = 10

next()
→ returns 10
→ current becomes 20

next()
→ returns 20
→ current becomes 30

next()
→ returns 30
→ current becomes 40
```

The iterator is **remembering its state**.

---

# 5. What happens after 50?

Continue:

```python
print(next(numbers))  # 40
print(next(numbers))  # 50
print(next(numbers))  # ?
```

After returning `50`:

```text
current = 60
```

So:

```python
if self.current <= 50:
```

is false.

Therefore:

```python
raise StopIteration
```

---

# 6. Now use `for`

This is where everything connects:

```python
numbers = NumberIterator()

for number in numbers:
    print(number)
```

Output:

```text
10
20
30
40
50
```

Internally, roughly:

```python
iterator = iter(numbers)

while True:
    try:
        value = next(iterator)
        print(value)
    except StopIteration:
        break
```

And:

```text
iter(numbers)
      ↓
__iter__()
      ↓
numbers itself
      ↓
next(numbers)
      ↓
__next__()
      ↓
10
      ↓
20
      ↓
30
      ↓
40
      ↓
50
      ↓
StopIteration
      ↓
for loop ends
```

---

# 7. Why do we need `self.current`?

This is a **very important concept**.

Imagine we didn't store the current position.

Every time `next()` runs, Python would have no way to know:

> "What did I return last time?"

The iterator needs **state**.

For our iterator:

```python
self.current
```

is that state.

```text
Iterator object
┌─────────────────────┐
│ current = 10        │
└─────────────────────┘
          ↓ next()
┌─────────────────────┐
│ current = 20        │
└─────────────────────┘
          ↓ next()
┌─────────────────────┐
│ current = 30        │
└─────────────────────┘
```

This is one reason iterators are useful: **they maintain progress through a sequence.**

---

# 8. A practical example

Imagine processing a huge database table.

Instead of loading:

```text
10 million records
        ↓
RAM
```

you could conceptually have an iterator that gives:

```text
record 1
   ↓
record 2
   ↓
record 3
   ↓
...
```

one at a time.

That's closely related to why **generators are useful for large data and streaming**.

We'll get to that soon.

---

# 9. Iterable vs Iterator in our example

Our `NumberIterator` is an **iterator** because it has:

```python
__iter__()
__next__()
```

And:

```python
iter(numbers)
```

returns:

```python
numbers
```

because:

```python
def __iter__(self):
    return self
```

So:

```text
NumberIterator
     │
     ├── __iter__() → itself
     │
     └── __next__() → next number
```

---

# 🎯 Interview question

### "How would you create a custom iterator in Python?"

A good answer:

> "I would create a class implementing the iterator protocol. It should define `__iter__()` and `__next__()`. `__iter__()` returns the iterator itself, while `__next__()` returns the next value and raises `StopIteration` when there are no more values."

Then you should be able to write something like:

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

Usage:

```python
for x in Counter(3):
    print(x)
```

Output:

```text
0
1
2
```

---

## 🧠 The key idea

Don't memorize the class.

Understand this:

```text
Iterator needs:
     ↓
state
     ↓
__next__() uses the state
     ↓
returns one value
     ↓
updates state
     ↓
eventually StopIteration
```

### So far:

```text
1. Iterable vs Iterator        ✅
2. for loop internally         ✅
3. Iterator protocol           ✅
4. Custom Iterator             ✅
```

Next: **Topic 5 — `StopIteration`**. We'll understand exactly **why it exists, who raises it, who catches it, and what happens if you don't catch it.**
