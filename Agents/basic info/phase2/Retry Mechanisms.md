# Phase 2 — Tool Calling

## 10. Retry Mechanisms

A **retry mechanism** means attempting a failed tool call again when the failure is likely to be temporary.

For agents, retries are important because tools often depend on external systems:

```text
Agent
 ↓
REST API
 ↓
Database
 ↓
Third-party service
```

Any of these can temporarily fail.

---

# 1. Why do we need retries?

Suppose your agent calls:

```python
get_customer(123)
```

The API temporarily returns:

```text
503 Service Unavailable
```

The customer probably still exists.

The service may recover a moment later.

Instead of immediately returning:

> "I can't get the customer."

we can retry:

```text
Attempt 1
   ↓
503
   ↓
Retry
   ↓
Attempt 2
   ↓
Success
```

---

# 2. Don't retry every error

This is the first rule:

> **Retry only when the failure is potentially temporary.**

### Good candidates for retry

```text
Timeout
Connection reset
503 Service Unavailable
Temporary network failure
429 Rate Limit
Temporary database connection failure
```

### Usually don't retry

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
Invalid arguments
Invalid customer ID
Business rule violation
```

For example:

```text
get_customer(999999)
       ↓
404 Not Found
```

Retrying:

```text
get_customer(999999)
get_customer(999999)
get_customer(999999)
```

won't make the customer appear.

---

# 3. Basic retry

The simplest implementation:

```python
import time

def call_with_retry(tool, max_retries=3):

    for attempt in range(max_retries):
        try:
            return tool()

        except TimeoutError:
            if attempt == max_retries - 1:
                raise

            time.sleep(2)
```

Flow:

```text
Attempt 1
   ↓
Failure
   ↓
Wait 2 sec
   ↓
Attempt 2
   ↓
Failure
   ↓
Wait 2 sec
   ↓
Attempt 3
   ↓
Success
```

This works, but production systems usually use something better.

---

# 4. Exponential Backoff

Instead of waiting the same amount of time:

```text
2 sec
2 sec
2 sec
```

we increase the delay:

```text
1 sec
2 sec
4 sec
8 sec
```

This is called **exponential backoff**.

Conceptually:

```python
delay = 2 ** attempt
```

For example:

```text
attempt 0 → 1 second
attempt 1 → 2 seconds
attempt 2 → 4 seconds
attempt 3 → 8 seconds
```

Why?

Because if the external service is overloaded, immediately retrying repeatedly can make the situation worse.

---

# 5. Why not retry immediately?

Imagine an API is overloaded.

1000 requests arrive:

```text
API overloaded
     ↓
1000 requests fail
```

If all 1000 immediately retry:

```text
1000 retries
     ↓
API gets even more overloaded
     ↓
1000 failures
     ↓
1000 more retries
```

This can create a **retry storm**.

Backoff gives the service time to recover.

---

# 6. Jitter

Even exponential backoff has a problem.

Imagine 1000 agents all fail at exactly the same time.

They might all retry:

```text
2 seconds later
```

So:

```text
1000 agents
     ↓
wait 2 seconds
     ↓
1000 requests simultaneously
```

That's still bad.

We add **jitter**, which introduces randomness.

For example:

```text
Agent 1 → 2.1 sec
Agent 2 → 2.7 sec
Agent 3 → 2.3 sec
Agent 4 → 3.0 sec
Agent 5 → 2.4 sec
```

Now the requests are spread out.

---

# 7. Exponential Backoff + Jitter

Conceptually:

```python
import random

delay = (2 ** attempt) + random.uniform(0, 1)
```

So instead of:

```text
2 sec
4 sec
8 sec
```

you might get:

```text
2.4 sec
4.8 sec
8.2 sec
```

This is a common production pattern.

---

# 8. Maximum retries

Never retry forever.

Bad:

```text
while True:
    retry()
```

You could end up with:

```text
Tool failure
 ↓
Retry
 ↓
Retry
 ↓
Retry
 ↓
Retry
 ↓
...
```

Instead:

```text
max_retries = 3
```

Then:

```text
Attempt 1
 ↓
Failure
 ↓
Attempt 2
 ↓
Failure
 ↓
Attempt 3
 ↓
Failure
 ↓
Stop
```

The application then returns an appropriate error.

---

# 9. Maximum execution time

Retries should also have a **time limit**.

For example:

```text
Maximum agent execution time = 30 seconds
```

Even if:

```text
max_retries = 10
```

the runtime should stop once the overall timeout is reached.

This protects against:

* Long-running requests
* Infinite loops
* Unexpected latency
* High infrastructure costs

---

# 10. Important: Retry the tool, not necessarily the whole agent

Suppose:

```text
User
 ↓
LLM
 ↓
search_customer()
 ↓
Timeout
```

You usually don't want to restart the entire agent reasoning process.

Instead:

```text
search_customer()
 ↓
temporary failure
 ↓
retry search_customer()
 ↓
success
 ↓
