# Topic 10 — Real-World Uses + Interview Questions

This is the **final topic** in Iterators + Generators. Let's connect everything you've learned to real production scenarios and interview questions.

---

## 1. Real-world use case: Reading a huge file

Suppose you have a **10 GB log file**.

### ❌ Bad approach

```python
with open("app.log") as file:
    data = file.readlines()

for line in data:
    process(line)
```

`readlines()` loads **all lines into memory**.

If the file is huge, this can consume a lot of memory.

### ✅ Better approach

```python
with open("app.log") as file:
    for line in file:
        process(line)
```

A file object is iterable and gives you lines incrementally.

You can also create your own generator:

```python
def read_logs(filename):
    with open(filename) as file:
        for line in file:
            yield line
```

Then:

```python
for line in read_logs("app.log"):
    process(line)
```

### What happens?

```text
read one line
     ↓
process line
     ↓
read next line
     ↓
process line
     ↓
...
```

You don't need to keep the entire 10 GB file in memory.

---

# 2. Database records

Imagine a database contains **10 million customers**.

### ❌ Bad

```python
customers = get_all_customers()

for customer in customers:
    process(customer)
```

If `get_all_customers()` returns 10 million records as a list, memory usage can become huge.

### ✅ Generator approach

```python
def get_customers():
    for customer in database:
        yield customer
```

Then:

```python
for customer in get_customers():
    process(customer)
```

The application processes records incrementally.

In real systems, databases often use **pagination, cursors, or batching** rather than literally fetching one row at a time, but the generator pattern can sit on top of those mechanisms.

---

# 3. API pagination

Suppose an API returns 100 users per request.

You want to process 100,000 users.

You could create a generator:

```python
def get_users():
    page = 1

    while True:
        users = fetch_users(page)

        if not users:
            break

        for user in users:
            yield user

        page += 1
```

Then:

```python
for user in get_users():
    process(user)
```

The caller doesn't need to know about pagination.

The generator hides this complexity.

```text
Caller
  ↓
get_users()
  ↓
API page 1
  ↓
yield users
  ↓
API page 2
  ↓
yield users
  ↓
API page 3
  ↓
...
```

This is a very good **interview example**.

---

# 4. Generator pipelines

Generators become especially powerful when you **chain them together**.

Imagine:

```text
Data
 ↓
Filter
 ↓
Transform
 ↓
Process
```

Example:

```python
def numbers():
    for i in range(10):
        yield i


def even_numbers(numbers):
    for n in numbers:
        if n % 2 == 0:
            yield n


def square(numbers):
    for n in numbers:
        yield n * n
```

Pipeline:

```python
data = numbers()
data = even_numbers(data)
data = square(data)

for value in data:
    print(value)
```

Output:

```text
0
4
16
36
64
```

### Important point

The whole pipeline doesn't execute immediately.

When:

```python
data = square(data)
```

happens, you're mostly **building the pipeline**.

Execution happens when:

```python
for value in data:
```

starts requesting values.

---

# 5. Let's understand the execution

Suppose we ask for the first value:

```python
next(data)
```

The request flows backwards:

```text
next(square_generator)
        ↓
next(even_numbers_generator)
        ↓
next(numbers_generator)
        ↓
0
```

`0` is even:

```python
0 * 0
```

so:

```text
0
```

is returned.

Then another `next()` continues from where each generator paused.

This is called **lazy evaluation**.

---

# 6. Why are generators memory efficient?

Consider:

```python
numbers = [x * x for x in range(1000000)]
```

Python creates and stores all one million results.

With:

```python
numbers = (x * x for x in range(1000000))
```

Python doesn't create all one million results immediately.

Instead:

```text
request value
     ↓
calculate value
     ↓
return value
     ↓
pause
     ↓
request next value
     ↓
calculate next value
```

Therefore generators are particularly useful when:

* Dataset is large
* You only need one item at a time
* Data arrives as a stream
* You don't need random access
* You want processing pipelines

---

# 7. Can you access a generator using an index?

Suppose:

```python
numbers = (x * x for x in range(5))
```

Can you do:

```python
numbers[2]
```

❌ No.

You'll get:

```text
TypeError
```

Why?

Because a generator is not a sequence with stored elements.

You consume it sequentially:

```python
next(numbers)
```

or:

```python
for n in numbers:
    print(n)
```

---

# 8. Can you restart a generator?

Consider:

```python
numbers = (x for x in range(3))

print(list(numbers))
print(list(numbers))
```

Output:

```text
[0, 1, 2]
[]
```

Why?

Because the generator was already consumed.

