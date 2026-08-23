# Phase 1 — Topic 7: Tool Execution & Error Handling

Now we move to an important **production-level agent concept**:

> What happens after the LLM chooses a tool?

In a demo, tools usually work perfectly. In production, they **fail all the time**.

---

## 1. Basic Tool Execution

Suppose the LLM generates:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Hyderabad"
  }
}
```

Your application needs to:

```text
LLM
 ↓
Tool call
 ↓
Validate arguments
 ↓
Find tool
 ↓
Execute tool
 ↓
Get result
 ↓
Send result back to LLM
```

For example:

```python
result = get_weather(city="Hyderabad")
```

Then:

```text
Tool result:
32°C, sunny
```

is sent back to the LLM.

---

# 2. What if the Tool Doesn't Exist?

Suppose the LLM generates:

```json
{
  "name": "get_stock_price",
  "arguments": {
    "symbol": "AAPL"
  }
}
```

But your application only has:

```text
calculator
get_weather
search_database
```

You should **not blindly execute it**.

Your orchestrator should detect:

```python
if tool_name not in available_tools:
    return error
```

Conceptually:

```text
LLM
 ↓
get_stock_price()
 ↓
Does tool exist?
 ↓
NO
 ↓
Tool error
 ↓
LLM
```

The LLM can then potentially recover:

> "I don't have access to a stock-price tool."

---

# 3. What if Arguments Are Invalid?

Suppose the tool requires:

```python
def calculator(a: int, b: int):
    ...
```

But the LLM generates:

```json
{
  "a": "hello",
  "b": 20
}
```

Your validation layer should catch it:

```text
Tool call
 ↓
Schema validation
 ↓
INVALID
 ↓
Return structured error
```

Don't let malformed input directly reach sensitive tools.

---

# 4. What if the Tool Itself Fails?

This is much more common.

Imagine:

```python
def get_weather(city):
    response = requests.get(...)
```

The weather API could return:

```text
500 Internal Server Error
```

or:

```text
Timeout
```

or:

```text
Connection refused
```

Your agent needs to handle this.

A robust architecture:

```text
             LLM
              ↓
          Tool Call
              ↓
         Validation
              ↓
          Execute
              ↓
       ┌──────┴──────┐
       ↓             ↓
    Success        Failure
       ↓             ↓
   Tool Result    Error Result
       ↓             ↓
       └──────┬──────┘
              ↓
             LLM
```

---

# 5. Don't Hide Errors From the Agent

Suppose the API fails.

Bad approach:

```python
try:
    result = get_weather(city)
except:
    result = None
```

Now the LLM sees:

```text
Tool result: None
```

It doesn't know what happened.

Better:

```text
Tool result:
{
    "status": "error",
    "error": "Weather API timed out"
}
```

Now the LLM can make a decision:

```text
Weather API timed out.

Should I:
- retry?
- use another tool?
- tell the user?
```

---

# 6. Retry

Some failures are temporary.

For example:

```text
API timeout
```

You might retry:

```text
Attempt 1
   ↓
Timeout
   ↓
Attempt 2
   ↓
Success
```

But don't retry indefinitely.

Use:

```text
max_retries = 3
```

Conceptually:

```python
for attempt in range(3):
    try:
        return execute_tool()
    except TimeoutError:
        continue

return error
```

---

# 7. Important: Retry vs Agent Loop

These are different.

### Tool retry

The **same tool** is attempted again:

```text
Tool
 ↓
Failure
 ↓
Retry same tool
 ↓
Success
```

### Agent loop

The **LLM decides what to do next**:

```text
Tool
 ↓
Failure
 ↓
LLM
 ↓
Try another tool
```

For example:

```text
Search API
 ↓
Failed
 ↓
Agent
 ↓
Try database instead
```

That's agent-level recovery.

---

# 8. Timeouts

Every external tool should generally have a timeout.

Imagine:

```text
Agent
 ↓
