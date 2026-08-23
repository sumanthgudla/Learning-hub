# Phase 2 — Tool Calling

## 1. What is a Tool?

A **tool is an external function that an LLM can ask to use when it needs to perform an action or retrieve information.**

The important distinction is:

> **LLM decides what to do; the tool actually does it.**

For example, an LLM by itself cannot reliably:

* Query your database
* Call a REST API
* Read the current weather
* Send an email
* Execute Python
* Search your company's internal system

So we give the LLM access to **tools**.

### Simple example

Suppose the user asks:

> "What is the current weather in Hyderabad?"

Your LLM might have this tool:

```python
def get_weather(city: str):
    # Call weather API
    return {
        "city": city,
        "temperature": 32,
        "condition": "Sunny"
    }
```

The LLM doesn't directly execute this Python function.

Instead, it decides:

```text
I need weather information.
I have a get_weather tool.
I should call it with city = Hyderabad.
```

Then your application executes:

```python
get_weather("Hyderabad")
```

The tool returns:

```json
{
  "city": "Hyderabad",
  "temperature": 32,
  "condition": "Sunny"
}
```

The result goes back to the LLM, which can then answer:

> "The current weather in Hyderabad is 32°C and sunny."

---

# The Tool Calling Flow

Think of it as:

```text
User
  ↓
LLM
  ↓
Decides a tool is needed
  ↓
Tool call
  ↓
Your application executes the tool
  ↓
Tool result
  ↓
LLM
  ↓
Final answer
```

The **LLM is not the tool**.

The LLM is the **decision maker**.

The tool is the **capability**.

---

# Why do we need tools?

An LLM has limitations.

For example, imagine you ask:

> "What is the balance of customer 12345?"

The LLM doesn't know your company's database.

But you can provide:

```python
def get_customer_balance(customer_id: str):
    ...
```

Now the LLM can decide:

```text
User wants customer balance
        ↓
Need database information
        ↓
Call get_customer_balance
```

This is one of the fundamental ideas behind **AI agents**.

---

# Tool ≠ API

This is an important interview distinction.

An **API can be exposed as a tool**, but a tool doesn't necessarily have to be a REST API.

For example:

```python
def calculate_tax(amount):
    return amount * 0.18
```

This is a tool.

Another tool could call:

```text
GET https://api.weather.com/...
```

Another could query:

```sql
SELECT * FROM customers WHERE id = 123;
```

Another could execute a Python function.

So:

> **Tool = a capability exposed to the LLM in a way that the LLM can invoke.**

---

# Example with an AI Agent

Imagine a customer-support agent has three tools:

```text
get_customer()
search_orders()
create_refund()
```

User says:

> "Check my latest order and refund it."

The LLM might do:

```text
1. search_orders()
        ↓
2. get order information
        ↓
3. create_refund()
        ↓
4. tell user refund was created
```

Notice something important:

**The LLM is deciding which tools to use and in what order.**

That's what makes tool calling particularly important for agents.

---

# Tool Calling vs Normal LLM

### Normal LLM

```text
User
 ↓
LLM
 ↓
Answer
```

### LLM with tools

```text
User
 ↓
LLM
 ↓
Should I use a tool?
 ↓
YES
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Answer
```

And with an agent:

```text
User
 ↓
LLM
 ↓
Tool 1
 ↓
Result
 ↓
LLM
 ↓
Tool 2
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

This connects directly to the **agent loop** you learned in Phase 1.

---

# Interview Definition

If an interviewer asks:

> **"What is a tool in an AI agent?"**

A good answer is:

> **"A tool is an external capability exposed to an LLM that allows it to perform an action or retrieve information that it cannot reliably do by itself. The LLM decides when and which tool to call, while the application executes the tool and returns the result to the LLM."**

That's the core concept.

### Next topic

The next important concept is **Function/Tool Schema** — how we describe a tool to the LLM, including its **name, description, parameters, and parameter types**.
