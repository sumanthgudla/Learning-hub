# Topic 8 — Generator Expressions ⭐

Generator expressions are basically the **generator version of list comprehensions**.

This is a very common Python interview topic.

---

## 1. First, normal list comprehension

Suppose we want squares:

```python
squares = [x * x for x in range(5)]
```

Result:

```text
[0, 1, 4, 9, 16]
```

The important thing is that the **list is created immediately**.

Conceptually:

```text
range(5)
   ↓
calculate 0²
calculate 1²
calculate 2²
calculate 3²
calculate 4²
   ↓
[0, 1, 4, 9, 16]
```

All results are stored.

---

# 2. Generator expression

Change the square brackets to parentheses:

```python
squares = (x * x for x in range(5))
```

Now `squares` is a **generator object**.

It doesn't immediately create:

```text
[0, 1, 4, 9, 16]
```

Instead, it produces values when requested.

```python
print(next(squares))
```

Output:

```text
0
```

Again:

```python
print(next(squares))
```

Output:

```text
1
```

Again:

```python
print(next(squares))
```

Output:

```text
4
```

---

# 3. Side-by-side

### List comprehension

```python
squares = [x * x for x in range(5)]
```

```text
Creates all values
       ↓
[0, 1, 4, 9, 16]
       ↓
Stores them
```

### Generator expression

```python
squares = (x * x for x in range(5))
```

```text
Generator object
       ↓
next() → 0
       ↓
next() → 1
       ↓
next() → 4
       ↓
next() → 9
       ↓
next() → 16
```

---

# 4. Memory difference ⭐

Consider:

```python
numbers = [x for x in range(10_000_000)]
```

The list stores all those values.

But:

```python
numbers = (x for x in range(10_000_000))
```

stores a generator that can produce the values as needed.

So:

```text
List comprehension
────────────────────────
10 million values
████████████████████████
       Memory


Generator expression
────────────────────────
Generator object
█
       Memory

values generated → consumed → generated → consumed
```

This is why generator expressions are useful when you **don't need all the results in memory at once**.

---

# 5. Is a generator expression a generator?

Yes.

```python
squares = (x * x for x in range(5))
```

`squares` is a generator object.

Therefore:

```python
next(squares)
```

works.

And:

```python
for x in squares:
    print(x)
```

works.

---

# 6. Generator expression vs generator function

There are actually two common ways to create generators.

### Generator function

Uses `yield`:

```python
def squares():
    for x in range(5):
        yield x * x
```

### Generator expression

Uses parentheses:

```python
squares = (x * x for x in range(5))
```

Both produce values lazily.

---

# 7. When should you use each?

### Simple transformation → generator expression

```python
squares = (x * x for x in range(1000000))
```

Very concise.

### More complex logic → generator function

```python
def process_numbers(numbers):
    for x in numbers:
        if x % 2 == 0:
            result = x * 10

            if result > 100:
                yield result
```

A generator function is easier to read when you have:

* multiple conditions
* multiple statements
* complex processing
* `try/except`
* stateful logic

---

# 8. Important example with `sum()`

Here's where generator expressions become really useful.

You can write:

```python
total = sum(x * x for x in range(1000000))
```

Notice:

```python
(x * x for x in range(1000000))
```

doesn't need to be converted into a list first.

Avoid unnecessarily doing:

```python
total = sum([x * x for x in range(1000000)])
```

The generator version can produce each square as `sum()` consumes it.

Conceptually:

```text
generator
    ↓
0 → sum
1 → sum
4 → sum
9 → sum
...
```

rather than building a huge intermediate list.

---

# 9. Important interview trap ⚠️

Look at this:

```python
numbers = (x for x in range(3))

print(list(numbers))
print(list(numbers))
```

What happens?

First:

```text
[0, 1, 2]
```

Second:

```text
[]
```

Why?

Because the generator has already been **exhausted**.

Remember:

```text
Generator
0 → 1 → 2 → StopIteration
```

It doesn't automatically restart.

If you need to iterate again, create another generator:

```python
numbers = (x for x in range(3))

print(list(numbers))

numbers = (x for x in range(3))

print(list(numbers))
```

Now both produce:

```text
[0, 1, 2]
[0, 1, 2]
```

---

# 10. List comprehension vs generator expression

|                            | List Comprehension | Generator Expression  |
| -------------------------- | ------------------ | --------------------- |
| Syntax                     | `[ ]`              | `( )`                 |
| Produces                   | List               | Generator             |
| Evaluation                 | Immediate          | Lazy                  |
| Memory                     | Stores results     | Produces on demand    |
| `next()`                   | ❌                  | ✅                     |
| Can iterate multiple times | ✅                  | ❌ after exhaustion    |
| Best for                   | Need all results   | Process progressively |

---

# 🎯 Interview questions

### Q1. What's the difference between these?

```python
[x * 2 for x in numbers]
```

and

```python
(x * 2 for x in numbers)
```

Strong answer:

> The first creates a list immediately and stores all results. The second creates a generator that evaluates lazily and produces each result only when requested.

---

### Q2. Why are generator expressions memory efficient?

> Because they don't create and store the entire result set. They produce one value at a time as requested.

---

### Q3. Can you call `next()` on a list?

```python
numbers = [1, 2, 3]

next(numbers)
```

❌ No.

But:

```python
numbers = (x for x in [1, 2, 3])

next(numbers)
```

✅ Yes.

Because the second is a generator/iterator.

---

## 🧠 The simplest way to remember

```text
[ ] → "Give me ALL results now"

( ) → "Give me results ONE AT A TIME"
```

For example:

```python
[x * 2 for x in range(1000000)]
```

means:

> Build all of them.

While:

```python
(x * 2 for x in range(1000000))
```

means:

> I'll ask for them when I need them.

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
8. Generator Expressions       ✅
9. yield from                  ⬅️ NEXT
10. Real-world + Interview
```

Next is **`yield from`**. It's a small topic, but useful for understanding how **one generator can delegate to another generator**.
