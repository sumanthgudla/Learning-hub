# Phase 2 — LangChain Tool Calling

We’ll go **one topic at a time**, just like your previous learning phases.

## Topic 1 — What is a LangChain Tool?

### 1. The basic problem

An LLM can **generate text**, but by itself it usually cannot:

* Query your database
* Call an API
* Search the web
* Read a file
* Execute Python code
* Check today's weather
* Send an email
* Perform an action in another system

For example, if you ask:

> "What is the current temperature in Hyderabad?"

The LLM doesn't inherently have access to live weather data.

A **tool** gives the LLM a way to interact with an external system.

---

## 2. What is a tool?

A LangChain tool is essentially a **function that an LLM is allowed to use**.

For example:

```python
def get_weather(city):
    return f"Weather information for {city}"
```

We can expose this function to the LLM as a tool.

Conceptually:

```text
User
  ↓
LLM
  ↓
Decides: "I need weather information"
  ↓
Tool: get_weather("Hyderabad")
  ↓
External system / function
  ↓
Tool result
  ↓
LLM
  ↓
Final answer
```

The important point is:

> **The LLM decides when a tool is needed, but the tool itself performs the actual operation.**

---

## 3. Tool vs LLM

Think of it this way:

| LLM                              | Tool                  |
| -------------------------------- | --------------------- |
| Reasons about what to do         | Performs an operation |
| Generates text                   | Executes code         |
| Decides which tool may be useful | Returns actual data   |
| Cannot inherently access your DB | Can query your DB     |
| Cannot inherently call your API  | Can call your API     |

For example:

```text
User:
"What is the status of customer 123?"

LLM:
"I need customer information."

        ↓

Tool:
get_customer(123)

        ↓

Tool result:
{
    "id": 123,
    "status": "ACTIVE"
}

        ↓

LLM:
"Customer 123 is ACTIVE."
```

---

# 4. Real-world example

Suppose you're building an AI assistant for a banking application.

You could provide tools such as:

```text
get_account_balance()
get_transaction_history()
transfer_money()
get_customer_details()
```

The user says:

> "What is my current balance?"

The LLM might decide:

```text
Tool required → get_account_balance
```

Then the tool executes:

```python
get_account_balance()
```

and returns:

```text
₹85,000
```

The LLM then converts that into a natural response:

> "Your current balance is ₹85,000."

---

# 5. Why this is important for Agents

This is where **LLM → Agent** starts becoming meaningful.

Without tools:

```text
User → LLM → Answer
```

With tools:

```text
User
 ↓
LLM
 ↓
Choose tool
 ↓
Execute tool
 ↓
Observe result
 ↓
LLM
 ↓
Answer
```

And with multiple tools:

```text
                  ┌── Weather Tool
                  │
User → LLM ───────┼── Database Tool
                  │
                  ├── Search Tool
                  │
                  └── API Tool
```

The LLM becomes capable of interacting with the outside world.

---

# 6. What exactly does the LLM see?

The LLM doesn't simply receive a Python function like:

```python
def get_weather(city):
    ...
```

LangChain converts the tool into a **tool definition/schema** that the model can understand.

Conceptually:

```text
Tool name:
get_weather

Description:
Get the current weather for a city.

Arguments:
city: string
```

The LLM can then decide:

```text
I should call:

get_weather(
    city="Hyderabad"
)
```

This leads directly to the next topics:

1. `@tool`
2. Tool descriptions
3. Tool arguments
4. Pydantic schemas
5. Binding tools to an LLM
6. LLM deciding which tool to call
7. Tool execution
8. Tool results

---

## 7. Simple mental model

Remember this:

> **Tool = a function that an LLM can request to execute.**

And:

> **LLM decides WHAT to call; your application executes the tool.**

That distinction is extremely important in interviews.

### Example interview answer

If an interviewer asks:

**"What is a tool in LangChain?"**

You can say:

> "A tool in LangChain is a callable function that an LLM can invoke to interact with external systems or perform operations that the LLM cannot do by itself, such as querying a database, calling an API, searching data, or executing application logic."

---

### Next topic

**Topic 2 — Creating tools with `@tool`**

We'll learn how to convert a normal Python function into a LangChain tool and what LangChain does behind the scenes.
