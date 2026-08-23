# Topic 9 — Tool Results

Now we complete the other half of tool execution.

We already know:

```text
User
 ↓
LLM
 ↓
Tool call
 ↓
Tool execution
```

Now:

```text
Tool execution
 ↓
Tool result
 ↓
LLM
 ↓
Final answer / another tool call
```

---

## 1. What is a tool result?

A **tool result** is the output returned by the tool after it executes.

Example:

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"{city}: 31°C, Sunny"
```

The LLM requests:

```text
get_weather(city="Hyderabad")
```

The tool executes and returns:

```text
Hyderabad: 31°C, Sunny
```

That returned value is the **tool result**.

---

# 2. The complete flow

```text
User
 │
 │ "What's the weather in Hyderabad?"
 ↓
LLM
 │
 │ tool call
 ↓
get_weather(city="Hyderabad")
 │
 │ execute
 ↓
Tool result
 │
 │ "Hyderabad: 31°C, Sunny"
 ↓
LLM
 │
 ↓
"Hyderabad is currently 31°C and sunny."
```

The important part is that the **tool result goes back into the conversation context for the LLM**.

---

# 3. Why does the LLM need the result?

Suppose your tool returns:

```text
31°C, Sunny
```

The LLM can use that information to formulate a response:

> "The current temperature in Hyderabad is 31°C and it's sunny."

The tool itself doesn't necessarily need to produce a polished conversational response.

For example:

```python
@tool
def get_weather(city: str):
    """Get the current weather for a city."""
    return {
        "temperature": 31,
        "condition": "Sunny"
    }
```

The tool returns structured data:

```python
{
    "temperature": 31,
    "condition": "Sunny"
}
```

The LLM can turn that into:

> "It's currently 31°C and sunny in Hyderabad."

---

# 4. Tool result vs final answer

These are different.

### Tool result

```text
{
    "temperature": 31,
    "condition": "Sunny"
}
```

### Final answer

```text
"The weather in Hyderabad is currently 31°C and sunny."
```

Think:

```text
Tool
 ↓
Raw/structured result
 ↓
LLM
 ↓
Natural-language answer
```

---

# 5. Tool results don't have to be strings

A tool can return different kinds of data.

### String

```python
@tool
def get_name(user_id: int):
    """Get a user's name."""
    return "Sumanth"
```

Result:

```text
"Sumanth"
```

### Number

```python
@tool
def calculate_sum(a: int, b: int):
    """Calculate the sum of two integers."""
    return a + b
```

Result:

```text
30
```

### Dictionary

```python
@tool
def get_customer(customer_id: int):
    """Get customer information."""
    return {
        "id": customer_id,
        "name": "Sumanth",
        "status": "ACTIVE"
    }
```

Result:

```python
{
    "id": 123,
    "name": "Sumanth",
    "status": "ACTIVE"
}
```

### List

```python
@tool
def get_orders(customer_id: int):
    """Get customer orders."""
    return [
        {"id": 101, "status": "SHIPPED"},
        {"id": 102, "status": "DELIVERED"}
    ]
```

The important idea is:

> **A tool result contains information that the LLM can use for the next step.**

---

# 6. Tool result becomes part of the conversation

Conceptually, the conversation becomes:

```text
Human:
What's the weather in Hyderabad?

AI:
I'll call get_weather.

Tool:
Hyderabad: 31°C, Sunny

AI:
The weather in Hyderabad is 31°C and sunny.
```

The tool message is important because it tells the LLM:

> "This is the result of the tool call you requested."

---

# 7. Tool call ID

Remember from the previous topic that tool calls usually have an ID.

For example:

```text
Tool call:
id = call_123
name = get_weather
arguments = {"city": "Hyderabad"}
```

The result is associated with that call:

```text
Tool result:
tool_call_id = call_123
content = "31°C, Sunny"
```

Conceptually:

```text
AI message
    │
    └── call_123
          │
          ↓
      Tool result
          │
          └── call_123
```

This association becomes particularly important when **multiple tools are called**.

---

# 8. Tool result can trigger another tool

This is where agents become powerful.

Suppose the user says:

> "Find customer Sumanth and show his orders."

We might have:

```text
search_customer
get_orders
```

The agent could do:

```text
User
 ↓
LLM
 ↓
search_customer("Sumanth")
 ↓
Tool result
 ↓
customer_id = 123
 ↓
LLM
 ↓
get_orders(customer_id=123)
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

So a tool result isn't necessarily the end.

It can become **input/context for the next LLM decision**.

---

# 9. Multi-step agent example

Imagine:

```python
@tool
def search_customer(name: str):
    """Find a customer by name."""
    return {
        "customer_id": 123,
        "name": "Sumanth"
    }


@tool
def get_orders(customer_id: int):
    """Get orders for a customer."""
    return [
        {"order_id": 501, "status": "SHIPPED"},
        {"order_id": 502, "status": "DELIVERED"}
    ]
```

User:

> "Show me Sumanth's orders."

### Step 1

LLM chooses:

```text
search_customer
```

Arguments:

```text
name = "Sumanth"
```

Tool result:

```json
{
    "customer_id": 123,
    "name": "Sumanth"
}
```

### Step 2

The LLM sees:

```text
customer_id = 123
```

and decides:

```text
get_orders(customer_id=123)
```

Tool result:

