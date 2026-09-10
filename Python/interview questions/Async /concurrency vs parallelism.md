# 6. Concurrency vs Parallelism — 🔥🔥 VERY IMPORTANT

This is a **classic Python interview question**.

The easiest way to remember:

> **Concurrency = dealing with multiple tasks at the same time.**
> **Parallelism = actually executing multiple tasks at the same instant.**

---

# 1. Concurrency

Imagine you are a single chef preparing three dishes.

```text
Chef
 ↓
Cook A
 ↓
while A is waiting → work on B
 ↓
while B is waiting → work on C
 ↓
back to A
```

The chef is switching between tasks.

That's **concurrency**.

In Python async:

```text
One thread
    ↓
Event Loop
    ↓
Task A
Task B
Task C
```

The event loop can switch between coroutines when they reach points where they can suspend, such as `await`.

---

# 2. Parallelism

Now imagine:

```text
Chef 1 → Cook A
Chef 2 → Cook B
Chef 3 → Cook C
```

Multiple tasks are **actually executing simultaneously**.

That's parallelism.

Typically, parallelism requires multiple execution resources, such as multiple CPU cores/processes.

---

# 3. Asyncio → concurrency

Consider:

```python id="y7zjzq"
async def task_a():
    await asyncio.sleep(2)

async def task_b():
    await asyncio.sleep(2)
```

With:

```python id="zj9g7p"
await asyncio.gather(task_a(), task_b())
```

the tasks can make progress concurrently.

Conceptually:

```text
Time →

Task A: ████ WAIT ████████
Task B: ████ WAIT ████████
```

They're **not necessarily executing Python instructions simultaneously on two CPU cores**.

Instead, the event loop coordinates them.

---

# 4. Parallelism → multiple workers

For CPU-heavy work, you might use processes:

```text
CPU Core 1 → Process A
CPU Core 2 → Process B
CPU Core 3 → Process C
CPU Core 4 → Process D
```

Now multiple pieces of computation can execute at the same time.

That's parallelism.

---

# 🔥 Why this matters in Python: GIL

Python's **CPython implementation** has the Global Interpreter Lock (GIL).

For traditional CPU-bound Python code, the GIL generally prevents multiple threads from executing Python bytecode simultaneously within the same process.

So:

```text
Threads
   ↓
Thread A ──┐
Thread B ──┼──> GIL
Thread C ──┘
             ↓
        one executes
        Python bytecode
        at a time
```

This doesn't mean threads are useless.

Threads are still very useful for **I/O-bound operations**, because while one thread is waiting on I/O, another can run.

And importantly, some native operations can release the GIL.

---

# 5. Async vs Threads vs Processes

This is a useful interview table:

| Approach  | Main idea                  | Good for                                |
| --------- | -------------------------- | --------------------------------------- |
| `asyncio` | Cooperative concurrency    | I/O-heavy workloads                     |
| Threads   | Concurrent execution units | I/O-heavy workloads, blocking libraries |
| Processes | Separate processes         | CPU-heavy parallel work                 |

Think:

```text
I/O-heavy
   ↓
asyncio / threads


CPU-heavy
   ↓
processes / multiprocessing
```

This is a simplified rule, but a very useful interview starting point.

---

# 6. AI Engineer example

Suppose your AI application needs to make three network calls:

```text
Agent
 ├── Azure OpenAI
 ├── Vector DB
 └── REST API
```

These are mostly I/O-bound.

Async is a good fit:

```python id="y4f9h0"
results = await asyncio.gather(
    call_llm(),
    search_vector_db(),
    call_external_api()
)
```

While Azure OpenAI is responding:

```text
LLM request
    ↓
waiting
    ↓
Event loop → Vector DB
                 ↓
               waiting
                 ↓
              REST API
```

That's **concurrency**.

---

# 7. CPU-heavy AI example

Suppose you have expensive CPU processing:

```python id="5pyxwy"
def process_large_dataset(data):
    # CPU-intensive computation
    ...
```

Simply doing:

```python id="h4xqv4"
async def process_large_dataset(data):
    ...
```

doesn't magically make it parallel.

You need an appropriate mechanism for CPU parallelism, such as processes.

---

# ⭐ Most important distinction

### Concurrency

Tasks **overlap in progress**.

```text
A ────────┐
          ├── overlapping work
B ────────┘
```

### Parallelism

Tasks **execute simultaneously**.

```text
CPU 1: AAAAAAAAA
CPU 2: BBBBBBBBB
```

---

# 🔥 Interview question

### "Is asyncio parallel?"

A strong answer:

> **"Not in the traditional sense. asyncio primarily provides concurrency using an event loop, usually within a single thread. It allows multiple I/O-bound coroutines to make progress by switching between them when they await. It doesn't by itself provide parallel CPU execution."**

---

### Another common question

**Q: If I have 10 API calls, should I use multiprocessing?**

Usually:

> **No.** If the calls are I/O-bound, `asyncio` or threads are generally more appropriate. Multiprocessing is primarily useful when the workload is CPU-bound.

---

## 🧠 Remember this

```text
CONCURRENCY
"Multiple tasks are in progress."

        asyncio
           ↓
     Event Loop
       ↙  ↓  ↘
      A   B   C


PARALLELISM
"Multiple tasks execute simultaneously."

      CPU 1 → A
      CPU 2 → B
      CPU 3 → C
```

### One-line interview memory trick:

> **Concurrency is about structure; parallelism is about simultaneous execution.**

**Next: `asyncio` — we'll learn what it actually provides and how `asyncio.run()`, tasks, and the event loop fit together.**