```text
Generator
   ↓
0
   ↓
1
   ↓
2
   ↓
exhausted
```

To start again, create a **new generator**:

```python
numbers = (x for x in range(3))

print(list(numbers))

numbers = (x for x in range(3))

print(list(numbers))
```

Output:

```text
[0, 1, 2]
[0, 1, 2]
```

---

# 9. Important interview question: `yield` vs `return`

### `return`

```python
def test():
    return 10
```

The function executes and finishes.

### `yield`

```python
def test():
    yield 10
```

The function produces a value and **pauses**.

```text
yield
 ↓
pause
 ↓
remember state
 ↓
next()
 ↓
resume
```

### Interview answer

> `return` terminates the function and returns a value, whereas `yield` produces a value while preserving the generator's execution state so it can resume later.

---

# 10. Tricky interview question

What is the output?

```python
def test():
    print("A")
    yield 1
    print("B")
    yield 2
    print("C")

g = test()

print("X")
print(next(g))
print("Y")
print(next(g))
print("Z")
```

Let's execute carefully.

### Step 1

```python
g = test()
```

Nothing prints.

Because generator functions don't execute their body when called.

---

### Step 2

```python
print("X")
```

Output:

```text
X
```

---

### Step 3

```python
print(next(g))
```

Generator starts:

```python
print("A")
```

prints:

```text
A
```

Then:

```python
yield 1
```

returns `1`.

So:

```text
1
```

Output so far:

```text
X
A
1
```

---

### Step 4

```python
print("Y")
```

```text
Y
```

---

### Step 5

```python
print(next(g))
```

Execution resumes **after**:

```python
yield 1
```

So:

```python
print("B")
```

prints:

```text
B
```

Then:

```python
yield 2
```

returns `2`.

So:

```text
2
```

Final output:

```text
X
A
1
Y
B
2
Z
```

The key concept is:

> **A generator remembers exactly where it paused.**

---

# 11. Most important interview questions

You should be able to answer these without hesitation.

### Q1. What is an iterable?

An object that can return an iterator and therefore can be iterated over.

Examples:

```python
list
tuple
string
set
dict
range
```

---

### Q2. What is an iterator?

An object that implements:

```python
__iter__()
__next__()
```

and produces values one at a time.

---

### Q3. What does `iter()` do?

It obtains an iterator from an iterable.

```python
iterator = iter([1, 2, 3])
```

---

### Q4. What does `next()` do?

It asks the iterator for its next value.

```python
next(iterator)
```

---

### Q5. What is `StopIteration`?

It's the exception raised by an iterator when there are no more values.

A `for` loop catches it internally.

---

### Q6. What is a generator?

A generator is a special iterator created using a function containing `yield`.

---

### Q7. Is every iterator a generator?

❌ No.

But:

> **Every generator is an iterator.**

---

### Q8. Why use generators?

Main reasons:

* Lazy evaluation
* Memory efficiency
* Streaming
* Large datasets
* Data pipelines

---

### Q9. What is a generator expression?

Example:

```python
(x * x for x in range(10))
```

It creates a generator without explicitly defining a generator function.

---

### Q10. Difference between list comprehension and generator expression?

```python
[x * x for x in range(10)]
```

creates a list immediately.

```python
(x * x for x in range(10))
```

produces values lazily.

---

### Q11. What does `yield from` do?

It delegates yielding to another iterable or generator.

```python
yield from other_generator()
```

instead of:

```python
for x in other_generator():
    yield x
```

---

### Q12. Can generators be indexed?

❌ No.

```python
g[2]
```

doesn't work.

---

### Q13. Can a generator be reused?

Not after it's exhausted.

You need to create another generator.

---

# Final Mental Model

You can remember the entire topic like this:

```text
ITERABLE
   │
   │ iter()
   ↓
ITERATOR
   │
   │ next()
   ↓
VALUE
   │
   │ next()
   ↓
VALUE
   │
   │ next()
   ↓
StopIteration
```

And:

```text
GENERATOR
   │
   │ created using yield
   ↓
ITERATOR
   │
   │ next()
   ↓
yield value
   │
   ↓
pause + remember state
   │
   │ next()
   ↓
resume
```

### The one sentence I'd want you to remember for interviews:

> **An iterable can provide an iterator, an iterator produces values through `__next__()`, and a generator is a convenient way to create such an iterator using `yield`, with lazy evaluation and automatic state management.**

You've now completed the **10/10 Iterators + Generators roadmap**. The next high-value Python topic for your interview prep would be **Exception Handling (`try`, `except`, `else`, `finally`, custom exceptions)**—especially because `try-else` was one of the things you recently missed in an interview.
