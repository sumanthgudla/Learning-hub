# Topic 6 — Binding Tools to an LLM

Now we connect the two things we've learned:

```text
Tool
  +
LLM
  ↓
LLM that knows about available tools
```

In LangChain, this is commonly done using:

```python
llm.bind_tools(tools)
```

---

# 1. Why do we bind tools?

Suppose we have:

```python
@tool
def get_weather(city: str):
    """Get the current weather for a city."""
    return f"Weather in {city} is sunny."
```

The LLM doesn't automatically know this tool exists.

We need to provide the tool to the model.

```text
Before binding:

User → LLM

LLM knows nothing about get_weather
```

After binding:

```text
User → LLM
         │
         └── knows about get_weather
```

---

# 2. Basic example

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny."


llm = ChatOpenAI(model="gpt-4.1")

llm_with_tools = llm.bind_tools([get_weather])
```

The important line is:

```python
llm_with_tools = llm.bind_tools([get_weather])
```

Now the model has access to the tool's **definition**.

---

# 3. What does `bind_tools()` actually do?

This is a very important distinction.

`bind_tools()` does **not** mean:

> "Execute this tool now."

It means:

> "Make these tools available to the LLM so it can request them."

Think:

```text
bind_tools()
     ↓
Tell the LLM:
"These tools are available."
```

It doesn't execute:

```python
get_weather(...)
```

---

# 4. What information is given to the LLM?

When you do:

```python
llm.bind_tools([get_weather])
```

LangChain provides the model with the tool's structured definition.

Conceptually:

```text
Tool name:
get_weather

Description:
Get the current weather for a city.

Arguments:
city: string
```

So the model now knows:

```text
Available tool:
get_weather

When useful:
Weather-related questions

Required argument:
city
```

---

# 5. Calling the LLM

Now:

```python
response = llm_with_tools.invoke(
    "What is the weather in Hyderabad?"
)
```

The important thing is that the model may decide:

> "I need to use get_weather."

Instead of immediately returning normal text, it can return a **tool call**.

Conceptually:

```text
response
   ↓
tool_calls
   ↓
get_weather
   ↓
city = Hyderabad
```

---

# 6. Very important: binding ≠ execution

This is one of the most important concepts in LangChain tool calling.

When you do:

```python
llm_with_tools = llm.bind_tools([get_weather])
```

you have:

```text
LLM
 │
 └── knows about get_weather
```

When you do:

```python
response = llm_with_tools.invoke(...)
```

the LLM can **request**:

```text
get_weather(city="Hyderabad")
```

But that doesn't necessarily mean your Python function has already executed.

The flow is:

```text
                 bind_tools()
                     ↓
LLM ←────────────── Tools
 │
 │ invoke()
 ↓
LLM decides
 │
 ↓
Tool call request
 │
 ↓
Application executes tool
 │
 ↓
Tool result
 │
 ↓
LLM
```

This distinction becomes critical when we build agents.

---

# 7. Multiple tools

You can bind multiple tools.

```python
@tool
def get_weather(city: str):
    """Get the current weather for a city."""
    ...


@tool
def search_news(topic: str):
    """Search recent news about a topic."""
    ...


@tool
def get_stock_price(symbol: str):
    """Get the current stock price."""
    ...


llm_with_tools = llm.bind_tools([
    get_weather,
    search_news,
    get_stock_price
])
```

Now the LLM has three tools available:

```text
              LLM
               │
       ┌───────┼────────┐
       ↓       ↓        ↓
   Weather    News     Stocks
```

---

# 8. The LLM decides which tool is appropriate

Suppose the user asks:

> "What's the weather in Hyderabad?"

The LLM sees:

```text
get_weather
search_news
get_stock_price
```

It determines:

```text
Weather question
      ↓
get_weather
```

Then it can generate:

```text
tool_call:
    name = "get_weather"

arguments:
    city = "Hyderabad"
