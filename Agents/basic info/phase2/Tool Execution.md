# Phase 2 — Tool Calling

## 5. Tool Execution

Now we reach the point where the **LLM has already decided what tool to call and generated its arguments**.

The key question is:

> **Who actually executes the tool?**

Usually, **your application executes it — not the LLM.**

---

## 1. The complete flow

Suppose the user asks:

> "What's the weather in Hyderabad?"

You have:

```python
def get_weather(city: str):
    # Call weather API
    return {"temperature": 32, "condition": "Sunny"}
```

The flow is:

```text
User
 ↓
LLM
 ↓
Tool selection
 ↓
Tool arguments
 ↓
Tool call
 ↓
Your application
 ↓
Execute Python function
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

---

# 2. What does the LLM actually return?

The LLM might return something conceptually like:

```json
{
  "tool_name": "get_weather",
  "arguments": {
    "city": "Hyderabad"
  }
}
```

At this point:

**The LLM has NOT executed `get_weather()`.**

It has only said:

> "I want the application to execute `get_weather` with these arguments."

---

# 3. Your application executes the function

Your application receives:

```text
tool_name = get_weather
arguments = {"city": "Hyderabad"}
```

It can then map the tool name to an actual function:

```python
tools = {
    "get_weather": get_weather,
    "search_orders": search_orders
}
```

Then:

```python
tool = tools["get_weather"]

result = tool(city="Hyderabad")
```

The function executes.

Maybe it calls a weather API:

```python
def get_weather(city):
    response = requests.get(
        "https://weather-api.com",
        params={"city": city}
    )

    return response.json()
```

---

# 4. Tool result

Suppose the tool returns:

```json
{
  "city": "Hyderabad",
  "temperature": 32,
  "condition": "Sunny"
}
```

Your application then sends this result **back to the LLM**.

The LLM now has:

```text
User:
What's the weather in Hyderabad?

Assistant:
I called get_weather.

Tool:
{
  "city": "Hyderabad",
  "temperature": 32,
  "condition": "Sunny"
}
```

The LLM can now formulate the final response:

> "It's currently 32°C and sunny in Hyderabad."

---

# 5. Why send the result back to the LLM?

Because the LLM needs to interpret the result.

Imagine the tool returns:

```json
{
  "temperature": 32,
  "condition": "Sunny",
  "humidity": 68
}
```

The tool doesn't necessarily know how to communicate with the user.

The LLM can transform that into:

> "It's 32°C and sunny in Hyderabad, with 68% humidity."

So:

```text
Tool
 ↓
Raw/structured result
 ↓
LLM
 ↓
Natural-language response
```

---

# 6. Tool execution can be anything

A tool doesn't have to be a simple Python function.

It could:

### Call a REST API

```python
def get_customer(customer_id):
    return requests.get(
        f"https://api.company.com/customers/{customer_id}"
    ).json()
```

### Query a database

```python
def get_customer_orders(customer_id):
    return db.execute(
        "SELECT * FROM orders WHERE customer_id = %s",
        (customer_id,)
    )
```

### Search a vector database

```python
def search_documents(query):
    return vector_db.similarity_search(query)
```

### Execute business logic

```python
def calculate_discount(customer_id):
    ...
```

### Call another service

```python
def create_ticket(description):
    ...
```

This is why tools make agents powerful.

---

# 7. Tool execution should be controlled

A production application shouldn't blindly execute whatever the LLM asks.

For example:

```text
delete_user(user_id)
```

The LLM might generate:

```json
{
  "user_id": 123
}
```

Your application should perform checks:

```text
Is the user authenticated?
        ↓
Is the user authorized?
        ↓
Is user 123 allowed to be deleted?
        ↓
Are business rules satisfied?
        ↓
Execute deletion
```

So the architecture should be:

```text
LLM
 ↓
Tool call
 ↓
Validation
 ↓
Authorization
 ↓
Business rules
 ↓
Tool execution
```

**Never use the LLM as your security layer.**

---

# 8. Tool errors

What if the tool fails?

For example:

```python
def get_weather(city):
    response = requests.get(...)
    response.raise_for_status()
```

The weather API might be down.

Your application could return:

```json
{
  "error": "Weather service unavailable"
}
```

Then the result goes back to the LLM.

The LLM can decide what to do next:

> "I'm unable to retrieve the current weather right now."

Or potentially try another available tool.

This leads directly to the next important concept:

**Tool errors and retry mechanisms.**

---

# 9. Agent loop

Put everything together:

```text
                 User
                   ↓
                  LLM
                   ↓
             Need a tool?
              ↙       ↘
            No         Yes
            ↓           ↓
         Answer    Select tool
                        ↓
                  Generate args
                        ↓
                   Tool call
                        ↓
                  Application
                        ↓
                 Validate args
                        ↓
                  Execute tool
                        ↓
                   Tool result
                        ↓
                       LLM
                        ↓
              ┌─────────┴─────────┐
              ↓                   ↓
          Need another         Finished
             tool?                ↓
              ↓                Answer
             Yes
              ↓
          Tool again
```

This is the **agent loop** you learned in Phase 1.

---

# Interview Question

### "Does the LLM execute the tool?"

A strong answer:

> **"No. The LLM generates a structured tool call containing the tool name and arguments. The application or agent runtime receives that call, validates it, executes the actual function or external service, and sends the tool result back to the LLM."**

That distinction is **very important in interviews**.

---

## What you have learned so far

```text
1. What is a Tool?
        ↓
2. Tool Schema
        ↓
3. LLM decides which tool to call
        ↓
4. LLM generates tool arguments
        ↓
5. Application executes the tool
        ↓
6. Tool returns result
        ↓
7. Result goes back to LLM
```

### Next: **Tool Results**

We'll cover how tool results are represented, why the result should usually be structured, and how the LLM uses the result to decide whether to **answer, call another tool, or retry**.
