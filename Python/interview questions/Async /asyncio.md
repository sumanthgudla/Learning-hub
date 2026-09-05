# 7. `asyncio` — 🔥 VERY IMPORTANT

`asyncio` is Python's built-in framework for writing **asynchronous, concurrent code**.

If `async`/`await` are the language features, think of `asyncio` as the **machinery that makes them work**.

---

## 1. Basic example

```python
import asyncio

async def hello():
    print("Hello")
    await asyncio.sleep(2)
    print("World")

asyncio.run(hello())
```

There are three important pieces here:

```text
async def
   ↓
defines coroutine

await
   ↓
allows coroutine to pause

asyncio
   ↓
provides event loop and async tools
```

---

# 2. `asyncio.run()`

You've already seen:

```python
asyncio.run(hello())
```

This is commonly used as the **entry point** for running an async program.

Conceptually:

```text
asyncio.run(hello())
        ↓
create/manage event loop
        ↓
run hello()
        ↓
coroutine executes
        ↓
complete
        ↓
event loop closes
```

So:

```python
async def hello():
    print("Hello")
```

doesn't execute by itself.

You can run it with:

```python
asyncio.run(hello())
```

---

# 3. Running multiple coroutines

Suppose we have:

```python
import asyncio

async def task_a():
    print("A started")
    await asyncio.sleep(2)
    print("A finished")

async def task_b():
    print("B started")
    await asyncio.sleep(1)
    print("B finished")
```

We can run them concurrently:

```python
async def main():
    await asyncio.gather(
        task_a(),
        task_b()
    )

asyncio.run(main())
```

Conceptually:

```text
asyncio.run(main())
        ↓
    Event Loop
        ↓
 ┌──────┴──────┐
 ↓             ↓
Task A       Task B
 ↓             ↓
await         await
 ↓             ↓
waiting       waiting
 ↓             ↓
resume        resume
```

---

# 4. `asyncio.sleep()`

This is one of the easiest ways to demonstrate async behavior.

```python
await asyncio.sleep(2)
```

This means:

> "Pause this coroutine for 2 seconds without blocking the event loop."

Compare:

```python
time.sleep(2)
```

with:

```python
await asyncio.sleep(2)
```

### `time.sleep()`

```text
Event Loop
    ↓
time.sleep(2)
    ↓
🚫 BLOCKED
```

### `asyncio.sleep()`

```text
Event Loop
    ↓
await asyncio.sleep(2)
    ↓
Coroutine pauses
    ↓
✅ Other tasks can run
```

---

# 5. Creating Tasks

`asyncio` also lets you create tasks.

```python
async def main():
    task1 = asyncio.create_task(task_a())
    task2 = asyncio.create_task(task_b())

    await task1
    await task2
```

Here:

```python
asyncio.create_task(...)
```

schedules a coroutine to run as an **asyncio Task**.

Think:

```text
Coroutine
    ↓
create_task()
    ↓
Task
    ↓
Event Loop schedules it
```

This distinction is useful:

```text
Coroutine → describes async work

Task → schedules that coroutine to run
```

---

# 6. Coroutine vs Task

This is a common interview follow-up.

### Coroutine

```python
coro = task_a()
```

You've created a coroutine object.

It isn't necessarily scheduled to run yet.

### Task

```python
task = asyncio.create_task(task_a())
```

Now you've asked the event loop to schedule that coroutine as a task.

Simplified:

```text
task_a()
   ↓
Coroutine object
   ↓
create_task()
   ↓
Task
   ↓
Event Loop
   ↓
Execution
```

---

# 7. `asyncio.gather()`

You've already seen:

```python
await asyncio.gather(
    task_a(),
    task_b()
)
```

`gather()` is commonly used when you want to **run multiple awaitables concurrently and collect their results**.

Example:

```python
async def get_user():
    await asyncio.sleep(1)
    return "Sumanth"

async def get_orders():
    await asyncio.sleep(2)
    return ["Order1", "Order2"]

async def main():
    user, orders = await asyncio.gather(
        get_user(),
        get_orders()
    )

    print(user)
    print(orders)

asyncio.run(main())
```

Instead of:

```python
user = await get_user()
orders = await get_orders()
```

which is sequential, `gather()` allows both operations to be in progress concurrently.

---

# 8. AI Engineer example

Imagine an agent needs:

```text
User
 ↓
Agent
 ├── Get customer profile
 ├── Search vector DB
 └── Call recommendation API
```

If these operations don't depend on each other:

```python
profile, documents, recommendations = await asyncio.gather(
    get_customer_profile(),
    search_vector_db(),
    get_recommendations()
)
```

This is a very realistic async pattern in AI systems.

Instead of:

```text
Profile       █████
Vector DB          █████
Recommendation          █████
```

you can have:

```text
Profile       █████
Vector DB     ███████
Recommendation ██████
```

The total time can approach the **slowest operation**, rather than the sum of all three, assuming the operations are truly independent and I/O-bound.

---

# ⚠️ But don't blindly use `gather()`

Suppose:

```python
user = await get_user()
orders = await get_orders(user)
```

Here the second operation depends on the first.

You **cannot meaningfully parallelize them**:

```text
get_user()
   ↓
need user
   ↓
get_orders(user)
```

So:

```python
user = await get_user()
orders = await get_orders(user)
```

is appropriate.

### Rule:

> **Use concurrency when operations are independent.**

---

# 9. `asyncio` does NOT make blocking code magically async

This is extremely important.

Bad:

```python
async def main():
    result = requests.get(url)
```

`requests.get()` is still blocking.

You have:

```text
asyncio
   ↓
requests.get()
   ↓
🚨 blocks event loop
```

If you have a synchronous blocking library that you cannot replace, one option is to run that blocking work outside the event loop, for example with:

```python
await asyncio.to_thread(blocking_function)
```

Example:

```python
import asyncio
import requests

def fetch():
    return requests.get("https://example.com")

async def main():
    response = await asyncio.to_thread(fetch)
    print(response.status_code)

asyncio.run(main())
```

Here the blocking function runs in a worker thread rather than directly blocking the event loop.

You don't need to memorize this deeply yet—we'll come back to it when we discuss handling blocking code.

---

# ⭐ Interview questions

### Q: What is `asyncio`?

> "`asyncio` is Python's standard library framework for asynchronous programming. It provides the event loop, tasks, futures, and utilities such as `gather()` for coordinating concurrent asynchronous operations."

### Q: What does `asyncio.run()` do?

> "It runs an async entry-point coroutine, managing the event loop for that execution and closing the loop when the coroutine completes."

### Q: What is `asyncio.gather()` used for?

> "It allows multiple awaitables to execute concurrently and returns their results together."

### Q: Does `asyncio` create multiple threads?

> "Not by default. asyncio primarily uses an event loop, typically running in a single thread. It provides concurrency for asynchronous operations without requiring one thread per task."

---

## 🧠 Your async Python mental model so far

```text
1. async
   ↓
defines coroutine function

2. await
   ↓
allows coroutine to suspend

3. Coroutine
   ↓
async work that can pause/resume

4. Event Loop
   ↓
manages and schedules async work

5. Blocking I/O
   ↓
can freeze the event loop

6. Concurrency
   ↓
multiple tasks can make progress

7. asyncio
   ↓
provides the machinery for all of this
```

### Next topic: `asyncio.gather()` in depth

We'll specifically cover **sequential vs concurrent execution, return values, exceptions, timing, and the interview traps around `gather()`**.