```

If the user asks:

> "What's Apple's stock price?"

It might choose:

```text
get_stock_price
```

with:

```text
symbol = "AAPL"
```

---

# 9. What does the response look like?

A tool-calling model response can contain structured tool calls.

Conceptually:

```python
response.tool_calls
```

might contain:

```python
[
    {
        "name": "get_weather",
        "args": {
            "city": "Hyderabad"
        },
        "id": "call_123"
    }
]
```

The exact structure can vary by LangChain/model version, but conceptually you should understand it as:

```text
Tool name
+
Arguments
+
Tool-call ID
```

---

# 10. Why is the tool-call ID important?

Suppose the LLM asks for:

```text
get_weather(city="Hyderabad")
```

The tool produces:

```text
Weather: Sunny, 30°C
```

The system needs to associate that result with the original tool call.

That's why tool calls typically have an ID:

```text
call_123
```

The conversation can therefore maintain:

```text
AI:
"I want to call get_weather"
ID = call_123

Tool:
"Weather is 30°C"
ID = call_123
```

This becomes especially useful when there are **multiple or parallel tool calls**.

---

# 11. Complete conceptual example

```python
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny."


llm = ChatOpenAI(model="gpt-4.1")

llm_with_tools = llm.bind_tools([get_weather])

response = llm_with_tools.invoke(
    "What is the weather in Hyderabad?"
)

print(response.tool_calls)
```

Conceptually:

```text
[
    {
        "name": "get_weather",
        "args": {
            "city": "Hyderabad"
        }
    }
]
```

At this point:

**The LLM has requested the tool.**

We haven't yet completed the entire agent loop.

---

# 12. Who actually executes the tool?

This is another important concept.

Typically:

```text
LLM
 ↓
Tool call
 ↓
Your application / LangChain agent runtime
 ↓
Python function
```

The model doesn't directly execute arbitrary Python.

For example:

```python
get_weather("Hyderabad")
```

is executed by your application/runtime.

The LLM only produces the structured request:

```text
get_weather
city = Hyderabad
```

---

# 13. `bind_tools()` vs Agent

You might wonder:

> "If `bind_tools()` lets the LLM call tools, isn't that already an agent?"

Not necessarily.

`bind_tools()` primarily gives the LLM **tool-calling capability**.

You still need logic to handle:

```text
LLM response
    ↓
Does it contain tool calls?
    ↓
Yes
    ↓
Execute tools
    ↓
Send results back to LLM
    ↓
LLM produces final answer
```

An agent framework/runtime can automate this loop.

So:

```text
bind_tools()
=
LLM knows how to request tools
```

while:

```text
Agent
=
LLM + tools + execution loop + state/control logic
```

This distinction is very important for interviews.

---

# 14. Real-world architecture

For a production application:

```text
                   ┌──────────────┐
                   │    User      │
                   └──────┬───────┘
                          ↓
                   ┌──────────────┐
                   │     LLM      │
                   │ + tool defs  │
                   └──────┬───────┘
                          ↓
                  Tool call request
                          ↓
                   ┌──────────────┐
                   │ Tool Executor│
                   └──────┬───────┘
                          ↓
              ┌───────────┼───────────┐
              ↓           ↓           ↓
           Database      API       Python
              │           │           │
              └───────────┼───────────┘
                          ↓
                     Tool result
                          ↓
                         LLM
                          ↓
                    Final answer
```

---

# 15. Interview question

### Q: What does `bind_tools()` do in LangChain?

A strong answer:

> "`bind_tools()` associates one or more tools with an LLM and exposes their names, descriptions, and argument schemas to the model. This allows the model to generate structured tool-call requests when it determines that a tool is needed. Binding the tools itself doesn't execute them; the tool call must be handled by the application or agent runtime."

---

# 16. Remember this distinction

This is the most important thing from today's topic:

```text
@tool
  ↓
Creates the tool


bind_tools()
  ↓
Makes the tool available to the LLM


LLM invocation
  ↓
LLM decides whether to request the tool


Tool execution
  ↓
Application actually runs the function
```

So the complete picture is:

```text
Python Function
      ↓
    @tool
      ↓
LangChain Tool
      ↓
  bind_tools()
      ↓
     LLM
      ↓
Tool-call decision
      ↓
Tool arguments
      ↓
Tool execution
      ↓
Tool result
      ↓
     LLM
      ↓
Final answer
```

### Next topic: **LLM Deciding Which Tool to Call**

We'll go deeper into **how the model chooses between multiple tools**, including what happens when the user asks something that doesn't require any tool.
