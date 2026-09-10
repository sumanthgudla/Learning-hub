# Topic 5 — `StopIteration`

This topic is short but **very important** because it completes the iterator mechanism.

---

## 1. What is `StopIteration`?

`StopIteration` is a special exception that means:

> **"There are no more values to produce."**

An iterator's `__next__()` method raises it when iteration is finished.

Example:

```python
numbers = iter([10, 20, 30])

print(next(numbers))  # 10
print(next(numbers))  # 20
print(next(numbers))  # 30
print(next(numbers))  # StopIteration
```

The fourth `next()` has nothing left to return.

---

# 2. Who raises `StopIteration`?

The **iterator's `__next__()` method**.

Remember our custom iterator:

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

Look at the final line:

```python
raise StopIteration
```

That's telling Python:

> "I've finished producing values."

---

# 3. What does `for` do with it?

This is the important part.

You write:

```python
for x in Counter(3):
    print(x)
```

Python roughly does:

```python
iterator = iter(Counter(3))

while True:
    try:
        x = next(iterator)
        print(x)
    except StopIteration:
        break
```

So when:

```python
next(iterator)
```

raises:

```text
StopIteration
```

the `for` loop effectively does:

```python
break
```

and finishes.

That's why you **don't see an error**.

---

# 4. But if I call `next()` myself?

Then Python doesn't automatically hide it.

```python
numbers = iter([10, 20])

print(next(numbers))
print(next(numbers))
print(next(numbers))
```

Output:

```text
10
20
StopIteration
```

Technically, the program raises the exception.

If you don't handle it, execution stops there.

---

# 5. You can catch it yourself

```python
numbers = iter([10, 20])

while True:
    try:
        value = next(numbers)
        print(value)

    except StopIteration:
        print("Finished!")
        break
```

Output:

```text
10
20
Finished!
```

This is basically what the `for` loop is doing internally.

---

# 6. Why not return `None` instead?

Very important interview question.

Imagine your iterator contains:

```python
[10, 20, None, 40]
```

If `__next__()` returned `None` to mean:

> "I'm finished"

there would be a problem.

Because `None` could actually be a **valid value**.

```text
10
20
None    ← actual data
40
```

So Python needs a special signal that cannot be confused with a normal returned value.

That signal is:

```python
StopIteration
```

---

# 7. `return` vs `raise StopIteration`

Inside `__next__()`:

```python
return value
```

means:

> "Here is another value."

Whereas:

```python
raise StopIteration
```

means:

> "There are no more values."

So:

```text
__next__()
   │
   ├── return 10
   ├── return 20
   ├── return 30
   │
   └── raise StopIteration
```

---

# 8. Very important distinction

Don't say:

> "`StopIteration` is returned."

❌ That's incorrect.

Say:

> **"`StopIteration` is raised by `__next__()` when there are no more values."**

That's the technically correct interview answer.

---

# 9. What happens if you call `next()` after exhaustion?

Consider:

```python
numbers = iter([10, 20])

next(numbers)  # 10
next(numbers)  # 20
```

Now exhausted.

```python
next(numbers)
```

raises `StopIteration`.

And importantly, calling it again:

```python
next(numbers)
```

still raises `StopIteration`.

The iterator doesn't restart.

```text
10 → 20 → exhausted

next() → StopIteration
next() → StopIteration
next() → StopIteration
```

To start again, you generally need a **new iterator**:

```python
numbers = [10, 20]

it1 = iter(numbers)
it2 = iter(numbers)
```

`it2` starts from the beginning.

---

# 10. The complete iterator lifecycle

You can now understand the entire process:

```text
Iterable
   │
   │ iter()
   ↓
Iterator
   │
   │ next()
   ↓
value
   │
   │ next()
   ↓
value
   │
   │ next()
   ↓
value
   │
   │ next()
   ↓
StopIteration
   │
   ↓
for loop ends
```

---

## 🎯 Interview questions you should be able to answer

### Q1. What is `StopIteration`?

> An exception used by an iterator to signal that there are no more values.

### Q2. Who raises it?

> `__next__()` raises `StopIteration` when iteration is exhausted.

### Q3. Who handles it in a `for` loop?

> The `for` loop handles it internally and terminates the loop.

### Q4. Why not return `None`?

> Because `None` could be a legitimate value in the iterable.

### Q5. Does an exhausted iterator restart?

> No. Once exhausted, subsequent `next()` calls continue to raise `StopIteration`. A new iterator is needed to start again.

---

## 🧠 One thing to memorize

```text
__next__()
   ↓
Has value?
   ↓ YES
return value
   ↓
Has value?
   ↓ NO
raise StopIteration
   ↓
for loop stops
```

### Progress

```text
1. Iterable vs Iterator       ✅
2. for loop internally       ✅
3. Iterator Protocol          ✅
4. Custom Iterator            ✅
5. StopIteration              ✅
6. Generators + yield         ⬅️ NEXT
7. Generator vs Iterator
8. Generator Expressions
9. yield from
10. Real-world + Interview
```

**Next is the big one: Generators and `yield`.** This is where you'll see why Python gives us a much easier way to create iterators without writing all that `__iter__()` / `__next__()` code.
