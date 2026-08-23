# Topic 7 — LLM Deciding Which Tool to Call

This is one of the **most important concepts in agent systems**.

The LLM doesn't blindly execute every tool you give it.

Instead, it looks at:

* User's request
* Tool names
* Tool descriptions
* Tool argument schemas
* Conversation context

and decides:

> **Should I call a tool? If yes, which one? And what arguments should I provide?**

---

# 1. Basic example

Suppose we give the LLM three tools:

```python
@tool
def get_weather(city: str):
    """Get the current weather for a city."""
    ...


@tool
def search_news(topic: str):
    """Search for recent news about a topic."""
    ...


@tool
def get_stock_price(symbol: str):
    """Get the current stock price."""
    ...
```

We bind them:

```python
llm_with_tools = llm.bind_tools([
    get_weather,
    search_news,
    get_stock_price
])
```

Now the LLM has three possible tools.

---

# 2. User asks a weather question

User:

> "What's the weather in Hyderabad?"

The LLM analyzes the request.

```text
User request
     ↓
"What is the weather in Hyderabad?"
     ↓
Available tools
     ↓
get_weather
search_news
get_stock_price
     ↓
Best match
     ↓
get_weather
```

It generates a tool call approximately like:

```text
get_weather(
    city="Hyderabad"
)
```

---

# 3. User asks a news question

User:

> "What are the latest AI news?"

The LLM sees:

```text
Weather tool
News tool
Stock tool
```

and selects:

```text
search_news
```

with:

```text
topic = "AI"
```

Conceptually:

```json
{
    "name": "search_news",
    "arguments": {
        "topic": "AI"
    }
}
```

---

# 4. User asks a stock question

User:

> "What's Apple's stock price?"

The LLM selects:

```text
get_stock_price
```

and generates:

```json
{
    "name": "get_stock_price",
    "arguments": {
        "symbol": "AAPL"
    }
}
```

Notice that the LLM has made **two decisions**:

```text
Decision 1:
Which tool?

→ get_stock_price

Decision 2:
What arguments?

→ symbol = "AAPL"
```

---

# 5. How does the LLM know which tool to use?

This is where **tool descriptions** become important.

Suppose the model receives:

```text
Tool 1:
get_weather
"Get current weather for a city."

Tool 2:
search_news
"Search recent news about a topic."

Tool 3:
get_stock_price
"Get current stock price for a company."
```

The model can map the user's intent to the appropriate tool.

Conceptually:

```text
User intent
    ↓
Compare against tool descriptions
    ↓
Find best matching tool
    ↓
Generate tool call
```

The LLM isn't necessarily using a simple keyword lookup.

It's using its language understanding to determine which tool best matches the request.

---

# 6. What if no tool is needed?

This is extremely important.

Suppose the same tools are available:

```text
get_weather
search_news
get_stock_price
```

User asks:

> "What is 2 + 2?"

The LLM may decide:

```text
No tool required.
```

and simply answer:

> "2 + 2 = 4."

So:

```text
User
 ↓
LLM
 ↓
Does a tool help?
 ├── Yes → tool call
 └── No  → normal response
```

**Binding a tool does not force the LLM to use it.**

---

# 7. Example

```python
response = llm_with_tools.invoke(
    "Explain what RAG is."
)
```

The model could return a normal response:

```text
"RAG stands for Retrieval-Augmented Generation..."
```

There may be:

```python
response.tool_calls
```

with no tool calls.

That's perfectly valid.

---

# 8. Tool selection is based on context

Consider:

```text
User:
"What is the weather in Hyderabad?"
```

The model chooses:

```text
get_weather
```

Now imagine:

```text
User:
"What is the weather there?"
```

If previous conversation said:

```text
User:
"I'm traveling to Hyderabad."

Assistant:
"Nice!"
```

then the model may infer:

```text
there = Hyderabad
```

and call:

```text
get_weather(city="Hyderabad")
```

This is why **conversation state/context** matters for agents.

---

# 9. Ambiguous requests

Suppose the user asks:

> "Tell me about Apple."

Which tool should the model use?

Potentially:

```text
get_stock_price
```

But the user could mean:

* Apple company
* Apple stock
* Apple products
* Apple news

The model may not have enough information.

A good agent may ask:

> "Do you mean Apple's stock price, recent news, or information about the company?"

This is better than blindly selecting a tool.

---

# 10. Tool descriptions can reduce ambiguity

Suppose we have:

```python
@tool
def get_stock_price(symbol: str):
    """Get the current market price of a publicly traded company."""
```

and:

```python
@tool
def search_news(topic: str):
    """Search recent news articles about a company or topic."""
```

For:

> "What's happening with Apple recently?"

The model may choose:

