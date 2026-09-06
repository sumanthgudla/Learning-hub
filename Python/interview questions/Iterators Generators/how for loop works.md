# Topic 2 — How `for` Loop Works Internally

This is **very important for interviews** because once you understand this, iterators and generators become much easier.

Consider:

```python
numbers = [10, 20, 30]

for x in numbers:
    print(x)
```

You already know `numbers` is an **iterable**.

But Python cannot directly call `next(numbers)` because a list is not an iterator.

So what does Python actually do?

---

## 1. Step 1 — Python calls `iter()`

Conceptually:

```python
iterator = iter(numbers)
```

So:

```text
numbers
[10, 20, 30]
    ↓
  iter()
    ↓
iterator
```

Now Python has an iterator.

---

## 2. Step 2 — Python repeatedly calls `next()`

Conceptually:

```python
x = next(iterator)
```

First call:

```text
next(iterator) → 10
```

Then:

```python
print(x)
```

Output:

```text
10
```

Python calls `next()` again:

```text
next(iterator) → 20
```

Then:

```text
20
```

Again:

```text
next(iterator) → 30
```

Then:

```text
30
```

---

## 3. Step 3 — Eventually `next()` raises `StopIteration`

Python calls:

```python
next(iterator)
```

There are no more elements.

So:

```text
StopIteration
```

is raised.

The `for` loop catches this internally and **stops the loop**.

---

# 4. So this:

```python
numbers = [10, 20, 30]

for x in numbers:
    print(x)
```

is conceptually similar to:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

while True:
    try:
        x = next(iterator)
        print(x)
    except StopIteration:
        break
```

This is the key thing to understand.

### `for` loop = `iter()` + repeated `next()` + handling `StopIteration`

---

# 5. Let's execute it manually

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))
```

Execution:

```text
iterator → [10, 20, 30]

next() → 10
next() → 20
next() → 30
```

Then:

```python
print(next(iterator))
```

results in:

```text
StopIteration
```

---

# 6. Why doesn't `for` show `StopIteration`?

This is an important interview question.

If you manually do:

```python
next(iterator)
```

after the iterator is exhausted, you see:

```text
StopIteration
```

But:

```python
for x in numbers:
    print(x)
```

doesn't show an error.

That's because the `for` loop internally handles `StopIteration`.

Conceptually:

```python
while True:
    try:
        value = next(iterator)
    except StopIteration:
        break
```

So `StopIteration` means:

> "Iteration is finished."

It isn't treated as an error by the `for` loop.

---

# 7. What about dictionaries?

Consider:

```python
person = {
    "name": "Sumanth",
    "age": 27
}

for x in person:
    print(x)
```

Internally:

```python
iterator = iter(person)
```

Then:

```python
next(iterator)
```

returns:

```text
name
```

Next:

```text
age
```

So the loop prints:

```text
name
age
```

Notice that iterating over a dictionary by default gives you **keys**.

---

# 8. What about strings?

```python
name = "ABC"

for char in name:
    print(char)
```

Conceptually:

```python
iterator = iter(name)

next(iterator)  # A
next(iterator)  # B
next(iterator)  # C
next(iterator)  # StopIteration
```

Output:

```text
A
B
C
```

---

# 9. The BIG interview connection

This explains why Python's `for` loop can work with completely different types:

```python
for x in [1, 2, 3]:
```

```python
for x in "hello":
```

```python
for x in {1, 2, 3}:
```

```python
for x in range(10):
```

Python doesn't need special logic for each one.

It basically asks:

> **"Can you give me an iterator?"**

If yes, Python can iterate over it.

That's the power of the **iterator protocol**.

---

# 🎯 Interview question

### Q: What happens internally when Python executes a `for` loop?

Good answer:

> "Python first calls `iter()` on the iterable to obtain an iterator. It then repeatedly calls `next()` on that iterator to retrieve values. When `next()` raises `StopIteration`, the `for` loop catches it and terminates."

That's a **very strong interview answer**.

---

## 🧠 Remember this diagram

```text
for x in numbers:
        ↓
iter(numbers)
        ↓
   Iterator
        ↓
    next()
        ↓
      10
        ↓
    next()
        ↓
      20
        ↓
    next()
        ↓
      30
        ↓
    next()
        ↓
StopIteration
        ↓
   loop ends
```

### One-line memory trick:

**`for` doesn't directly iterate over the collection — it iterates over an iterator.**

---

Next is **Topic 3 — Iterator Protocol: `__iter__()` and `__next__()`**. This is where we'll understand exactly **how Python knows that an object is an iterator**.