External API
 ↓
... waiting ...
 ↓
... waiting ...
 ↓
... waiting ...
```

Without a timeout, your agent could hang.

Instead:

```text
API call
 ↓
10 second timeout
 ↓
Failure
 ↓
Agent handles it
```

For production systems, you should think about:

* Connection timeout
* Read timeout
* Overall operation timeout

---

# 9. Tool Result Size

Another production problem:

Suppose your database tool returns:

```text
10 million rows
```

You shouldn't send all of that to the LLM.

Instead:

```text
Database
 ↓
Filter
 ↓
Limit
 ↓
Summarize / aggregate
 ↓
LLM
```

For example:

```sql
SELECT ...
LIMIT 20;
```

or perform aggregation in the database first.

This saves:

* Tokens
* Cost
* Latency
* Context window

---

# 10. Tool Permissions

This is extremely important.

Imagine an agent has these tools:

```text
search_customer()
get_customer()
update_customer()
delete_customer()
```

Should every user be allowed to invoke all four?

**No.**

Your application should enforce authorization:

```text
User
 ↓
Agent
 ↓
Tool requested
 ↓
Permission check
 ├── Allowed → Execute
 └── Denied → Reject
```

Never rely on the LLM to enforce security.

For example, don't assume:

> "The prompt tells the LLM not to delete customers."

That's not a security boundary.

---

# 11. Human-in-the-Loop

For dangerous operations, you may require human approval.

Example:

```text
Agent
 ↓
"Send email to 10,000 customers"
 ↓
Sensitive operation
 ↓
Human approval
 ├── Approve → Execute
 └── Reject → Stop
```

Other examples:

* Delete database records
* Transfer money
* Change production configuration
* Deploy code
* Send external communications

This becomes very important when building enterprise agents.

---

# 12. Tool Execution Architecture

A production-oriented design looks something like:

```text
                    ┌──────────────┐
                    │     LLM      │
                    └──────┬───────┘
                           ↓
                       Tool Call
                           ↓
                  ┌─────────────────┐
                  │ Tool Orchestrator│
                  └────────┬────────┘
                           ↓
                     Validate Input
                           ↓
                     Check Permission
                           ↓
                       Execute Tool
                           ↓
                 ┌─────────┴─────────┐
                 ↓                   ↓
              Success              Failure
                 ↓                   ↓
           Tool Result          Error Result
                 └─────────┬─────────┘
                           ↓
                          LLM
```

This is much closer to what you'll see in real applications.

---

# 13. Example Using Your RAG System

Imagine:

```python
search_rules(query)
```

Your agent asks:

> "Find information about rule ABC."

The RAG tool might fail because the vector DB is unavailable.

Instead of crashing:

```text
search_rules()
 ↓
pgvector unavailable
 ↓
Error
 ↓
Agent
 ↓
Could retry
 ↓
If still failing
 ↓
Tell user knowledge search is unavailable
```

This is much better than returning a hallucinated answer.

---

# 14. The Principle You Should Remember

A production agent should **never assume tools always succeed**.

Think:

```text
LLM output is untrusted
Tool arguments are untrusted
External APIs can fail
Databases can fail
Network can fail
Tools can timeout
Permissions can fail
```

Therefore:

```text
Validate
 ↓
Authorize
 ↓
Execute
 ↓
Handle errors
 ↓
Retry when appropriate
 ↓
Return structured result
```

---

## Phase 1 Progress

You've now covered:

```text
✅ What is an Agent?
✅ Agent Loop
✅ Agent vs Chain vs RAG
✅ Tool Calling
✅ Building a basic tool-calling agent
✅ Tool Schemas
✅ Tool Execution & Error Handling
```

### Next topic: **Planning**

We'll answer an important question:

> **How does an agent handle a complex task that requires multiple steps?**

We'll cover **planning, task decomposition, ReAct, and the difference between planning and simply calling tools.**
