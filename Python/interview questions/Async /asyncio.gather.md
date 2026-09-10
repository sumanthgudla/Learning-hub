# 8. `asyncio.gather()` — 🔥🔥 VERY IMPORTANT

`asyncio.gather()` is used when you want to **run multiple async operations concurrently and collect their results**.

This is extremely useful for AI Engineer work because you often have multiple independent API/DB calls.

---

## 1. Sequential execution

Suppose:

```python
import asyncio

async def task_a():
    await asyncio.sleep(2)
    return "A"

async def task_b():
    await asyncio.sleep(3)
    return "B"
```

If you do:

```python
async def main():
    a = await task_a()
    b = await task_b()

    print(a, b)

asyncio.run(main())
```

Execution is:

```text
Task A: ██████████ 2 sec
Task B:           ███████████████ 3 sec
                         ↓
                    Total ≈ 5 sec
```

Why?

Because Python waits for A to finish before starting B.

---

# 2. Using `asyncio.gather()`

Now:

```python
async def main():
    a, b = await asyncio.gather(
        task_a(),
        task_b()
    )

    print(a, b)

asyncio.run(main())
```

Now:

```text
Task A: ██████████
Task B: ███████████████

Time →  0     2     3
              ↓     ↓
             A      B
```

Total ≈ **3 seconds**.

The operations are independent, so they can make progress concurrently.

---

# 3. What does `gather()` return?

This is important.

Suppose:

```python
async def get_user():
    await asyncio.sleep(1)
    return "Sumanth"

async def get_orders():
    await asyncio.sleep(1)
    return ["Order1", "Order2"]
```

Then:

```python
user, orders = await asyncio.gather(
    get_user(),
    get_orders()
)
```

You get:

```python
user
# "Sumanth"

orders
# ["Order1", "Order2"]
```

The results are returned in the **same order as the awaitables passed to `gather()`**.

So:

```python
results = await asyncio.gather(
    get_user(),       # result 0
    get_orders()      # result 1
)
```

means:

```python
results[0]  # get_user result
results[1]  # get_orders result
```

Even if `get_orders()` happens to finish first.

---

# 4. Important interview trap

Suppose:

```python
asyncio.gather(
    slow_task(),
    fast_task()
)
```

Maybe:

```text
slow_task → 5 seconds
fast_task → 1 second
```

`fast_task` finishes first.

But the returned results are still:

```text
[
    slow_task_result,
    fast_task_result
]
```

because `gather()` preserves the **input order**.

---

# 5. AI Engineer example

Imagine you're building an AI application.

You need:

```text
Customer request
       ↓
 ┌─────┼───────────┐
 ↓     ↓           ↓
Profile Vector DB  API
```

These operations don't depend on each other.

You can do:

```python
profile, documents, api_data = await asyncio.gather(
    get_customer_profile(),
    search_vector_db(),
    call_external_api()
)
```

This is much better than:

```python
profile = await get_customer_profile()

documents = await search_vector_db()

api_data = await call_external_api()
```

if all three are independent I/O operations.

---

# 6. What if one task fails?

This is an important interview topic.

Suppose:

```python
async def task_a():
    return "A"

async def task_b():
    raise Exception("Something went wrong")

async def task_c():
    return "C"
```

Then:

```python
results = await asyncio.gather(
    task_a(),
    task_b(),
    task_c()
)
```

By default, if one awaitable raises an exception, `gather()` propagates that exception to the caller.

You can handle it:

```python
try:
    results = await asyncio.gather(
        task_a(),
        task_b(),
        task_c()
    )
except Exception as e:
    print(e)
```

---

# 7. `return_exceptions=True`

Sometimes you don't want one failure to prevent you from receiving the outcomes of the other operations.

You can use:

```python
results = await asyncio.gather(
    task_a(),
    task_b(),
    task_c(),
    return_exceptions=True
)
```

Now an exception can appear in the results:

```python
[
    "A",
    Exception("Something went wrong"),
    "C"
]
```

You can inspect each result.

```python
for result in results:
    if isinstance(result, Exception):
        print("Failed:", result)
    else:
        print("Success:", result)
```

---

# 8. Don't use `gather()` when tasks depend on each other

Bad candidate:

```python
user = await get_user()

orders = await get_orders(user)
```

Because:

```text
get_user()
    ↓
need user
    ↓
get_orders(user)
```

You can't start the second operation until you have the first result.

So sequential `await` is correct.

---

# 9. Don't use `gather()` for everything

This:

```python
await asyncio.gather(
    operation_a(),
    operation_b(),
    operation_c()
)
```

is beneficial when operations are:

* Independent
* I/O-bound
* Safe to execute concurrently

But there may be reasons **not** to run everything simultaneously:

```text
1000 API calls
      ↓
asyncio.gather(...)
      ↓
💥 too many requests
      ↓
rate limits
```

In production, you may need:

* concurrency limits
* semaphores
* connection pooling
* retries
* backoff
* rate limiting

These become important when building production AI applications.

---

# ⭐ Interview question

### "What's the difference?"

```python
a = await task_a()
b = await task_b()
```

vs.

```python
a, b = await asyncio.gather(
    task_a(),
    task_b()
)
```

Answer:

> "The first executes the operations sequentially because `task_b()` doesn't start until `task_a()` completes. `asyncio.gather()` schedules the awaitables so they can make progress concurrently, which is particularly useful for independent I/O-bound operations."

---

# ⭐ Another interview question

### "Does `asyncio.gather()` make CPU-bound code parallel?"

**No.**

`gather()` provides async concurrency; it doesn't turn CPU-bound Python code into parallel execution.

---

## 🧠 Remember

```text
Sequential:

await A
   ↓
A finishes
   ↓
await B
   ↓
B finishes

Total ≈ A + B
```

```text
gather():

gather(A, B)
   ↓
A ──────────→ finish
B ───────────────→ finish

Total ≈ max(A, B)
```

That `max(A, B)` idea assumes the operations are genuinely independent, I/O-bound, and can overlap without other bottlenecks.

### Your roadmap so far

```text
1. async                 ✅
2. await                 ✅
3. coroutine             ✅
4. event loop            ✅
5. blocking/non-blocking ✅
6. concurrency/parallel  ✅
7. asyncio               ✅
8. asyncio.gather()      ✅
9. when async helps
10. when async doesn't help
```

**Next: When does async actually help?** We'll use real examples from **FastAPI, LLM APIs, RAG, vector DBs, and agents**, which is especially relevant for your AI Engineer interviews.
