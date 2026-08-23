# Topic 10 — Multiple Tools

So far, we've mostly worked with one tool:

```text
LLM
 ↓
get_weather()
```

Real agents usually have **many tools available at the same time**.

For example:

```text
LLM
 ├── search_customer
 ├── get_orders
 ├── get_weather
 └── search_rules
```

The LLM decides which tool or tools are appropriate for the user's request.

---

# 1. Binding multiple tools

Let's create three tools:

```python
from langchain_core.tools import tool


@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"{city}: 31°C, Sunny"


@tool
def get_stock_price(symbol: str) -> str:
    """Get the current stock price for a company."""
    return f"{symbol}: $200"


@tool
def search_news(topic: str) -> str:
    """Search for recent news about a topic."""
    return f"Recent news about {topic}"
```

Now bind all three:

```python
llm_with_tools = llm.bind_tools([
    get_weather,
    get_stock_price,
    search_news
])
```

The LLM now knows about:

```text
┌──────────────────────┐
│         LLM          │
├──────────────────────┤
│ get_weather          │
│ get_stock_price      │
│ search_news          │
└──────────────────────┘
```

---

# 2. One user request → one tool

User:

> "What's the weather in Hyderabad?"

The LLM sees the available tools and chooses:

```text
get_weather
```

with:

```text
city = Hyderabad
```

Flow:

```text
User
 ↓
LLM
 ↓
get_weather("Hyderabad")
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

---

# 3. Another request → different tool

User:

> "What's Apple's stock price?"

The same LLM has access to all three tools.

It chooses:

```text
get_stock_price
```

with:

```text
symbol = AAPL
```

So the same agent can perform completely different operations.

---

# 4. One request can require multiple tools

Now consider:

> "What's Apple's stock price and what are the latest Apple AI news?"

There are two independent tasks:

```text
Task 1:
Get stock price
       ↓
get_stock_price("AAPL")

Task 2:
Get news
       ↓
search_news("Apple AI")
```

The LLM may generate **two tool calls**.

Conceptually:

```text
LLM
 ├── get_stock_price("AAPL")
 │
 └── search_news("Apple AI")
```

This is where multiple tool calling becomes more interesting.

---

# 5. Sequential vs multiple tool calls

There are two different scenarios.

### Scenario A — One tool

```text
LLM
 ↓
Tool A
 ↓
Result
 ↓
LLM
```

### Scenario B — Multiple independent tools

```text
          LLM
         /   \
        ↓     ↓
    Tool A  Tool B
        ↓     ↓
     Result Result
         \   /
          ↓ ↓
          LLM
```

If Tool B doesn't depend on Tool A, they can potentially be executed independently.

That's the foundation for **parallel tool calls**, which is our next topic.

---

# 6. Dependent tools

Not every multiple-tool workflow can be parallelized.

Consider:

> "Find customer Sumanth and then get his orders."

First:

```text
search_customer("Sumanth")
```

returns:

```json
{
    "customer_id": 123
}
```

Now we can call:

```text
get_orders(customer_id=123)
```

The second tool depends on the first result.

Therefore:

```text
search_customer
       ↓
customer_id = 123
       ↓
get_orders
```

This must logically happen in sequence.

---

# 7. Independent tools

Now:

> "What's the weather in Hyderabad and what's Apple's stock price?"

These don't depend on each other.

```text
get_weather("Hyderabad")
```

and:

```text
get_stock_price("AAPL")
```

can conceptually execute independently:

```text
            LLM
           /   \
          ↓     ↓
      Weather   Stock
          ↓     ↓
        Result Result
           \   /
            ↓ ↓
             LLM
```

This is a candidate for **parallel execution**.

---

# 8. Tool registry

When you have many tools, it's useful to think of them as a registry.

For example:

```python
tools = [
    get_weather,
    get_stock_price,
    search_news
]
```

Bind:

```python
llm_with_tools = llm.bind_tools(tools)
```

Conceptually:

```text
Tool Registry
│
├── get_weather
├── get_stock_price
├── search_news
├── search_customer
├── get_orders
└── search_documents
```

The LLM receives the definitions of these tools.

---

# 9. Tool names should be unique

This is important.

Don't have:

```text
search
search
search
```

Instead:

```text
search_customer
search_orders
search_documents
```

Why?

Because the LLM needs to distinguish between them.

For example:

```text
search_customer
→ Search customer records

search_orders
→ Search order records

search_documents
→ Search documents
```

Clear names + clear descriptions make tool selection easier.

---

# 10. Tool descriptions become even more important

With one tool, a mediocre description may not cause much trouble.

With 20 tools, it becomes much more important.

Imagine:

```text
Tool 1:
search_customer

Tool 2:
search_customer_history

Tool 3:
search_customer_orders

Tool 4:
search_customer_profile
```

If all descriptions are vague, the LLM may choose incorrectly.

Better:

```text
search_customer
→ Find a customer using ID or name.

search_customer_history
→ Retrieve historical interactions with a customer.

search_customer_orders
→ Retrieve orders placed by a customer.

