# Topic 4 — Tool Arguments

Now we learn **how the LLM provides inputs to a tool**.

A tool usually needs some information to perform its job.

For example:

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"Weather in {city} is sunny."
```

Here, the tool requires one argument:

```text
city
```

---

## 1. What are tool arguments?

Tool arguments are the **input values required by a tool**.

For:

```python
get_weather(city)
```

the argument is:

```text
city
```

For:

```python
calculate_sum(a, b)
```

the arguments are:

```text
a
b
```

Example:

```python
@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two integers."""
    return a + b
```

The tool needs:

```text
a → integer
b → integer
```

---

# 2. Where do the arguments come from?

This is where tool calling becomes interesting.

User:

> "What is 25 + 30?"

The LLM sees the tool:

```text
calculate_sum
```

with arguments:

```text
a: integer
b: integer
```

The LLM can produce a tool call conceptually like:

```json
{
  "name": "calculate_sum",
  "arguments": {
    "a": 25,
    "b": 30
  }
}
```

Then LangChain/application executes:

```python
calculate_sum.invoke({
    "a": 25,
    "b": 30
})
```

Result:

```text
55
```

---

# 3. The complete flow

This is the important flow to remember:

```text
User
 │
 │ "What is 25 + 30?"
 ↓
LLM
 │
 │ decides:
 │ calculate_sum
 │
 │ arguments:
 │ a = 25
 │ b = 30
 ↓
Tool execution
 │
 ↓
calculate_sum(25, 30)
 │
 ↓
55
 │
 ↓
LLM
 │
 ↓
"25 + 30 = 55"
```

The LLM is responsible for **constructing the tool call**.

Your application/LangChain is responsible for **executing the tool**.

---

# 4. Multiple arguments

Consider:

```python
@tool
def get_order(order_id: int, customer_id: int) -> str:
    """Retrieve an order for a specific customer."""
    return f"Order {order_id} belongs to customer {customer_id}."
```

There are two arguments:

```text
order_id
customer_id
```

User:

> "Get order 500 for customer 123."

The LLM may produce:

```json
{
  "name": "get_order",
  "arguments": {
    "order_id": 500,
    "customer_id": 123
  }
}
```

---

# 5. Type hints help define arguments

Consider:

```python
@tool
def create_user(
    name: str,
    age: int,
    active: bool
):
    ...
```

LangChain can derive a schema roughly like:

```text
name   → string
age    → integer
active → boolean
```

Conceptually:

```json
{
  "name": "Sumanth",
  "age": 27,
  "active": true
}
```

This gives the LLM structured information about what arguments are expected.

---

# 6. Required arguments

Consider:

```python
@tool
def get_customer(customer_id: int):
    """Get customer information."""
    ...
```

`customer_id` is required.

The LLM shouldn't produce:

```json
{}
```

because the tool needs:

```text
customer_id
```

Instead:

```json
{
  "customer_id": 123
}
```

---

# 7. Optional arguments

You can also have optional arguments.

For example:

```python
@tool
def search_products(
    query: str,
    limit: int = 10
):
    """Search products using a query."""
    ...
```

Here:

```text
query → required
limit → optional
```

So the LLM could call:

```json
{
  "query": "laptop"
}
```

and the function uses:

```text
limit = 10
```

Or it could provide:

```json
{
  "query": "laptop",
  "limit": 5
}
```

---

# 8. Arguments can come from the user

Example:

```python
@tool
def search_customer(customer_id: int):
    """Search for a customer by customer ID."""
    ...
```

User:

> "Find customer 456."

The LLM extracts:

```text
456
```

and creates:

```text
search_customer(customer_id=456)
```

---

# 9. Arguments can come from previous tool results

This becomes especially important in **agents**.

Imagine:

```text
Tool 1:
search_customer("Sumanth")
```

returns:

```json
{
  "customer_id": 123,
  "name": "Sumanth"
}
```

Then the agent wants to call:

```text
get_orders(customer_id=123)
```

The `123` came from the **previous tool result**, not directly from the user.

So an agent can have:

```text
User
 ↓
Tool A
 ↓
Result
 ↓
LLM
 ↓
Tool B
 ↓
Result
 ↓
LLM
 ↓
Answer
```

This is one of the foundations of agent workflows.

---

# 10. Don't confuse tool arguments with Python parameters

These are related but conceptually different.

Python function:

```python
def get_customer(customer_id: int):
```

Python parameter:

```text
customer_id
```

When exposed as a tool, LangChain creates a tool schema describing that parameter.

The LLM then generates a structured tool call:

```json
{
  "customer_id": 123
}
```

LangChain maps that to the Python function:

```python
get_customer(customer_id=123)
```

So:

```text
Python parameter
        ↓
Tool schema
        ↓
LLM generates arguments
        ↓
LangChain passes arguments
        ↓
Python function
```

---

# 11. What if the LLM provides the wrong argument?

Example tool:

```python
@tool
def get_customer(customer_id: int):
    """Get customer information."""
    ...
```

But the model generates:

```json
{
  "customer_id": "hello"
}
```

That's where **validation** becomes important.

Or the model might generate:

```json
{
  "customer": 123
}
```

instead of:

```json
{
  "customer_id": 123
}
```

This is why tool schemas and validation are important.

We'll cover this in detail when we reach:

**Pydantic Schemas → Tool Validation → Tool Errors → Retries**

---

# 12. Real-world example

Suppose your agent has:

```python
@tool
def search_rule(
    rule_name: str,
    application: str
):
    """Search for a business rule in a specific application."""
    ...
```

User:

> "Find the CustomerEligibility rule in the Banking application."

The LLM needs to extract:

```text
rule_name = "CustomerEligibility"
application = "Banking"
```

and generate something like:

```json
{
  "rule_name": "CustomerEligibility",
  "application": "Banking"
}
```

Then your application executes the tool.

This pattern is extremely common in production AI applications.

---

# 13. Important interview question

### Q: How does an LLM determine tool arguments?

A strong answer:

> "The tool exposes an argument schema containing the argument names, types, and descriptions. Based on the user's request and that schema, the LLM generates a structured tool call containing the appropriate argument values. LangChain then uses those arguments to invoke the actual tool."

---

# 14. Mental model

Remember this:

```text
Tool
 │
 ├── Name
 ├── Description
 └── Arguments
       │
       ├── Name
       ├── Type
       └── Required/Optional
```

Then:

```text
User request
      ↓
LLM
      ↓
Understand request
      ↓
Choose tool
      ↓
Generate arguments
      ↓
Tool execution
```

---

## One very important distinction

**Tool selection** and **tool arguments** are two separate decisions.

For:

> "Get the weather in Hyderabad."

The LLM must decide:

### Decision 1 — Which tool?

```text
get_weather
```

### Decision 2 — What arguments?

```text
city = "Hyderabad"
```

So:

```text
"What should I call?"
        ↓
Tool selection

"What should I pass?"
        ↓
Tool arguments
```

---

### Next topic: **Pydantic Schemas**

We'll see how to define **strong, structured tool argument schemas** instead of relying only on basic Python type hints.