```text
search_news
```

because "recently" suggests current news.

But:

> "How much is Apple trading at?"

would strongly suggest:

```text
get_stock_price
```

---

# 11. Multiple tools can be relevant

Suppose the user asks:

> "What's Apple's stock price and what are the latest Apple AI announcements?"

There are two distinct tasks:

```text
Task 1
→ get_stock_price

Task 2
→ search_news
```

The model may produce **multiple tool calls**:

```text
get_stock_price(symbol="AAPL")

search_news(topic="Apple AI announcements")
```

This leads into the next topic:

**Multiple Tools / Parallel Tool Calls.**

---

# 12. Tool selection is not hardcoded

A common misconception is:

> "LangChain checks the user's text and decides which tool to call."

Usually, that's not what is happening.

The LLM is given the available tools and decides which tool call to produce.

Conceptually:

```text
                Tools
                  ↓
            ┌───────────┐
User ─────→ │    LLM    │
            └─────┬─────┘
                  ↓
          Tool call decision
```

LangChain provides the framework and tool definitions.

The model performs the language-level decision.

---

# 13. Important distinction: LLM vs tool executor

This is worth remembering for interviews.

### LLM

Responsible for:

```text
Understanding request
       ↓
Choosing tool
       ↓
Generating arguments
```

### Tool executor

Responsible for:

```text
Receiving tool call
       ↓
Finding actual function
       ↓
Executing function
       ↓
Returning result
```

So:

```text
                 LLM
                  │
          "Call get_weather"
                  │
                  ↓
             Executor
                  │
          get_weather(...)
                  │
                  ↓
              Result
```

---

# 14. What happens internally?

A simplified flow:

```text
1. User sends message
        ↓
2. LLM receives message + tool definitions
        ↓
3. LLM analyzes the request
        ↓
4. LLM determines whether a tool is needed
        ↓
5. If needed, selects a tool
        ↓
6. Generates arguments
        ↓
7. Returns structured tool call
```

For example:

```text
User:
"What's the weather in Vizag?"
```

LLM produces something conceptually like:

```json
{
    "name": "get_weather",
    "arguments": {
        "city": "Vizag"
    }
}
```

The LLM hasn't executed the function yet.

---

# 15. Very important: the LLM can make mistakes

Tool selection isn't guaranteed to be perfect.

For example:

```text
User:
"Give me recent news about Tesla."
```

The model might incorrectly choose:

```text
get_stock_price
```

instead of:

```text
search_news
```

This is why production agents need:

* Clear tool descriptions
* Good schemas
* Validation
* Tool-level error handling
* Guardrails
* Retries
* Sometimes explicit routing logic

---

# 16. Production example

Imagine your AI system has:

```text
search_customer
get_customer_details
search_orders
get_order_details
cancel_order
create_order
```

User says:

> "Cancel order 456."

The LLM should ideally determine:

```text
Intent:
Cancel an order

Tool:
cancel_order

Argument:
order_id = 456
```

Then:

```text
LLM
 ↓
cancel_order(order_id=456)
 ↓
Tool executor
 ↓
Order cancelled
 ↓
LLM
 ↓
"Order 456 has been cancelled."
```

---

# 17. A useful mental model

Think of the LLM as a **router**.

```text
                  User Request
                       ↓
                      LLM
                       ↓
             ┌─────────┼─────────┐
             ↓         ↓         ↓
          Weather     News      Stock
            Tool      Tool       Tool
```

The LLM asks itself:

> "Which capability can best satisfy this request?"

Then it generates the appropriate tool call.

---

# 18. Interview question

### Q: How does an LLM decide which tool to call?

A strong answer:

> "When tools are bound to the model, the model receives their names, descriptions, and input schemas. Given the user's request and conversation context, the model determines whether a tool is needed and, if so, selects the tool that best matches the user's intent and generates the required arguments. The application or agent runtime then executes the requested tool."

---

# 19. The full picture so far

You've now learned:

```text
1. What is a Tool?
        ↓
2. @tool
        ↓
3. Tool Description
        ↓
4. Tool Arguments
        ↓
5. Pydantic Schema
        ↓
6. bind_tools()
        ↓
7. LLM chooses tool
```

So the current architecture is:

```text
                    User
                      ↓
                     LLM
                      ↑
              Tool definitions
                      ↑
              ┌───────┴───────┐
              │               │
          Tool A            Tool B
              │               │
              └───────┬───────┘
                      ↓
                Tool execution
```

The **next missing piece** is what happens after the LLM chooses the tool.

# Next topic — Tool Execution

We'll take a generated tool call like:

```text
get_weather(city="Hyderabad")
```

and see **how LangChain actually executes the Python function and sends the result back to the LLM**.