```json
[
    {"order_id": 501, "status": "SHIPPED"},
    {"order_id": 502, "status": "DELIVERED"}
]
```

### Step 3

LLM generates:

> "Sumanth has two orders: 501, which is shipped, and 502, which is delivered."

That's the **agent loop**.

---

# 10. Tool result can cause another decision

This is a key concept.

After receiving a tool result, the LLM can decide:

```text
Should I:
    ↓
    ├── Give final answer?
    │
    └── Call another tool?
```

For example:

```text
Tool result
    ↓
LLM
    ↓
 ┌──────────────┐
 │              │
 ↓              ↓
Final answer   Another tool
```

This is what makes an agent different from a simple:

```text
User → LLM → Tool → Answer
```

An agent can have:

```text
User
 ↓
LLM
 ↓
Tool A
 ↓
Result
 ↓
LLM
 ↓
Tool B
 ↓
Result
 ↓
LLM
 ↓
Final answer
```

---

# 11. Tool result should be useful to the LLM

Consider this bad tool:

```python
@tool
def get_customer(customer_id: int):
    """Get customer information."""
    return "Done"
```

The LLM learns nothing from:

```text
"Done"
```

A better tool returns the actual information:

```python
@tool
def get_customer(customer_id: int):
    """Get customer information."""
    return {
        "id": customer_id,
        "name": "Sumanth",
        "status": "ACTIVE"
    }
```

Now the LLM has useful information.

---

# 12. Don't return unnecessary data

There's another important production consideration.

Suppose your database returns:

```json
{
    "id": 123,
    "name": "Sumanth",
    "email": "...",
    "address": "...",
    "internal_notes": "...",
    "created_at": "...",
    "updated_at": "...",
    "50_other_fields": "..."
}
```

You may not want to send all of that to the LLM.

Instead, the tool can return only what's necessary:

```json
{
    "id": 123,
    "name": "Sumanth",
    "status": "ACTIVE"
}
```

This reduces:

* Token usage
* Context size
* Latency
* Unnecessary information exposure

So a good tool should return **useful, focused results**.

---

# 13. Tool result and RAG

This is especially relevant to your AI work.

Suppose you have a tool:

```python
@tool
def search_rules(query: str):
    """Search business rules using semantic search."""
    ...
```

The tool might query:

```text
Vector DB
   ↓
Top-k documents
```

and return:

```json
[
    {
        "rule": "CustomerEligibility",
        "description": "...",
        "score": 0.92
    },
    {
        "rule": "CustomerRetention",
        "description": "...",
        "score": 0.87
    }
]
```

The LLM then uses these results to answer the user.

So your architecture could be:

```text
User
 ↓
LLM
 ↓
search_rules()
 ↓
Vector DB
 ↓
Retrieved documents
 ↓
LLM
 ↓
Answer
```

This is essentially combining **RAG + tool calling**.

---

# 14. Tool result vs observation

You'll often hear the word **observation** in agent discussions.

Conceptually:

```text
Tool call
    ↓
Tool execution
    ↓
Observation / Tool result
    ↓
LLM
```

So when someone says:

> "The agent observes the tool result."

they mean:

> The LLM receives the result produced by the tool and uses it for its next reasoning/action step.

---

# 15. What if the result is an error?

Suppose:

```text
get_customer(123)
```

returns:

```text
Customer not found
```

The LLM can potentially reason:

```text
Customer 123 doesn't exist.
```

and respond to the user.

Or perhaps it decides:

```text
Maybe I should search by name instead.
```

and calls another tool.

This leads directly into our later topic:

**Tool Errors**

---

# 16. The complete agent loop

At this point you should understand this very clearly:

```text
                   User
                     ↓
                    LLM
                     ↓
              Choose a tool
                     ↓
             Generate arguments
                     ↓
               Tool Executor
                     ↓
                Execute tool
                     ↓
                Tool Result
                     ↓
                    LLM
                     ↓
              ┌──────┴──────┐
              ↓             ↓
        Another tool     Final answer
              ↓
        Execute again
              ↓
            Result
              ↓
             LLM
```

This loop is the core of **tool-using agents**.

---

# 17. Interview question

### Q: What happens after a tool executes?

A strong answer:

> "The tool returns a result, which is associated with the original tool call and added back to the model's conversation context. The LLM then uses that result to either generate the final response or determine whether another tool call is required."

---

# 18. One more important distinction

Don't confuse:

### Tool call

```text
get_customer(customer_id=123)
```

with:

### Tool result

```json
{
    "id": 123,
    "name": "Sumanth",
    "status": "ACTIVE"
}
```

The first is:

> **What the LLM wants the system to do.**

The second is:

> **What the system actually got after doing it.**

So remember:

```text
LLM → Tool Call
Tool → Tool Result
```

---

## Your current mental model

You've now covered **9/14 topics**:

```text
1. What is a LangChain Tool?       ✅
2. @tool                            ✅
3. Tool descriptions                ✅
4. Tool arguments                   ✅
5. Pydantic schemas                 ✅
6. Binding tools to LLM             ✅
7. LLM choosing tools               ✅
8. Tool execution                   ✅
9. Tool results                     ✅
10. Multiple tools                  ← Next
11. Parallel tool calls
12. Tool errors
13. Retries
14. Tool validation
```

### Next: Multiple Tools

We'll build an LLM with **2–3 tools simultaneously** and understand how it handles requests where **one tool is needed vs multiple tools are needed**.
