# Phase 2 — Tool Calling

## 9. Tool Errors

In a real production agent, **tools will fail**.

For example:

* API is down
* Database connection fails
* Request times out
* Invalid arguments
* Authentication fails
* Resource doesn't exist
* Permission denied
* External service returns an unexpected response

A good agent must know how to handle these failures.

---

# 1. Simple example

Suppose we have:

```python
def get_weather(city):
    response = requests.get(
        "https://weather-api.com",
        params={"city": city}
    )

    return response.json()
```

The LLM calls:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Hyderabad"
  }
}
```

But the weather API is down.

The Python code might raise:

```text
ConnectionError
```

If you don't handle this, your entire agent request could fail.

---

# 2. Tool errors should be caught

Instead of allowing the exception to crash the agent:

```python
def get_weather(city):
    try:
        response = requests.get(
            "https://weather-api.com",
            params={"city": city},
            timeout=5
        )

        response.raise_for_status()

        return {
            "success": True,
            "data": response.json()
        }

    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
```

Now the tool returns a controlled result.

For example:

```json
{
  "success": false,
  "error": "Weather service unavailable"
}
```

---

# 3. The error goes back to the LLM

The flow becomes:

```text
User
 ↓
LLM
 ↓
get_weather()
 ↓
Tool fails
 ↓
Error result
 ↓
LLM
```

The LLM can then decide what to do.

For example:

> "I'm unable to retrieve the weather right now."

Or it might try another available tool.

---

# 4. Different types of tool errors

Not all errors should be handled the same way.

This is an important production concept.

### A. Invalid arguments

LLM generates:

```json
{
  "customer_id": "abc"
}
```

But your tool expects an integer.

```text
Expected: integer
Received: string
```

You might return:

```json
{
  "success": false,
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "customer_id must be an integer"
  }
}
```

The LLM may be able to correct the arguments and try again.

---

# 5. B. Resource not found

Suppose:

```text
get_order("ORD-999")
```

returns:

```json
{
  "success": false,
  "error": {
    "type": "NOT_FOUND",
    "message": "Order ORD-999 does not exist"
  }
}
```

Retrying the exact same call won't help.

The agent should probably:

* Ask the user for another order ID
* Search for the order
* Or explain that the order doesn't exist

This is a **non-retryable error** in many cases.

---

# 6. C. Authentication error

Suppose the tool calls:

```text
GET /customer/123
```

and receives:

```text
401 Unauthorized
```

This is usually **not something the LLM should solve by changing the arguments**.

Your application needs to handle:

```text
Token expired?
Credentials missing?
Service authentication broken?
```

The LLM shouldn't be given secrets and told to "fix" authentication.

---

# 7. D. Permission error

Suppose the user says:

> "Delete customer 123."

Your tool returns:

```json
{
  "success": false,
  "error": {
    "type": "FORBIDDEN",
    "message": "User does not have permission to delete customers"
  }
}
```

The agent should not retry:

```text
delete_customer(123)
delete_customer(123)
delete_customer(123)
```

The permission won't magically change.

It should tell the user that the operation isn't permitted.

---

# 8. E. Timeout

Suppose:

```text
search_documents()
```

takes too long.

Your application might have:

```python
timeout=10
```

After 10 seconds:

```text
TimeoutError
```

Now the agent can potentially retry.

For example:

```text
First attempt
     ↓
Timeout
     ↓
Retry
     ↓
Success
```

This brings us to **retry mechanisms**.

---

# 9. Retryable vs non-retryable errors

This is a very important interview concept.

### Usually retryable

```text
Timeout
Temporary network failure
503 Service Unavailable
Temporary database connection failure
Rate limit (after waiting)
```

### Usually not retryable

```text
Invalid argument
404 Not Found
403 Forbidden
Invalid customer ID
Business rule violation
Insufficient permissions
```

You should not blindly retry every error.

---

# 10. Retry mechanism

A basic retry:

```python
import time

def call_tool_with_retry(tool, max_retries=3):

    for attempt in range(max_retries):
        try:
            return tool()

        except TimeoutError:
            if attempt == max_retries - 1:
                raise

            time.sleep(2)
```

Conceptually:

```text
Attempt 1
   ↓
Failure
   ↓
Wait
   ↓
Attempt 2
   ↓
Failure
   ↓
Wait
   ↓
Attempt 3
```

---

# 11. Exponential backoff

In production, instead of always waiting 2 seconds:

```text
2 sec
2 sec
2 sec
```

you can use exponential backoff:

```text
1 sec
2 sec
4 sec
8 sec
```

For example:

```python
delay = 2 ** attempt
```

This helps avoid hammering an overloaded service.

---

# 12. Retry with jitter

If thousands of agents fail at the same time, they could all retry simultaneously.

For example:

```text
10,000 requests fail
       ↓
