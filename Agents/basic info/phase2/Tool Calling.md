# Phase 2 — Tool Calling

## 2. Function / Tool Schema

Now that you know what a tool is, the next question is:

> **How does the LLM know what tools are available and how to use them?**

We provide the LLM with a **tool schema**.

A tool schema is a structured description of a tool.

It tells the LLM:

1. **Tool name**
2. **What the tool does**
3. **What arguments it accepts**
4. **Type of each argument**
5. **Which arguments are required**

---

## Example

Suppose we have this Python function:

```python
def get_weather(city: str, unit: str):
    ...
```

We can describe it to the LLM roughly like this:

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string",
        "description": "Name of the city"
      },
      "unit": {
        "type": "string",
        "description": "Temperature unit: C or F"
      }
    },
    "required": ["city", "unit"]
  }
}
```

The LLM sees this information.

It now knows:

```text
Tool: get_weather

Purpose:
    Get current weather

Arguments:
    city → string
    unit → string

Required:
    city
    unit
```

---

# Why is the schema important?

Imagine you only tell the LLM:

```text
There is a function called get_weather.
```

The LLM doesn't know:

* What does it do?
* What arguments does it need?
* Should city be a string?
* What should `unit` contain?
* Which parameters are mandatory?

The schema removes this ambiguity.

---

# The LLM does NOT receive the Python function itself

This is a very important concept.

You might have:

```python
def get_weather(city: str, unit: str):
    # actual implementation
    ...
```

But the LLM doesn't need to see your implementation.

Instead, it receives something like:

```text
Name:
get_weather

Description:
Get the current weather for a city.

Arguments:
city: string
unit: string
```

So there are two separate things:

### 1. Tool implementation

Your actual code:

```python
def get_weather(city, unit):
    # Call weather API
    ...
```

### 2. Tool schema

The description given to the LLM:

```json
{
  "name": "get_weather",
  "description": "Get current weather for a city",
  ...
}
```

---

# What happens when the user asks something?

User:

> "What's the weather in Hyderabad?"

The LLM sees the available tool:

```text
get_weather(city, unit)
```

It understands:

```text
User wants weather
        ↓
get_weather can provide weather
        ↓
city = Hyderabad
        ↓
unit = ?
```

Depending on the schema and application design, it may choose an appropriate/default unit or ask the user.

The model then produces a **tool call**, conceptually:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Hyderabad",
    "unit": "C"
  }
}
```

Your application receives this and executes:

```python
get_weather("Hyderabad", "C")
```

---

# Schema controls the arguments

Suppose your tool is:

```python
def search_customer(customer_id: int):
    ...
```

Schema:

```json
{
  "name": "search_customer",
  "description": "Find a customer by ID",
  "parameters": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "integer"
      }
    },
    "required": ["customer_id"]
  }
}
```

User:

> "Find customer 123."

LLM can generate:

```json
{
  "name": "search_customer",
  "arguments": {
    "customer_id": 123
  }
}
```

Notice:

```text
customer_id → integer
```

because the schema tells the model that.

---

# Description is extremely important

Consider these two tools:

```text
search()
search_customer()
```

If you only provide names, the LLM may have difficulty deciding which one to use.

Good descriptions help:

```text
search_customer:
"Search the customer database using customer ID or email."

search_products:
"Search the product catalog using product name or category."
```

Now the model has useful information for choosing the correct tool.

### This is an important interview point:

> **Tool descriptions and parameter descriptions influence the LLM's tool-selection behavior.**

---

# Real-world example

Imagine you're building an AI assistant for an e-commerce application.

You expose:

```text
get_order
search_products
cancel_order
create_return
```

The schemas might conceptually look like:

```text
get_order
    order_id: string

search_products
    query: string

cancel_order
    order_id: string
    reason: string

create_return
    order_id: string
    item_id: string
```

User:

> "Cancel order 123 because I don't need it anymore."

The LLM can reason:

```text
User wants to cancel an order
        ↓
cancel_order is appropriate
        ↓
order_id = "123"
reason = "don't need it anymore"
```

Then generate:

```json
{
  "name": "cancel_order",
  "arguments": {
    "order_id": "123",
    "reason": "don't need it anymore"
  }
}
```

---

# Tool Schema → Tool Call

Remember this relationship:

```text
              TOOL SCHEMA
                  ↓
        tells LLM what is possible
                  ↓
               LLM
                  ↓
        decides what to call
                  ↓
             TOOL CALL
                  ↓
       name + arguments
                  ↓
          application executes
```

So:

**Schema = instructions about how a tool can be used**

**Tool call = the LLM's request to use that tool**

---

## Interview Question

If the interviewer asks:

> **"What information does a tool schema contain?"**

Answer:

> "Typically, it contains the tool's name, description, input parameters, parameter types, descriptions, and required fields. The schema gives the LLM enough information to determine whether the tool is relevant and construct valid arguments for the tool call."

---

### Next topic: **LLM deciding which tool to call**

This is where tool calling becomes interesting: when you give an LLM **5–10 tools**, how does it determine **which one to use** based on the user's request?
