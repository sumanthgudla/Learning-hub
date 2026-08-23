# Topic 3 — Tool Descriptions

Tool descriptions are **very important** because the LLM uses them to understand **what a tool does and when it should use it**.

---

## 1. Simple example

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"Weather in {city} is sunny."
```

Here:

```python
"""Get the current weather for a city."""
```

is the **tool description**.

Conceptually, the LLM sees:

```text
Tool name: get_weather

Description:
Get the current weather for a city.

Arguments:
city: string
```

The LLM uses this information when deciding whether to call the tool.

---

# 2. Why does the description matter?

Suppose you have these tools:

```text
get_weather
search_news
get_stock_price
search_customer
```

User asks:

> "What's the weather in Hyderabad?"

The LLM needs to determine:

```text
Which tool is relevant?
```

It looks at the available tool information.

```text
get_weather
→ Get the current weather for a city.

search_news
→ Search for recent news articles.

get_stock_price
→ Get the current stock price.

search_customer
→ Find customer information.
```

It can determine:

```text
User wants weather
        ↓
get_weather is relevant
        ↓
Call get_weather
```

---

# 3. Bad description

Consider:

```python
@tool
def get_weather(city: str):
    """Get information."""
    ...
```

This doesn't tell the LLM much.

What information?

```text
Weather?
Customers?
News?
Stock?
Orders?
```

The model has less information for making the tool-selection decision.

---

# 4. Better description

```python
@tool
def get_weather(city: str):
    """Get the current weather conditions for a specific city."""
    ...
```

Much better.

The LLM understands:

```text
Purpose → weather
Input → city
```

---

# 5. Very good description

You can be more specific:

```python
@tool
def get_weather(city: str):
    """
    Get the current weather conditions for a specific city.
    Use this tool when the user asks about current temperature,
    weather conditions, or forecast information.
    """
    ...
```

Now the tool description tells the model:

### What does it do?

```text
Get weather conditions
```

### When should it be used?

```text
When the user asks about:
- temperature
- weather
- forecast
```

This helps tool selection.

---

# 6. Description should define the tool's responsibility

Imagine you have two tools:

```python
@tool
def search_customers(query: str):
    """Search customer records."""
    ...


@tool
def search_orders(query: str):
    """Search order records."""
    ...
```

User asks:

> "Find order 12345."

The model should select:

```text
search_orders
```

Clear descriptions make this easier.

---

# 7. Avoid overlapping descriptions

Bad:

```python
@tool
def search_customers(query: str):
    """Search information."""
```

```python
@tool
def search_orders(query: str):
    """Search information."""
```

Now both tools look almost identical.

The LLM may have difficulty determining which one to use.

Better:

```python
@tool
def search_customers(query: str):
    """Search customer records by customer name or customer ID."""
```

```python
@tool
def search_orders(query: str):
    """Search order records by order ID or customer ID."""
```

Now the distinction is clear.

---

# 8. Description + arguments

Tool descriptions should also make the arguments understandable.

Example:

```python
@tool
def get_customer(customer_id: int):
    """
    Retrieve customer information using the customer's unique ID.
    Use this when the user asks for customer profile information.
    """
    ...
```

The LLM sees something conceptually like:

```text
Tool:
get_customer

Description:
Retrieve customer information using the customer's unique ID.
Use this when the user asks for customer profile information.

Arguments:
customer_id: integer
```

So if the user says:

> "Show me customer 123."

The LLM can generate:

```text
get_customer(
    customer_id=123
)
```

---

# 9. Description is not instructions for the user

A common misunderstanding:

```python
"""Get customer information."""
```

isn't shown to the user as the normal response.

It primarily provides information to the **model/tool-calling system**.

The user sees something like:

> "Customer 123 is active."

not:

> "I selected the `get_customer` tool because its description says..."

---

# 10. Real-world Agent example

Imagine your AI agent has:

```text
Tools
│
├── search_rules
├── get_rule_details
├── compare_rules
├── create_rule
└── delete_rule
```

For your kind of AI-engineering application, descriptions could be:

```python
@tool
def search_rules(query: str):
    """Search existing business rules using keywords or natural-language descriptions."""
```

```python
@tool
def get_rule_details(rule_name: str):
    """Retrieve the complete configuration and metadata for a specific business rule."""
```

```python
@tool
def compare_rules(rule_a: str, rule_b: str):
    """Compare two business rules and identify differences in their configuration."""
```

Now the LLM has a much better understanding of each tool's purpose.

---

# 11. Think of descriptions as a tool's "resume"

A useful mental model:

```text
Tool
 │
 ├── Name
 │
 ├── Description  ← What can I do?
 │
 ├── Arguments    ← What do I need?
 │
 └── Function     ← How do I actually do it?
```

The LLM primarily uses the **name + description + argument schema** to decide what to request.

---

# 12. Interview question

### Q: Why are tool descriptions important?

A good answer:

> "Tool descriptions help the LLM understand the purpose and appropriate usage of each tool. When multiple tools are available, the model uses their names, descriptions, and schemas to determine which tool best matches the user's request. Clear and specific descriptions improve tool-selection accuracy."

---

## Key takeaway

Remember:

```text
Good tool description
        ↓
LLM understands tool purpose
        ↓
Better tool selection
        ↓
Better agent behavior
```

**Next topic: Tool Arguments**

We'll learn how the LLM determines **what values to pass to a tool**, e.g. how:

> `"What's the weather in Hyderabad?"`

becomes:

```text
get_weather(city="Hyderabad")
```

and why argument schemas are important.
