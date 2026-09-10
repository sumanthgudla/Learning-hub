# Topic 9 — `yield from` ⭐

`yield from` is actually a **small concept**.

Its main purpose is:

> **Let one generator yield all the values from another iterable/generator.**

---

## 1. First, without `yield from`

Suppose we have:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Now we want another generator that produces those same values.

We could write:

```python
def all_numbers():
    for x in numbers():
        yield x
```

Usage:

```python
for x in all_numbers():
    print(x)
```

Output:

```text
1
2
3
```

The outer generator is basically saying:

> "Take every value from `numbers()` and yield it."

---

# 2. `yield from` simplifies this

Instead of:

```python
def all_numbers():
    for x in numbers():
        yield x
```

we can write:

```python
def all_numbers():
    yield from numbers()
```

That's it.

Output is still:

```text
1
2
3
```

So:

```python
yield from numbers()
```

roughly means:

```python
for x in numbers():
    yield x
```

---

# 3. Simple example

```python
def first():
    yield 1
    yield 2

def second():
    yield 3
    yield 4

def combined():
    yield from first()
    yield from second()
```

Now:

```python
for x in combined():
    print(x)
```

Output:

```text
1
2
3
4
```

Execution:

```text
combined()
    ↓
yield from first()
    ↓
1
2
    ↓
yield from second()
    ↓
3
4
```

---

# 4. You can use it with normal iterables too

It doesn't have to be another generator.

For example:

```python
def numbers():
    yield from [10, 20, 30]
```

Then:

```python
for x in numbers():
    print(x)
```

Output:

```text
10
20
30
```

You can also use:

```python
yield from (1, 2, 3)
```

or:

```python
yield from range(5)
```

So `yield from` can delegate to an **iterable**.

---

# 5. Why does `yield from` exist?

Imagine you have nested data:

```python
groups = [
    [1, 2, 3],
    [4, 5],
    [6, 7, 8]
]
```

You want one generator that produces:

```text
1
2
3
4
5
6
7
8
```

You could write:

```python
def flatten(groups):
    for group in groups:
        for item in group:
            yield item
```

That's perfectly valid.

But:

```python
def flatten(groups):
    for group in groups:
        yield from group
```

is cleaner.

---

# 6. Let's understand the execution

```python
def flatten(groups):
    for group in groups:
        yield from group
```

Suppose:

```python
groups = [
    [1, 2],
    [3, 4]
]
```

First:

```text
group = [1, 2]
```

Then:

```python
yield from group
```

produces:

```text
1
2
```

Then:

```text
group = [3, 4]
```

and:

```python
yield from group
```

produces:

```text
3
4
```

Final result:

```text
1
2
3
4
```

---

# 7. `yield from` does NOT create a nested result

This is important.

Suppose:

```python
def numbers():
    yield from [1, 2, 3]
```

It does **not** produce:

```text
[1, 2, 3]
```

as one value.

Instead it produces:

```text
1
2
3
```

one at a time.

Think:

```text
yield [1, 2, 3]
        ↓
ONE value
        ↓
[1, 2, 3]


yield from [1, 2, 3]
        ↓
THREE values
        ↓
1
2
3
```

🔥 This distinction is worth remembering.

---

# 8. `yield` vs `yield from`

This is a common interview question.

### `yield`

```python
def test():
    yield [1, 2, 3]
```

Calling:

```python
list(test())
```

gives:

```python
[[1, 2, 3]]
```

Because the **whole list is one yielded value**.

---

### `yield from`

```python
def test():
    yield from [1, 2, 3]
```

Then:

```python
list(test())
```

gives:

```python
[1, 2, 3]
```

Because each element is yielded separately.

---

# 9. Think of it as delegation

The best mental model:

```text
Generator A
     │
     │ yield from
     ↓
Generator B
     │
     ├── value 1
     ├── value 2
     └── value 3
```

Generator A says:

> "For now, Generator B will handle producing the values."

Once B finishes, A continues.

Example:

```python
def child():
    yield 1
    yield 2

def parent():
    print("Start")
    yield from child()
    print("End")
```

Execution:

```python
g = parent()

next(g)
```

prints:

```text
Start
```

and returns:

```text
1
```

Next:

```python
next(g)
```

returns:

```text
2
```

Next:

```python
next(g)
```

Now the child is finished, so the parent continues:

```text
End
```

and then the generator finishes.

So `yield from` **temporarily delegates iteration to another iterable**.

---

# 10. Interview answer 🎯

### Q: What is `yield from`?

Strong answer:

> "`yield from` allows a generator to delegate yielding values to another iterable or generator. It is roughly equivalent to iterating over that object and yielding each value individually, but it provides cleaner generator composition."

### Q: Difference between `yield` and `yield from`?

> "`yield` produces the object itself as a single value, while `yield from` produces each value from the supplied iterable individually."

Example:

```python
yield [1, 2, 3]
```

→ one value:

```text
[1, 2, 3]
```

while:

```python
yield from [1, 2, 3]
```

→ three values:

```text
1
2
3
```

---

## 🧠 Remember this

```text
yield
 ↓
"Give this object as ONE value"

yield from
 ↓
"Give me everything inside this iterable"
```

And:

```python
yield from other_generator()
```

is roughly:

```python
for value in other_generator():
    yield value
```

---

### Progress

```text
1. Iterable vs Iterator       ✅
2. for loop internally        ✅
3. Iterator Protocol           ✅
4. Custom Iterator             ✅
5. StopIteration               ✅
6. Generators + yield          ✅
7. Generator vs Iterator       ✅
8. Generator Expressions       ✅
9. yield from                  ✅
10. Real-world + Interview     ⬅️ NEXT
```

Next we'll finish the whole topic with **real-world generator use cases + the most important interview questions**, including some tricky execution-output questions.
