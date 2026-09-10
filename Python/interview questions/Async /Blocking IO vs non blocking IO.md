# 5. Blocking I/O vs Non-blocking I/O — 🔥🔥 VERY IMPORTANT

This is **one of the most important async interview concepts**.

The key question is:

> **Does the program have to stop and wait, or can it continue doing other work while waiting?**

---

# 1. What is I/O?

**I/O = Input/Output**

It means communicating with something outside the CPU.

Examples:

* Calling an API
* Reading from a database
* Reading a file
* Writing to a network
* Calling Azure OpenAI
* Calling a vector database

For example:

```python
response = requests.get(url)
```

The program is communicating with a remote server.

---

# 2. Blocking I/O

Blocking I/O means:

> **The current execution is forced to wait until the I/O operation finishes.**

Example:

```python
import requests

def fetch_data():
    response = requests.get("https://example.com")
    return response
```

While `requests.get()` is waiting for the server:

```text
Python
  ↓
requests.get()
  ↓
Waiting for server
  ↓
🚫 Cannot continue this execution
  ↓
Response arrives
  ↓
Continue
```

If the request takes 3 seconds, you're effectively waiting for those 3 seconds.

---

# 3. Non-blocking I/O

Non-blocking I/O means:

> **The program can give control back and allow other work to proceed while waiting for the I/O operation.**

Example:

```python
import asyncio

async def fetch_data():
    response = await async_api_call()
    return response
```

Conceptually:

```text
Coroutine A
    ↓
API request
    ↓
await
    ↓
PAUSE A
    ↓
Event Loop
    ↓
Run Coroutine B
    ↓
Run Coroutine C
    ↓
API response arrives
    ↓
Resume A
```

So the CPU isn't sitting around waiting for that particular coroutine.

---

# 4. Very important distinction

Don't confuse:

> **Blocking I/O**

with:

> **Slow I/O**

A slow operation isn't necessarily blocking.

For example:

```python
await asyncio.sleep(10)
```

It waits for 10 seconds, but it is **non-blocking** from the event loop's perspective.

Whereas:

```python
time.sleep(10)
```

is **blocking**.

### Compare:

```python
time.sleep(10)
```

```text
Event Loop
    ↓
sleep
    ↓
🚫 BLOCKED for 10 seconds
```

versus:

```python
await asyncio.sleep(10)
```

```text
Event Loop
    ↓
coroutine pauses
    ↓
✅ other tasks can run
```

This distinction is **extremely important**.

---

# 5. Real AI Engineer example

Imagine you have an agent that needs to call:

```text
User
 ↓
AI Agent
 ├── Azure OpenAI
 ├── Vector DB
 └── External API
```

Suppose each takes 2 seconds.

### Blocking approach

```python
def run_agent():
    llm_response = call_llm()       # 2 sec
    vector_results = search_db()    # 2 sec
    api_response = call_api()       # 2 sec
```

Approximately:

```text
LLM        ██████████ 2 sec
Vector DB             ██████████ 2 sec
External API                       ██████████ 2 sec

Total ≈ 6 sec
```

Each operation blocks the current flow.

---

# 6. Async approach

If the operations are independent:

```python
async def run_agent():
    llm_response = ...
    vector_results = ...
    api_response = ...
```

You can later use concurrency mechanisms such as:

```python
await asyncio.gather(
    call_llm(),
    search_db(),
    call_api()
)
```

Conceptually:

```text
LLM          ██████████
Vector DB    ██████████
External API ██████████

Total ≈ 2 sec
```

Because while one operation is waiting on I/O, other operations can make progress.

We'll study `asyncio.gather()` separately.

---

# 7. What happens if you use blocking code inside async?

This is the **EPAM-style question** you specifically wanted to prepare for.

Consider:

```python
import asyncio
import time

async def task_a():
    print("A started")

    time.sleep(5)

    print("A finished")

async def task_b():
    print("B started")

    await asyncio.sleep(1)

    print("B finished")

async def main():
    await asyncio.gather(
        task_a(),
        task_b()
    )

asyncio.run(main())
```

You might expect:

```text
A started
B started
B finished
A finished
```

But `task_a()` executes:

```python
time.sleep(5)
```

which blocks the **event loop**.

So `task_b()` may not get a chance to run until that blocking operation finishes.

Conceptually:

```text
Event Loop
    ↓
task_a
    ↓
time.sleep(5)
    ↓
🚨 EVENT LOOP BLOCKED
    ↓
5 seconds
    ↓
task_a continues
    ↓
Now task_b gets a chance
```

### This is the critical rule:

> **An `async def` function does not automatically make the code inside it non-blocking.**

---

# 8. Common examples

| Operation                     | Typical behavior                                              |
| ----------------------------- | ------------------------------------------------------------- |
| `requests.get()`              | Blocking                                                      |
| `time.sleep()`                | Blocking                                                      |
| `asyncio.sleep()`             | Non-blocking                                                  |
| Async HTTP client             | Non-blocking                                                  |
| Async DB client               | Non-blocking                                                  |
| CPU-heavy Python loop         | Blocks event loop                                             |
| `await some_async_function()` | Allows suspension if the awaited operation is genuinely async |

---

# 9. What about CPU-heavy work?

This is another important point.

Suppose:

```python
async def calculate():
    for i in range(1_000_000_000):
        ...
```

There is no useful `await` during the calculation.

So:

```text
Event Loop
    ↓
CPU-heavy calculation
    ↓
🚨 BLOCKED
```

Async is primarily useful for **I/O-bound work**, not CPU-bound work.

For CPU-heavy work, you generally consider:

* multiprocessing
* process pools
* native libraries that release the GIL
* other appropriate parallel-computation approaches

We'll cover concurrency vs parallelism soon.

---

# ⭐ Interview question

### Q: What's the difference between blocking and non-blocking I/O?

A strong answer:

> **"Blocking I/O makes the current execution wait until the operation completes. Non-blocking I/O allows the program to continue handling other work while the I/O operation is pending. In asyncio, an async I/O operation can be awaited, allowing the coroutine to suspend and the event loop to run other tasks."**

### Follow-up: "Can blocking code exist inside an async function?"

Answer:

> **"Yes. `async def` doesn't automatically make all code inside it asynchronous. Blocking operations such as `time.sleep()` or synchronous HTTP calls can block the event loop and prevent other coroutines from making progress."**

---

## 🧠 Remember this

```text
BLOCKING
--------
Task
 ↓
I/O
 ↓
WAIT
 ↓
🚫 execution blocked


NON-BLOCKING
------------
Task
 ↓
I/O
 ↓
await
 ↓
PAUSE coroutine
 ↓
Event Loop
 ↓
run other tasks
 ↓
I/O completes
 ↓
resume coroutine
```

**Next: Concurrency vs Parallelism** — this is another classic interview question, and it connects `asyncio`, threads, processes, and the Python GIL.
