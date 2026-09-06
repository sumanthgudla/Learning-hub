# Topic 1 — Iterable vs Iterator

This is the **foundation**. Once this is clear, generators become much easier.

## 1. What is an Iterable?

An **iterable is an object that you can loop over**.

Examples:

```python
numbers = [1, 2, 3]

for x in numbers:
    print(x)
```

`list` is iterable.

Other common iterables:

```python
list
tuple
string
set
dictionary
range
```

For example:

```python
name = "Sumanth"

for char in name:
    print(char)
```

A string is also iterable.

---

# 2. What is an Iterator?

An **iterator is an object that gives you one value at a time**.

You create an iterator from an iterable using:

```python
iter()
```

Example:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)
```

Now:

```python
next(iterator)
```

gives:

```text
10
```

Again:

```python
next(iterator)
```

gives:

```text
20
```

Again:

```python
next(iterator)
```

gives:

```text
30
```

And one more time:

```python
next(iterator)
```

Python raises:

```text
StopIteration
```

---

# 3. The important relationship

Think of it this way:

```text
Iterable
   |
   | iter()
   ↓
Iterator
   |
   | next()
   ↓
value
```

Example:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))  # 10
print(next(iterator))  # 20
print(next(iterator))  # 30
```

### Interview definition

> **An iterable is an object that can return an iterator, while an iterator is an object that produces values one at a time using `next()`.**

---

# 4. Why do we need `iter()`?

This is an important question.

You have:

```python
numbers = [10, 20, 30]
```

The list itself contains the data.

But `next()` needs an **iterator** that keeps track of where it currently is.

```text
List
[10, 20, 30]
     ↓
    iter()
     ↓
Iterator
     ↓
position = 0

next() → 10
position = 1

next() → 20
position = 2

next() → 30
position = 3

next() → StopIteration
```

So the iterator maintains the **iteration state**.

---

# 5. Very important example

Look at this:

```python
numbers = [10, 20, 30]

print(next(numbers))
```

What happens?

❌ Error.

Something like:

```text
TypeError: 'list' object is not an iterator
```

Why?

Because:

```python
numbers
```

is an **iterable**, not an iterator.

We need:

```python
numbers = [10, 20, 30]

iterator = iter(numbers)

print(next(iterator))
```

Output:

```text
10
```

---

# 6. How do I check whether something is iterable?

You can use:

```python
iter(numbers)
```

If Python can create an iterator, it's iterable.

For example:

```python
numbers = [1, 2, 3]

iterator = iter(numbers)

print(iterator)
```

Works.

But more importantly, Python's iteration protocol is based on the object's `__iter__()` method.

We'll get into that in **Topic 3**.

---

# 7. A very important interview distinction

### Iterable

Can be passed to:

```python
for x in iterable:
```

Examples:

```python
list
tuple
string
set
dict
range
```

### Iterator

Can be passed to:

```python
next(iterator)
```

For example:

```python
numbers = [10, 20, 30]

it = iter(numbers)

next(it)
next(it)
```

---

# 8. One subtle point interviewers like

An iterator is also an iterable.

For example:

```python
numbers = [10, 20, 30]

it = iter(numbers)

print(iter(it) is it)
```

Output:

```text
True
```

Why?

Because an iterator needs to be usable in a `for` loop too.

So:

```text
Iterable
   ↓
can produce an Iterator

Iterator
   ↓
is itself Iterable
   ↓
produces values using next()
```

---

# 9. Real-world analogy

Imagine a **book**:

```text
Book = Iterable
```

The book contains all the pages.

Now you have a **bookmark**:

```text
Bookmark = Iterator
```

The bookmark remembers:

> "I'm currently on page 10."

Move forward:

```text
next() → page 11
next() → page 12
next() → page 13
```

The **book contains the data**.

The **bookmark maintains the current position**.

That's roughly the difference between an iterable and an iterator.

---

# 🎯 Interview question

If an interviewer asks:

> **What is the difference between an iterable and an iterator?**

A strong answer would be:

> "An iterable is an object that can be iterated over and can provide an iterator using `iter()`. An iterator is the object that actually maintains the iteration state and produces the next value using `next()`. Once there are no more values, it raises `StopIteration`."

And if they ask:

> **Is every iterator iterable?**

Say:

> "Yes. An iterator is also an iterable, because it implements the iteration protocol."

---

## 🧠 Remember just this

```text
Iterable → gives iterator
Iterator → gives values
iter()   → creates/gets iterator
next()   → gets next value
StopIteration → no more values
```

Next, **Topic 2: How exactly does a `for` loop work internally?** This is where `iter()` and `next()` will really click.