all retry after 2 seconds
       ↓
server gets 10,000 requests
       ↓
server fails again
```

That's bad.

So production systems often add **jitter**:

```text
retry after:
2.1 sec
2.7 sec
3.2 sec
2.4 sec
...
```

This spreads the retries out.

You don't need to implement this for every interview question, but knowing **exponential backoff + jitter** is valuable for production-level AI engineering.

---

# 13. Tool errors can also come from bad LLM arguments

Consider:

```python
def get_order(order_id: str):
    ...
```

User says:

> "Get my latest order."

But the LLM generates:

```json
{
  "order_id": ""
}
```

Your tool validation catches it:

```json
{
  "success": false,
  "error": {
    "type": "VALIDATION_ERROR",
    "message": "order_id is required"
  }
}
```

The agent can potentially recover by calling:

```text
search_orders()
```

to find the latest order.

This is an example of an agent **recovering from a tool error by taking another action**.

---

# 14. Tool errors shouldn't expose sensitive information

Suppose your database throws:

```text
psycopg2.OperationalError:
connection failed to db-prod-03.internal.company.com
user=admin password=...
```

Never send that raw error to the LLM/user.

Instead:

```json
{
  "success": false,
  "error": {
    "type": "DATABASE_ERROR",
    "message": "Unable to retrieve customer information."
  }
}
```

Internally, you can log the detailed exception.

So:

```text
User/LLM → Safe error
Logs      → Detailed error
```

---

# 15. Tool errors and agent loops

Now you can see why the agent loop needs error handling.

```text
                 LLM
                  ↓
              Tool Call
                  ↓
             Execute Tool
                  ↓
             ┌────┴────┐
             ↓         ↓
          Success     Error
             ↓         ↓
            LLM    Classify error
                       ↓
              ┌────────┼─────────┐
              ↓        ↓         ↓
            Retry   Another    Stop
                     tool
```

For example:

```text
search_customer()
       ↓
Timeout
       ↓
Retry
       ↓
Success
       ↓
search_orders()
```

---

# 16. Don't let the LLM control retries indefinitely

This is a major production concern.

Imagine:

```text
Tool fails
 ↓
LLM retries
 ↓
Tool fails
 ↓
LLM retries
 ↓
Tool fails
 ↓
LLM retries
 ↓
...
```

You can end up with:

* Huge latency
* High token cost
* Excessive API calls
* Infinite loops

So the application should impose limits:

```text
max tool calls = 10
max retries = 3
max execution time = 30 seconds
```

These should be enforced by the **runtime/application**, not merely instructed to the LLM.

---

# 17. Production architecture

A robust tool execution layer looks something like:

```text
                LLM
                 ↓
             Tool Call
                 ↓
        Validate arguments
                 ↓
         Check authorization
                 ↓
           Execute tool
                 ↓
          ┌──────┴──────┐
          ↓             ↓
       Success         Error
          ↓             ↓
      Tool result    Classify error
                         ↓
                 ┌───────┼────────┐
                 ↓       ↓        ↓
               Retry   Recover    Stop
                         ↓
                    Another tool
```

And around all of this:

```text
timeouts
rate limits
logging
metrics
tracing
max retries
max tool calls
```

---

# Interview Questions

### "How do you handle tool failures?"

A strong answer:

> **"I would catch tool exceptions in the tool execution layer and return structured error information to the agent. I would classify errors into retryable and non-retryable categories. Transient failures such as timeouts or 503s can use bounded retries with exponential backoff and jitter, while errors such as invalid arguments or authorization failures should generally not be retried. I'd also enforce timeouts, retry limits, and maximum tool-call limits to prevent loops and excessive cost."**

### "Should the LLM handle authentication failures?"

> **"No. Authentication and authorization should be enforced by the application or service layer. The LLM can interpret the resulting error, but it shouldn't be trusted as a security mechanism."**

---

# What you've learned in Phase 2

You now understand:

```text
1. What is a Tool?
       ↓
2. Tool Schema
       ↓
3. LLM chooses a Tool
       ↓
4. Tool Arguments
       ↓
5. Tool Execution
       ↓
6. Tool Results
       ↓
7. Multiple Tools
       ↓
8. Parallel Tool Calls
       ↓
9. Tool Errors
       ↓
10. Retry Mechanisms
```

### Next topic: **Retry Mechanisms**

We'll go deeper into **when to retry, exponential backoff, jitter, maximum retries, idempotency, and how to prevent an agent from getting stuck in an infinite retry loop**.