search_customer_profile
→ Retrieve profile and demographic information.
```

Now the model has clearer boundaries.

---

# 11. Tool descriptions should define responsibility

Think of every tool as having a specific responsibility.

Bad:

```text
search_data
→ Search data.
```

Better:

```text
search_customer
→ Search customer records using customer ID or name.
```

Better tool boundaries lead to better agent behavior.

---

# 12. Multiple tools in your AI/RAG applications

This is particularly relevant to your AI Engineer preparation.

Imagine you're building a **Rule Assistant**.

You might have:

```text
search_rules
get_rule_details
search_rule_history
compare_rules
validate_rule
```

User:

> "Find the CustomerEligibility rule and compare it with CustomerRetention."

The agent might need:

```text
search_rules
```

then potentially:

```text
compare_rules
```

Or perhaps:

```text
get_rule_details
```

for both rules before comparison.

The flow could become:

```text
User
 ↓
LLM
 ↓
search_rules
 ↓
Results
 ↓
LLM
 ↓
get_rule_details
 ↓
get_rule_details
 ↓
LLM
 ↓
compare_rules
 ↓
Result
 ↓
LLM
 ↓
Final answer
```

This is where tool-using agents become much more powerful than a simple RAG chain.

---

# 13. Multiple tools vs multiple agents

Don't confuse these.

### Multiple tools

One LLM has many capabilities:

```text
             LLM
          /   |   \
         /    |    \
     Tool A Tool B Tool C
```

### Multiple agents

You may have multiple specialized LLM-driven components:

```text
             Supervisor
             /        \
            ↓          ↓
       Researcher    Analyst
          ↓             ↓
       Tools          Tools
```

For now, we're focusing on **multiple tools available to one LLM**.

---

# 14. What if the LLM doesn't need any tool?

Even when 10 tools are available:

```text
LLM
├── Tool A
├── Tool B
├── Tool C
...
└── Tool J
```

the user can ask:

> "Explain what an LLM is."

The LLM can simply answer:

```text
An LLM is...
```

No tool call is necessary.

So:

```text
Many tools available
        ≠
Always call a tool
```

The LLM still decides whether a tool is useful.

---

# 15. Multiple tool calls and execution

Suppose the model produces:

```text
tool_calls = [
    {
        "name": "get_weather",
        "args": {
            "city": "Hyderabad"
        }
    },
    {
        "name": "get_stock_price",
        "args": {
            "symbol": "AAPL"
        }
    }
]
```

The execution layer needs to:

1. Identify each tool.
2. Validate its arguments.
3. Execute each tool.
4. Collect the results.
5. Return those results to the LLM.

Conceptually:

```text
                LLM
                 ↓
          Multiple tool calls
             /         \
            ↓           ↓
       get_weather   get_stock_price
            ↓           ↓
         Result       Result
             \         /
              ↓       ↓
                  LLM
                   ↓
              Final answer
```

---

# 16. Tool selection can be hierarchical

For a large application, you might have 100+ tools.

Giving every tool to the LLM all the time isn't necessarily ideal.

You might first determine:

```text
User intent
    ↓
Relevant tool group
    ↓
Specific tool
```

For example:

```text
User:
"What's the customer's order status?"

        ↓

Customer/Order tools
        ↓

get_order_status
```

This type of architecture can improve:

* Tool-selection accuracy
* Token usage
* Latency
* Maintainability

You'll encounter this concept in more advanced agent architectures.

---

# 17. Important interview distinction

### Q: Can an LLM call multiple tools?

A good answer:

> "Yes. When multiple tools are bound to a model, the model can generate multiple tool calls when the user's request requires multiple independent operations. The application or agent runtime executes those calls and returns their results to the model. If the calls are independent, they may be executed in parallel; if one depends on the result of another, they need to be executed sequentially."

That's a strong Senior AI Engineer answer.

---

# 18. The key distinction: independent vs dependent

This is the most important part of today's topic.

### Independent

```text
Weather ──────────┐
                  ├──→ LLM
Stock ────────────┘
```

Potentially parallel.

### Dependent

```text
Search customer
       ↓
customer_id
       ↓
Get orders
       ↓
LLM
```

Must be sequential.

Remember:

> **Parallelism is possible when tool calls don't depend on each other's results.**

---

# 19. Your mental model

You should now think about an agent like this:

```text
                    USER
                      ↓
                     LLM
                      ↓
             ┌────────┼────────┐
             ↓        ↓        ↓
         Weather    Search    Database
           Tool      Tool       Tool
             ↓        ↓        ↓
             └────────┼────────┘
                      ↓
                  Tool Results
                      ↓
                     LLM
                      ↓
              Another tool?
                /       \
              Yes        No
               ↓          ↓
            Execute     Answer
```

And the fundamental rule:

```text
LLM = DECIDES
TOOLS = PERFORM ACTIONS
EXECUTOR = RUNS TOOLS
RESULTS = FEED INFORMATION BACK TO LLM
```

---

## Where we are now

You've covered:

```text
1. What is a LangChain Tool?     ✅
2. @tool                          ✅
3. Tool descriptions              ✅
4. Tool arguments                 ✅
5. Pydantic schemas               ✅
6. Binding tools to LLM           ✅
7. LLM choosing tools             ✅
8. Tool execution                 ✅
9. Tool results                   ✅
10. Multiple tools                ✅
```

### Next → Parallel Tool Calls

We'll take the **independent tools** example and learn how an agent can execute:

```text
get_weather()
get_stock_price()
search_news()
```

**at the same time instead of waiting for each one**, including why this improves latency in production AI systems.