continue agent
```

This is more efficient.

---

# 11. The LLM doesn't necessarily control retries

This is an important interview distinction.

You could tell the LLM:

> "If the tool fails, retry it."

But that's not sufficient.

Why?

Because the LLM might do:

```text
retry
retry
retry
retry
...
```

Instead, your **application/runtime** should enforce:

```text
max_retries = 3
timeout = 30 sec
```

The LLM can decide what to do conceptually, but the runtime should enforce safety limits.

---

# 12. Idempotency — very important

Now we get to an important production concept.

Suppose your tool is:

```text
charge_credit_card(amount)
```

The first request succeeds, but the response gets lost because of a network timeout.

Your agent sees:

```text
Timeout
```

It might retry:

```text
charge_credit_card(₹5000)
```

But what if the first request **actually succeeded**?

You could charge the customer twice.

```text
First call
 ↓
₹5000 charged
 ↓
Response lost
 ↓
Agent thinks it failed
 ↓
Retry
 ↓
Another ₹5000 charged
```

This is dangerous.

---

# 13. Idempotency keys

For operations like payments, refunds, order creation, etc., we often use an **idempotency key**.

Example:

```text
idempotency_key = "payment-request-abc123"
```

First request:

```text
charge ₹5000
key = abc123
```

The server processes it.

If the request is retried:

```text
charge ₹5000
key = abc123
```

The server recognizes:

> "I've already processed this operation."

So it doesn't create a duplicate charge.

---

# 14. Read vs write retries

This distinction is useful in interviews.

### Read operation

```text
get_customer()
search_orders()
get_weather()
```

Usually safer to retry.

### Write operation

```text
create_order()
charge_card()
send_email()
delete_customer()
```

Needs more caution.

Why?

Because the operation may have already succeeded even though the response failed.

---

# 15. Example: Safe retry

```text
get_weather()
 ↓
Timeout
 ↓
Retry
 ↓
Success
```

Usually fine.

---

# 16. Example: Dangerous retry

```text
charge_card(₹5000)
 ↓
Timeout
 ↓
Retry
 ↓
charge_card(₹5000)
```

Potential duplicate charge.

So you need mechanisms like:

```text
Idempotency key
+
Server-side deduplication
```

---

# 17. Retry decision flow

A production retry layer can look like:

```text
              Tool Call
                  ↓
              Execute
                  ↓
             ┌────┴────┐
             ↓         ↓
          Success     Error
                       ↓
                Classify error
                       ↓
              ┌────────┴────────┐
              ↓                 ↓
          Retryable         Non-retryable
              ↓                 ↓
       Retry budget?          Stop
              ↓
          ┌───┴───┐
          ↓       ↓
         Yes      No
          ↓       ↓
        Retry    Stop
          ↓
 Exponential backoff
          +
        Jitter
```

---

# 18. Production example

Imagine your agent calls a payment service.

```python
def process_payment(amount, idempotency_key):
    ...
```

Your retry policy might be:

```text
Timeout       → Retry
503           → Retry
429           → Retry after server-provided delay
400           → Don't retry
401           → Don't retry
403           → Don't retry
```

With:

```text
Max retries: 3
Timeout: 10 seconds
Backoff: exponential
Jitter: enabled
Idempotency key: required
```

That's much safer.

---

# 19. What about rate limits?

Suppose the API returns:

```text
429 Too Many Requests
```

This means:

> "You're sending requests too quickly."

The response may include something like:

```text
Retry-After: 5
```

Then your application should ideally wait according to that instruction before retrying.

Conceptually:

```text
429
 ↓
Retry-After = 5 sec
 ↓
Wait
 ↓
Retry
```

This is better than immediately retrying.

---

# 20. Interview answer

### "How would you implement retries for an AI agent?"

A strong answer:

> **"I would first classify tool failures into retryable and non-retryable errors. For transient failures such as timeouts, 503s, and certain rate limits, I'd use bounded retries with exponential backoff and jitter. I'd enforce maximum retries and an overall execution timeout. For state-changing operations, I'd use idempotency keys where supported to prevent duplicate side effects. Authentication, validation, permission, and business-rule errors generally shouldn't be blindly retried."**

That's a strong **production-level answer**.

---

# Phase 2 Complete

You've now covered the full basic tool-calling lifecycle:

```text
Tool
 ↓
Tool Schema
 ↓
LLM selects tool
 ↓
Arguments
 ↓
Tool execution
 ↓
Tool result
 ↓
Multiple tools
 ↓
Parallel calls
 ↓
Tool errors
 ↓
Retries
```

## The most important mental model

```text
              ┌──────────────┐
              │     User     │
              └──────┬───────┘
                     ↓
              ┌──────────────┐
              │     LLM      │
              └──────┬───────┘
                     ↓
              Choose a tool
                     ↓
             Generate arguments
                     ↓
              ┌──────────────┐
              │ Tool Runtime │
              └──────┬───────┘
                     ↓
                Validate
                     ↓
                Execute
                     ↓
             ┌───────┴───────┐
             ↓               ↓
          Success           Error
             ↓               ↓
        Tool result       Retry/stop
             └───────┬───────┘
                     ↓
                    LLM
                     ↓
          Another tool / Answer
```

### Next phase

Now that you understand **tool calling conceptually**, the next useful step is to **implement it in Python with an actual LLM**.

That will connect all these concepts—**schema → tool selection → arguments → execution → result → loop**—into working code.
