# Topic 2 — Creating Tools with `@tool`

Now we'll see how to convert a normal Python function into a **LangChain tool**.

---

## 1. Normal Python function

Suppose you have:

```python
def get_weather(city):
    return f"The weather in {city} is sunny."
```

This is just a Python function.

An LLM **cannot automatically use it**.

We need to tell LangChain:

> "This function is available as a tool."

That's what `@tool` does.

---

# 2. Using `@tool`

```python
from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny."
```

Now `get_weather` is a **LangChain Tool**.

The important part is:

```python
@tool
```

This is a Python decorator.

---

## 3. What does `@tool` do?

Conceptually:

```text
Python function
      ↓
    @tool
      ↓
LangChain Tool object
      ↓
LLM can understand/use it
```

It takes information from your function such as:

* Tool name
* Description
* Arguments
* Argument types
* Function logic

and creates a tool that can be provided to an LLM.

---

# 4. Why the docstring is important

Look at this:

```python
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
    return f"The weather in {city} is sunny."
```

This part:

```python
"""Get the current weather for a city."""
```

becomes the **tool description**.

The LLM uses this description to understand:

> "When should I use this tool?"

For example:

```python
@tool
def get_weather(city: str) -> str:
    """Get the current weather for a city."""
```

versus:

```python
@tool
def get_weather(city: str) -> str:
    """Returns weather information for the specified city."""
```

Both are technically valid, but the description should clearly explain **what the tool does**.

---

# 5. Tool name

The Python function name becomes the tool name.

```python
@tool
def get_weather(city: str):
    ...
```

Tool name:

```text
get_weather
```

Another example:

```python
@tool
def search_customer(customer_id: int):
    ...
```

Tool name:

```text
search_customer
```

Another:

```python
@tool
def calculate_discount(price: float, percentage: float):
    ...
```

Tool name:

```text
calculate_discount
```

---

# 6. Type hints matter

Consider:

```python
@tool
def get_weather(city: str):
    ...
```

LangChain can understand that:

```text
city → string
```

If you have:

```python
@tool
def get_customer(customer_id: int):
    ...
```

LangChain knows:

```text
customer_id → integer
```

And:

```python
@tool
def calculate_discount(
    price: float,
    discount: float
):
    ...
```

The tool schema can represent:

```text
price    → number
discount → number
```

This becomes important when we learn **Pydantic schemas**.

---

# 7. Multiple arguments

You can have multiple arguments:

```python
@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b
```

The tool expects:

```text
a
b
```

Conceptually, the LLM can request:

```text
calculate_sum(
    a=10,
    b=20
)
```

The function executes:

```python
10 + 20
```

and returns:

```text
30
```

---

# 8. Tool execution vs tool definition

This distinction is **very important**.

When you write:

```python
@tool
def calculate_sum(a: int, b: int) -> int:
    """Calculate the sum of two numbers."""
    return a + b
```

you have **defined the tool**.

You can also directly execute it from Python:

```python
calculate_sum.invoke({
    "a": 10,
    "b": 20
})
```

Result:

```text
30
```

So there are two concepts:

```text
Tool definition
      ↓
@tool
      ↓
calculate_sum

Tool execution
      ↓
calculate_sum.invoke(...)
      ↓
30
```

Later, when an LLM is involved, the flow becomes:

```text
User
 ↓
LLM
 ↓
LLM decides:
"Call calculate_sum"
 ↓
Tool call
 ↓
calculate_sum.invoke(...)
 ↓
30
 ↓
LLM
 ↓
Final response
```

---

# 9. Complete small example

```python
from langchain_core.tools import tool


@tool
def multiply(a: int, b: int) -> int:
    """Multiply two integers."""
    return a * b


result = multiply.invoke({
    "a": 5,
    "b": 4
})

print(result)
```

Output:

```text
20
```

Notice that we didn't need an LLM here.

We're simply testing the tool itself.

---

# 10. Why use `@tool` instead of normal functions?

Because LangChain needs structured information about the function.

For example:

```python
@tool
def get_customer(customer_id: int) -> str:
    """Retrieve customer information using the customer ID."""
    ...
```

LangChain can expose something conceptually like:

```text
Name:
get_customer

Description:
Retrieve customer information using the customer ID.

Arguments:
customer_id: integer
```

The LLM can use this information to determine whether the tool is relevant.

---

# 11. Important interview concept

Don't think:

> "`@tool` makes the LLM execute my Python function."

That's not quite correct.

Think:

```text
@tool
  ↓
Creates a LangChain tool representation
  ↓
Tool can be given to the LLM
  ↓
LLM decides whether to request it
  ↓
Application/LangChain executes it
```

The LLM **doesn't directly execute arbitrary Python code**.

It produces a structured **tool call**.

Your application executes the corresponding function.

---

# 12. Real-world example

Imagine your AI application has:

```python
@tool
def search_customer(customer_id: int):
    """Search customer information by customer ID."""
    ...


@tool
def get_customer_orders(customer_id: int):
    """Get all orders for a customer."""
    ...


@tool
def cancel_order(order_id: int):
    """Cancel a customer order."""
    ...
```

Now your LLM has three capabilities:

```text
search_customer
get_customer_orders
cancel_order
```

The LLM can determine which one is appropriate based on the user's request.

For example:

> "Show me the orders for customer 123."

Potential tool call:

```text
get_customer_orders(customer_id=123)
```

---

## Key takeaway

Remember these four things:

```text
@tool
  ↓
Converts a Python function into a LangChain tool

Function name
  ↓
Tool name

Docstring
  ↓
Tool description

Type hints
  ↓
Help define the argument schema
```

### Next topic: **Tool Descriptions**

We'll focus specifically on **how the description influences the LLM's decision about when to use a tool**, which is very important when you have many tools.
