# Phase 1 — Topic 6: Tool Schemas & Structured Arguments

Now let's understand **how an LLM knows what arguments a tool expects**.

This is a very important bridge between basic Python functions and real tool-calling APIs.

---

## 1. The problem

Suppose we have:

```python
def get_weather(city):
    ...
```

The LLM needs to know:

* What is the tool called?
* What does it do?
* What arguments does it accept?
* What type should each argument be?
* Which arguments are required?

We provide this information through a **tool schema**.

---

# 2. Tool Schema

Conceptually:

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
      }
    },
    "required": ["city"]
  }
}
```

This is essentially a **contract** between your application and the LLM.

It tells the LLM:

> "If you want to use this tool, give me a city as a string."

---

# 3. Why Schema Is Important

Suppose the user says:

> "What's the weather in Hyderabad?"

The LLM has to convert that natural language into:

```json
{
  "city": "Hyderabad"
}
```

Then your application can execute:

```python
get_weather(city="Hyderabad")
```

Without a schema, the model has less explicit information about how the function should be called.

---

# 4. Multiple Parameters

Consider:

```python
def book_flight(
    source,
    destination,
    date
):
    ...
```

The schema could be:

```json
{
  "name": "book_flight",
  "description": "Book a flight",
  "parameters": {
    "type": "object",
    "properties": {
      "source": {
        "type": "string"
      },
      "destination": {
        "type": "string"
      },
      "date": {
        "type": "string"
      }
    },
    "required": [
      "source",
      "destination",
      "date"
    ]
  }
}
```

Now if the user says:

> "Book a flight from Hyderabad to Delhi on August 20."

The LLM can produce:

```json
{
  "source": "Hyderabad",
  "destination": "Delhi",
  "date": "2026-08-20"
}
```

Your application then executes:

```python
book_flight(
    source="Hyderabad",
    destination="Delhi",
    date="2026-08-20"
)
```

---

# 5. Structured Arguments

This is the key idea.

Without structured output, an LLM might produce:

```text
Book a flight from Hyderabad to Delhi on August 20.
```

That's just text.

With tool calling, we want:

```json
{
  "source": "Hyderabad",
  "destination": "Delhi",
  "date": "2026-08-20"
}
```

Now the application can reliably process it.

So:

```text
Natural language
       ↓
      LLM
       ↓
Structured arguments
       ↓
Tool
```

---

# 6. Python Type Hints Help

You can define:

```python
def get_weather(city: str):
    ...
```

or:

```python
def calculator(a: int, b: int):
    ...
```

These type hints communicate the expected data types.

For example:

```python
calculator(
    a=10,
    b=20
)
```

is valid.

But:

```python
calculator(
    a="hello",
    b=20
)
```

is not what we want.

In modern agent frameworks, schemas can often be generated from Python definitions, Pydantic models, or similar schema definitions.

---

# 7. Pydantic

You'll encounter **Pydantic** frequently when building production AI applications.

For example:

```python
from pydantic import BaseModel


class WeatherInput(BaseModel):
    city: str
```

Now you have a structured definition of the tool's input.

Another example:

```python
class FlightInput(BaseModel):
    source: str
    destination: str
    date: str
```

This gives you validation as well as structure.

---

# 8. Why Validation Matters

Imagine the LLM generates:

```json
{
  "source": "Hyderabad",
  "destination": 123,
  "date": "tomorrow"
}
```

Your application shouldn't blindly execute this.

You want:

```text
LLM
 ↓
Generated arguments
 ↓
Schema validation
 ↓
Valid?
 ├── Yes → Execute tool
 └── No → Handle error
```

This becomes especially important for tools that perform real-world actions.

For example:

```text
delete_customer()
send_email()
transfer_money()
update_database()
```

You absolutely don't want to blindly trust arbitrary LLM-generated arguments.

---

# 9. Tool Schema vs Tool Implementation

Keep these separate in your mind.

### Tool implementation

```python
def get_weather(city):
    # Call weather API
    ...
```

This is the **actual capability**.

### Tool schema

```text
name:
get_weather

input:
city: string
```

This tells the LLM **how to use the capability**.

So:

```text
Tool implementation
       +
Tool schema
       ↓
LLM can use the tool
```

---

# 10. Tool Description Matters Too

Consider these two descriptions.

### Bad

```text
"Search"
```

### Better

```text
"Search the company's internal knowledge base for
information about Pega rules, configurations,
and upgrade changes."
```

The second description gives the LLM much more information about **when the tool should be used**.

Tool descriptions are therefore part of your agent design.

---

# 11. Example: Your RAG Tool

Suppose you expose your RAG system as:

```python
def search_rules(query: str):
    ...
```

A good tool definition might conceptually be:

```text
Name:
search_rules

Description:
Search the internal rule knowledge base for information
about rule definitions, history, dependencies, and
upgrade-related changes.

Input:
query: string
```

Then the agent can decide:

> "This question requires internal rule information, so I should call `search_rules`."

This is how your existing **RAG knowledge becomes a tool available to an agent**.

---

# 12. Tool Schema Is a Contract

This is the main thing to remember.

Think:

```text
             LLM
              ↓
      "I want to use this"
              ↓
        Tool Schema
              ↓
       Validate Input
              ↓
       Tool Execution
```

The schema defines the **contract** between the LLM and your application.

---

# Interview Question

Suppose you have:

```python
def search_customer(
    customer_id: int,
    include_orders: bool
):
    ...
```

The user says:

> "Get customer 123 and include their orders."

What structured tool arguments should the LLM generate?

And why is schema validation important before executing the function?
