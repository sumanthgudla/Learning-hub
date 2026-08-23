# Phase 1 — Topic 5: Build Your First Tool-Calling Agent

Now let's move from theory to implementation.

The goal is to understand the **raw agent architecture**, before using LangChain or LangGraph.

We'll build a small agent with two tools:

```text
Calculator
Weather
```

---

## 1. Our architecture

The application will work like this:

```text
User
 ↓
LLM
 ↓
Does the LLM want a tool?
 ├── No → Final answer
 │
 └── Yes
      ↓
   Tool call
      ↓
   Python executes tool
      ↓
   Tool result
      ↓
   LLM
      ↓
   Final answer / another tool
```

---

# 2. Create our tools

Let's start with normal Python functions.

```python
def calculator(a: int, b: int):
    return a + b


def get_weather(city: str):
    weather = {
        "hyderabad": "32°C, sunny",
        "vizag": "30°C, cloudy",
        "bangalore": "24°C, rainy"
    }

    return weather.get(city.lower(), "Weather unavailable")
```

Notice something important:

**These are just normal Python functions.**

There is nothing "AI" about them.

The agent framework will eventually connect the LLM to these functions.

---

# 3. Give the LLM information about the tools

The LLM needs to know what tools are available.

Conceptually:

```python
tools = [
    {
        "name": "calculator",
        "description": "Add two numbers",
        "parameters": {
            "a": "integer",
            "b": "integer"
        }
    },
    {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "city": "string"
        }
    }
]
```

Think of this as telling the LLM:

> "These are the things you are allowed to do."

---

# 4. User asks a question

Suppose:

```text
What is 10 + 20?
```

The LLM receives:

```text
User:
What is 10 + 20?

Available tools:
calculator
get_weather
```

The LLM might return something conceptually like:

```json
{
    "tool": "calculator",
    "arguments": {
        "a": 10,
        "b": 20
    }
}
```

Notice:

The LLM **didn't calculate 30 itself**.

It decided:

> "I should use the calculator."

---

# 5. Our application executes the tool

Now our Python application sees:

```json
{
    "tool": "calculator",
    "arguments": {
        "a": 10,
        "b": 20
    }
}
```

It executes:

```python
result = calculator(10, 20)
```

Result:

```text
30
```

---

# 6. Send the result back to the LLM

Now we give the LLM:

```text
Tool:
calculator

Result:
30
```

The LLM can now produce:

```text
The answer is 30.
```

So the complete flow is:

```text
User
 │
 │ "What is 10 + 20?"
 ↓
LLM
 │
 │ calculator(10,20)
 ↓
Python
 │
 │ 30
 ↓
LLM
 │
 │ "The answer is 30."
 ↓
User
```

---

# 7. Now make it an actual loop

The interesting part happens when there can be **multiple tool calls**.

Imagine the user asks:

> "What is 10 + 20 and what's the weather in Vizag?"

The agent could do:

```text
                    User
                     ↓
                    LLM
                     ↓
              Choose calculator
                     ↓
                 Calculator
                     ↓
                    30
                     ↓
                    LLM
                     ↓
             Choose weather
                     ↓
                Weather API
                     ↓
            30°C, cloudy
                     ↓
                    LLM
                     ↓
                 Final answer
```

The code conceptually becomes:

```python
while True:

    response = llm(messages, tools=tools)

    if response.type == "tool_call":

        tool_name = response.tool_name
        arguments = response.arguments

        result = execute_tool(
            tool_name,
            arguments
        )

        messages.append(response)
        messages.append(result)

    else:
        print(response.text)
        break
```

**This `while` loop is the heart of the agent.**

---

# 8. The `execute_tool()` function

We need something that maps the LLM's tool name to our Python function.

```python
def execute_tool(tool_name, arguments):

    if tool_name == "calculator":
        return calculator(**arguments)

    elif tool_name == "get_weather":
        return get_weather(**arguments)

    else:
        raise ValueError("Unknown tool")
```

Now:

```python
execute_tool(
    "calculator",
    {"a": 10, "b": 20}
)
```

calls:

```python
calculator(a=10, b=20)
```

---

# 9. What's actually happening?

There are **three different components** here.

### Component 1 — LLM

Responsible for:

```text
Understanding request
        ↓
Choosing tool
        ↓
Generating arguments
        ↓
Interpreting tool result
        ↓
Generating final response
```

### Component 2 — Agent Orchestrator

Your Python code/framework.

Responsible for:

```text
Receive LLM decision
        ↓
Execute tool
        ↓
Send result back to LLM
        ↓
Continue loop
```

### Component 3 — Tools

Actual capabilities:

```text
Calculator
Database
Search
API
RAG
Email
etc.
```

So:

```text
                 LLM
                  ↓
             Decision
                  ↓
          Agent Orchestrator
                  ↓
              Tool
                  ↓
               Result
                  ↓
                 LLM
```

This separation is **very important for production architecture**.

---

# 10. Where LangChain fits

Later, instead of manually implementing:

```python
while True:
    ...
```

LangChain can provide abstractions for:

```text
LLM
Tools
Tool execution
Messages
Agent loop
```

And LangGraph gives you more explicit control over:

```text
State
Nodes
Edges
Loops
Persistence
Human approval
```

That's why we're learning the underlying concept first.

---

# 11. One important production problem

What happens if the LLM says:

```json
{
    "tool": "calculator",
    "arguments": {
        "a": "hello",
        "b": 20
    }
}
```

Our function expects:

```python
a: int
```

This can fail.

So production agents need:

```text
LLM
 ↓
Validate tool arguments
 ↓
Execute tool
 ↓
Catch errors
 ↓
Return structured error
 ↓
LLM decides what to do
```

For example:

```text
Tool failed
 ↓
Agent
 ↓
Can I fix the arguments?
 ├── Yes → Retry
 └── No → Explain failure
```

We'll cover **tool validation, retries, and error handling** later.

---

# 12. The key mental model

Don't think:

> "An agent is some magical AI framework."

Think:

```text
Agent =
    LLM
    +
    Tools
    +
    Orchestration
    +
    Loop
    +
    State
```

We'll gradually add each of these pieces.

---

## Your exercise

Don't use LangChain yet.

Write these two functions yourself:

```python
def calculator(a, b):
    ...


def get_weather(city):
    ...
```

Then write:

```python
def execute_tool(tool_name, arguments):
    ...
```

Your `execute_tool()` should support:

```text
calculator
get_weather
```

Once you're comfortable with this, **Phase 1 Topic 6 will be tool schemas and structured tool arguments**, where we'll look at how real LLM APIs represent these tool calls.
