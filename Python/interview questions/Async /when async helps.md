# 9. When does Async actually help? — 🔥🔥

This is where you move from **knowing syntax** to being able to answer interview questions.

The main rule is:

> **Async helps when your program spends a lot of time waiting for I/O.**

---

## 1. Async is excellent for I/O-bound work

Examples:

* REST API calls
* LLM API calls
* Database queries
* Vector DB searches
* Network requests
* WebSocket communication

Imagine:

```text
Your Python application
        |
        ├── Azure OpenAI ────── 2 sec
        ├── Vector DB ───────── 1 sec
        └── REST API ────────── 3 sec
```

If they're independent, async can allow all three to be in progress together.

```python
results = await asyncio.gather(
    call_llm(),
    search_vector_db(),
    call_api()
)
```

Potentially:

```text
LLM          ██████████  2 sec
Vector DB    █████       1 sec
REST API     ███████████████ 3 sec

Total ≈ 3 sec
```

Instead of approximately:

```text
LLM          ██████████
Vector DB               █████
REST API                       ███████████████

Total ≈ 6 sec
```

---

# 2. Why does async help?

Because the CPU isn't doing useful work while waiting for the network.

For example:

```python
response = await call_llm()
```

The LLM server may take 2 seconds to respond.

During that time:

```text
Your application
      ↓
waiting for network
      ↓
Event loop
      ↓
run another coroutine
```

So you make better use of the time that would otherwise be spent waiting.

---

# 3. AI Engineer example — LLM calls

Suppose an agent needs three independent pieces of information:

```text
                    Agent
                      |
        ┌─────────────┼──────────────┐
        ↓             ↓              ↓
   LLM call      Vector search    Customer API
```

You could write:

```python
async def get_context():
    llm, docs, customer = await asyncio.gather(
        call_llm(),
        search_vector_db(),
        get_customer()
    )

    return llm, docs, customer
```

This is a very realistic use of async in an AI application.

---

# 4. AI Engineer example — RAG

Imagine your RAG pipeline does:

```text
User question
      ↓
Query rewriting
      ↓
Vector search
      ↓
Metadata search
      ↓
External knowledge
      ↓
LLM
```

Some operations may be sequential because they depend on previous results.

But suppose you have:

```text
Vector DB search
      +
Keyword search
      +
Metadata search
```

and they don't depend on each other.

You can potentially do:

```python
vector_results, keyword_results, metadata = await asyncio.gather(
    vector_search(query),
    keyword_search(query),
    metadata_search(query)
)
```

Then combine the results.

That's a good async use case.

---

# 5. Async helps when you have many concurrent users

Imagine a FastAPI service:

```text
100 users
   ↓
FastAPI
   ↓
Each request calls an LLM
```

If every request spends most of its time waiting for network responses, asynchronous I/O can allow the server to handle many in-flight requests efficiently.

Conceptually:

```text
Event Loop

Request 1 → waiting for LLM
Request 2 → waiting for DB
Request 3 → waiting for LLM
Request 4 → processing
Request 5 → waiting for API
```

The event loop can move between tasks instead of dedicating a blocked execution path to each wait.

---

# 6. When async does NOT help

This is equally important.

### CPU-bound work

For example:

```python
async def calculate():
    for i in range(1_000_000_000):
        # expensive computation
        ...
```

There's no meaningful I/O waiting.

The CPU is busy calculating:

```text
CPU
████████████████████████████
       calculation
```

Adding:

```python
async
```

doesn't make the calculation parallel.

---

# 7. Another bad async example

```python
async def process():
    time.sleep(10)
```

This is bad because:

```python
time.sleep(10)
```

blocks the event loop.

You haven't gained anything from making the function `async`.

Use:

```python
await asyncio.sleep(10)
```

if the intention is simply to asynchronously wait.

---

# 8. Async isn't always necessary

Suppose your application does:

```text
Request
 ↓
Simple calculation
 ↓
Return response
```

and there is almost no I/O waiting.

You don't necessarily need async.

Don't use async just because:

> "Async is faster."

That's an incorrect assumption.

Instead ask:

> **"What is my bottleneck?"**

If the bottleneck is waiting on I/O → async may help.

If the bottleneck is CPU computation → async alone probably won't help.

---

# ⭐ Interview decision framework

When you see a problem, think:

```text
                Is the workload I/O-bound?
                       /       \
                     YES        NO
                      |          |
             Is it independent?  CPU-bound?
                /      \           |
              YES       NO         |
               |         |         ↓
         asyncio/gather  async   Consider
                         still    processes/
                         useful   other CPU
                                  strategies
```

---

# 🔥 Interview question

### "When would you use async Python?"

A strong answer:

> "I would use async primarily for I/O-bound workloads where the application spends significant time waiting for external systems, such as REST APIs, databases, LLM APIs, or vector databases. Async allows the event loop to run other tasks while one coroutine is waiting. I wouldn't expect async alone to improve CPU-bound workloads."

---

# 🔥 AI Engineer interview example

### Interviewer:

> "You have an AI service that calls three APIs. Each takes around 2 seconds. How would you reduce the latency?"

First ask:

> **"Are the three API calls independent?"**

If yes:

```python
await asyncio.gather(
    api_1(),
    api_2(),
    api_3()
)
```

Potentially:

```text
Sequential:

2 + 2 + 2 = ~6 sec


Concurrent:

max(2, 2, 2) = ~2 sec
```

Then mention production considerations:

> "I'd also consider connection pooling, API rate limits, concurrency limits, timeouts, retries, and whether the downstream services actually support concurrent requests."

That's a **much stronger senior-level answer** than simply saying "use async."

---

## 🧠 Final mental model

```text
ASYNC IS GOOD
─────────────

Network/API       ✅
LLM calls         ✅
Database I/O      ✅
Vector DB         ✅
HTTP requests     ✅
WebSockets        ✅


ASYNC ALONE IS NOT THE SOLUTION
───────────────────────────────

Heavy computation       ❌
CPU-intensive loops     ❌
Blocking libraries      ❌
time.sleep()            ❌
```

### The rule to remember:

> **Async doesn't make work faster. It makes waiting more efficient.**

That sentence is worth remembering for your interview.

**Next and final topic: When async does NOT help + how to handle synchronous/blocking code inside async Python (`asyncio.to_thread`, executors, and common interview traps).**
