Absolutely. We'll do **Async Python one topic at a time**, in an interview-oriented way.

## 1. `async` — What does it mean?

`async` is used to define a **coroutine function**.

Basic example:

```python
async def fetch_data():
    print("Fetching data...")
```

Compare it with normal Python:

```python
def fetch_data():
    print("Fetching data...")
```

The important difference is:

```python
def fetch_data():
```

is a **normal function**, while:

```python
async def fetch_data():
```

is an **asynchronous coroutine function**.

---

### What happens when you call it?

Normal function:

```python
def fetch_data():
    print("Fetching data...")

fetch_data()
```

Output:

```text
Fetching data...
```

The function executes immediately.

But:

```python
async def fetch_data():
    print("Fetching data...")

fetch_data()
```

does **not** execute the body immediately.

Instead:

```python
result = fetch_data()

print(result)
```

you get something like:

```text
<coroutine object fetch_data at 0x...>
```

So:

> Calling an `async def` function creates a **coroutine object**. It doesn't execute the coroutine's body immediately.

---

## Then how do we execute it?

Usually with an **event loop**:

```python
import asyncio

async def fetch_data():
    print("Fetching data...")

asyncio.run(fetch_data())
```

Output:

```text
Fetching data...
```

`asyncio.run()` starts an event loop and runs the coroutine.

---

## Why do we need `async`?

Imagine you're calling an API:

```python
async def fetch_data():
    response = await call_api()
    return response
```

While waiting for the API response, Python can potentially do other work instead of just sitting idle.

For example:

```text
Task A → API request ───────────────→ response
                 ↓
              waiting

Task B → database request ─────→ response
```

This is particularly useful for **I/O-heavy applications**, such as:

* Calling LLM APIs
* Calling multiple REST APIs
* Database operations
* Network requests
* Reading/writing network streams

This is why async Python is particularly relevant to **AI Engineer** roles.

For example, an AI application might call:

```text
User
 ↓
Agent
 ├── LLM API
 ├── Vector DB
 ├── External API
 └── Another service
```

Many of these operations involve waiting for external systems.

---

## Important interview point

`async` **does NOT automatically make code faster**.

This:

```python
async def calculate():
    for i in range(100000000):
        ...
```

doesn't magically become faster because you added `async`.

Async is mainly useful when your program spends significant time **waiting for I/O**.

### Good use case

```python
async def call_llm():
    response = await llm.ainvoke(...)
    return response
```

The LLM call involves network I/O.

### Poor use case

```python
async def calculate():
    return sum(i * i for i in range(100000000))
```

This is CPU-heavy work. `async` doesn't provide parallel CPU execution.

---

## ⭐ Interview answer

If EPAM asks:

> **What is `async` in Python?**

A strong answer:

> "`async` is used to define a coroutine function. Calling an async function returns a coroutine object, which can be executed by an event loop. Async programming is mainly useful for I/O-bound operations because while one operation is waiting, the event loop can allow other tasks to make progress. It doesn't by itself provide parallel execution or make CPU-bound code faster."

### Remember this

```text
async def
   ↓
defines coroutine function
   ↓
calling it
   ↓
creates coroutine object
   ↓
event loop executes it
```

**Next topic: `await`** — this is where async Python starts becoming interesting, especially the question **"what exactly happens when Python hits `await`?"**
