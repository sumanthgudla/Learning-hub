# 3. Coroutine — 🔥 VERY IMPORTANT

A **coroutine** is a function that can **pause its execution and later resume from where it stopped**.

In Python, an `async def` function creates a coroutine.

```python
async def fetch_data():
    print("Start")
    await asyncio.sleep(2)
    print("End")
```

When you call:

```python
result = fetch_data()
```

you **don't execute the function immediately**.

You get a **coroutine object**:

```text
fetch_data()
     ↓
Coroutine object
```

To actually run it:

```python
import asyncio

asyncio.run(fetch_data())
```

---

## Normal function vs coroutine

### Normal function

```python
def hello():
    print("Hello")

hello()
```

Execution:

```text
hello()
 ↓
execute immediately
 ↓
"Hello"
 ↓
return
```

### Coroutine

```python
async def hello():
    print("Hello")

hello()
```

Execution:

```text
hello()
 ↓
create coroutine object
 ↓
NOT executed yet
```

You need something like:

```python
asyncio.run(hello())
```

to execute it.

---

# Why is a coroutine special?

The key feature is that it can **pause and resume**.

Example:

```python
async def fetch():
    print("Step 1")

    await asyncio.sleep(2)

    print("Step 2")
```

Execution:

```text
Step 1
   ↓
await asyncio.sleep(2)
   ↓
PAUSE
   ↓
event loop runs other tasks
   ↓
2 seconds pass
   ↓
RESUME
   ↓
Step 2
```

A normal function doesn't work this way with `await`.

---

# Coroutine ≠ Thread

This is a very important interview distinction.

A coroutine is **not a thread**.

You could have:

```text
1 Python thread
      |
      └── Event Loop
             |
             ├── Coroutine A
             ├── Coroutine B
             ├── Coroutine C
             └── Coroutine D
```

The event loop coordinates these coroutines.

For example:

```python
async def task_a():
    await asyncio.sleep(2)

async def task_b():
    await asyncio.sleep(2)

async def task_c():
    await asyncio.sleep(2)
```

They can all make progress while waiting for I/O.

This is **concurrency**, not necessarily parallel execution.

We'll cover that distinction later.

---

# Coroutine + `await`

Think of the relationship this way:

```text
async def
   ↓
creates coroutine
   ↓
await
   ↓
coroutine can pause
   ↓
event loop
   ↓
runs other available work
   ↓
awaited operation completes
   ↓
coroutine resumes
```

---

# ⭐ Common interview question

### Q: What is a coroutine in Python?

Good answer:

> "A coroutine is an asynchronous function defined using `async def`. Calling it returns a coroutine object. The coroutine can suspend its execution at an `await` expression and later resume when the awaited operation is ready. Coroutines are managed by an event loop and are commonly used for concurrent I/O operations."

---

## One important mistake to avoid

Don't say:

> "`async` creates a new thread."

❌ **Wrong.**

`async`/`await` is primarily about **cooperative concurrency using an event loop**, not automatically creating threads.

---

### Quick test

What do you think this prints?

```python
import asyncio

async def hello():
    print("Hello")

x = hello()

print("Done")
```

The answer is:

```text
Done
```

You **won't see `Hello`**, because the coroutine was created but never executed.

If you want to execute it:

```python
asyncio.run(hello())
```

Then:

```text
Hello
Done
```

**Next: Event Loop — the most important concept for understanding how `async` Python actually works.**
