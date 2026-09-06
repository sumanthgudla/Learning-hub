# Topic 3 — Iterator Protocol: `__iter__()` and `__next__()`

Now we're getting to the **actual mechanics behind iterators**.

You already know:

```python
iter()
next()
```

But Python internally uses two special methods:

```python
__iter__()
__next__()
```

---

## 1. `iter()` calls `__iter__()`

When you write:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)
```

Python conceptually does:

```python
iterator = numbers.__iter__()
```

So:

```text
iter(numbers)
     ↓
numbers.__iter__()
     ↓
Iterator
```

---

## 2. `next()` calls `__next__()`

When you write:

```python
next(iterator)
```

Python conceptually does:

```python
iterator.__next__()
```

So:

```text
next(iterator)
      ↓
iterator.__next__()
      ↓
next value
```

Therefore:

```text
iter()  → __iter__()
next()  → __next__()
```

This is extremely important.

---

# 3. What makes an object an iterator?

An iterator follows the **iterator protocol**.

It needs two methods:

```python
__iter__()
__next__()
```

For example:

```python
class MyIterator:

    def __iter__(self):
        return self

    def __next__(self):
        ...
```

The important part is:

```python
__iter__() → returns an iterator
__next__() → returns the next value
```

---

# 4. Let's build a simple iterator

We'll create an iterator that produces:

```text
1
2
3
```

Code:

```python
class MyIterator:

    def __init__(self):
        self.number = 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.number <= 3:
            value = self.number
            self.number += 1
            return value

        raise StopIteration
```

Now:

```python
it = MyIterator()

print(next(it))
print(next(it))
print(next(it))
```

Output:

```text
1
2
3
```

Another:

```python
print(next(it))
```

gives:

```text
StopIteration
```

---

# 5. Understand what is happening

Initially:

```python
self.number = 1
```

Then:

```python
next(it)
```

calls:

```python
it.__next__()
```

Inside:

```python
value = self.number
```

So:

```text
value = 1
```

Then:

```python
self.number += 1
```

Now:

```text
number = 2
```

and returns:

```text
1
```

---

Next call:

```python
next(it)
```

returns:

```text
2
```

and updates the state:

```text
number = 3
```

Next:

```text
3
```

and:

```text
number = 4
```

Next call:

```python
next(it)
```

checks:

```python
if self.number <= 3:
```

which is false.

So:

```python
raise StopIteration
```

---

# 6. Now the `for` loop makes sense

If we do:

```python
it = MyIterator()

for x in it:
    print(x)
```

Python essentially does:

```python
iterator = iter(it)
```

which calls:

```python
it.__iter__()
```

which returns:

```python
it
```

Then repeatedly:

```python
next(iterator)
```

which calls:

```python
iterator.__next__()
```

Eventually:

```python
__next__()
```

raises:

```python
StopIteration
```

and the loop stops.

---

# 7. Why does `__iter__()` return `self`?

This is one of the most common interview questions.

For an iterator:

```python
def __iter__(self):
    return self
```

Why?

Because **the iterator itself is already the object that knows how to produce the next value**.

For example:

```text
MyIterator
    |
    ├── current state
    |
    └── __next__()
```

So when Python asks:

> "Give me your iterator."

It says:

> "I am already the iterator. Return myself."

Hence:

```python
return self
```

---

# 8. Iterable vs Iterator — deeper understanding

Now we can distinguish them more precisely.

### Iterable

Has:

```python
__iter__()
```

which gives you an iterator.

Example:

```python
numbers = [1, 2, 3]
```

You can do:

```python
iter(numbers)
```

### Iterator

Has:

```python
__iter__()
__next__()
```

Example:

```python
it = iter(numbers)
```

You can do:

```python
next(it)
```

---

## 9. The relationship

Think:

```text
ITERABLE
   |
   | __iter__()
   ↓
ITERATOR
   |
   | __next__()
   ↓
VALUE
```

And the iterator itself:

```text
Iterator
   |
   ├── __iter__() → self
   |
   └── __next__() → next value
```

---

# 10. Interview trap ⚠️

Interviewer:

> "What are the two methods required by the iterator protocol?"

Answer:

```text
__iter__()
__next__()
```

Then they might ask:

> "What should `__iter__()` return for an iterator?"

Answer:

> **The iterator itself (`self`).**

And:

> "What happens when there are no more values?"

Answer:

> **`__next__()` raises `StopIteration`.**

---

# 🧠 Remember these four lines

```python
iter(obj)       → obj.__iter__()
next(iterator)  → iterator.__next__()

__iter__()      → iterator
__next__()      → next value
```

And:

```text
No more values
      ↓
StopIteration
      ↓
for loop stops
```

### The complete picture so far

```text
Iterable
   │
   │ iter()
   ↓
__iter__()
   │
   ↓
Iterator
   │
   │ next()
   ↓
__next__()
   │
   ↓
Value
   │
   └── eventually → StopIteration
```

**Next: Topic 4 — Building a Custom Iterator from scratch**, where we'll write a practical iterator and understand every line of it.
