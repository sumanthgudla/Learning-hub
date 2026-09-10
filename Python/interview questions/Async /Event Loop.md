# 4. Event Loop — 🔥🔥 MOST IMPORTANT

If you understand the **event loop**, async Python becomes much easier.

The **event loop** is the mechanism that manages and schedules asynchronous tasks.

Think of it as a **manager**:

```text
                 EVENT LOOP
                     |
       ┌─────────────┼─────────────┐
       ↓             ↓             ↓
   Coroutine A   Coroutine B   Coroutine C
       |             |             |
    API call      DB call       API call
       ↓             ↓             ↓
    waiting       waiting       waiting
```

When one coroutine is waiting for I/O, the event loop can give another coroutine a chance to run.

---

## Simple example

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

If we run them concurrently:

```python
async def main():
    await asyncio.gather(task_a(), task_b())

asyncio.run(main())
```

Conceptually:

```text
Event Loop
    |
    ├── task_a
    |     ↓
    |   sleep(2)
    |     ↓
    |   waiting
    |
    └── task_b
          ↓
        sleep(1)
          ↓
        waiting
```

The event loop doesn't just sit there waiting for `task_a`.

It can handle `task_b`.

After one second:

```text
B finished
```

After another second:

```text
A finished
```

---

# Why is it called a "loop"?

Because conceptually it repeatedly checks:

```text
Is there work I can execute?
        ↓
Execute it
        ↓
Is something waiting for I/O ready?
        ↓
Resume it
        ↓
Repeat...
```

Simplified:

```text
┌─────────────────────────┐
│       Event Loop        │
│                         │
│  Check ready tasks      │
│          ↓              │
│  Run a little           │
│          ↓              │
│  Check I/O              │
│          ↓              │
│  Resume ready tasks     │
│          ↓              │
│        Repeat           │
└─────────────────────────┘
```

---

# 🔥 The most important concept: `await` gives control back

Consider:

```python
async def fetch():
    response = await call_api()
    print(response)
```

When Python reaches:

```python
await call_api()
```

the coroutine may have to wait for the network.

Instead of blocking the entire event loop, the coroutine **suspends** and the event loop can run other ready tasks.

```text
Coroutine A
    |
    | await API
    ↓
PAUSED
    |
    ↓
Event Loop
    |
    ├── Run Coroutine B
    ├── Run Coroutine C
    └── Handle I/O
```

When the API response is ready:

```text
API response ready
       ↓
Event loop
       ↓
Resume Coroutine A
       ↓
print(response)
```

---

# ⚠️ Blocking code can freeze the event loop

This is **very important for interviews**.

Suppose:

```python
import time

async def task():
    print("Start")

    time.sleep(5)

    print("End")
```

You might think:

> "It's an async function, so other tasks can run."

❌ Not here.

`time.sleep(5)` is **blocking**.

The event loop gets stuck:

```text
Event Loop
    ↓
task()
    ↓
time.sleep(5)
    ↓
🚫 BLOCKED
    ↓
Other async tasks cannot run
```

Instead use:

```python
await asyncio.sleep(5)
```

Now:

```text
Event Loop
    ↓
await asyncio.sleep(5)
    ↓
task pauses
    ↓
Event Loop is free
    ↓
run other tasks
```

---

# 🔥 Interview question

### "Can synchronous code run inside an async function?"

**Yes.**

For example:

```python
async def process():
    x = 10
    y = 20

    print(x + y)

    await some_api()
```

The `print()` and calculations are synchronous.

That's perfectly fine.

The problem is **blocking synchronous operations**, such as:

```python
time.sleep()
requests.get()
heavy_cpu_calculation()
```

These can block the event loop.

---

# Event Loop vs Thread

This distinction is frequently asked.

### Traditional threading

```text
Thread 1 → Task A
Thread 2 → Task B
Thread 3 → Task C
```

### Asyncio

```text
One thread
    ↓
Event Loop
    ↓
Coroutine A
Coroutine B
Coroutine C
Coroutine D
```

The event loop coordinates coroutines **cooperatively**.

A coroutine generally needs to reach an `await` point to give the event loop an opportunity to run other tasks.

---

# AI Engineer example

Imagine your agent needs to call three services:

```text
Agent
 |
 ├── Azure OpenAI
 |
 ├── Vector DB
 |
 └── External REST API
```

Each may involve network waiting.

Async can allow the application to efficiently handle those waits:

```text
Event Loop

LLM request ────────────────┐
                            │
Vector DB request ──────┐   │
                        │   │
External API ────────┐  │   │
                     ↓  ↓   ↓
                 responses
```

This is why `asyncio` is very common in **LLM applications, FastAPI services, agents, and API-heavy systems**.

---

## ⭐ Interview answer

If asked:

> **What is an event loop in Python?**

Say:

> "The event loop is the mechanism that manages and schedules asynchronous tasks. When a coroutine reaches an `await` on an I/O operation, it can suspend, allowing the event loop to execute other ready tasks. Once the I/O operation is ready, the event loop resumes the suspended coroutine. Blocking synchronous operations can block the event loop and reduce the benefits of async programming."

### Remember this one diagram:

```text
async function
      ↓
   coroutine
      ↓
     await
      ↓
   coroutine pauses
      ↓
   EVENT LOOP
      ↓
runs other tasks
      ↓
I/O completes
      ↓
coroutine resumes
```

**Next: Blocking I/O vs Non-blocking I/O** — this is one of the most likely areas to be asked directly in an interview.
