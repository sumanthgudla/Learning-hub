
# Phase 2 — Tool Calling

## 3. LLM Deciding Which Tool to Call

This is one of the **most important concepts in agent systems**.

Suppose you give the LLM 4 tools:

```text
get_customer()
search_orders()
search_products()
create_refund()
```

Now the user says:

> "Show me my latest order."

The LLM needs to determine:

```text
Which tool can satisfy this request?
```

It looks at the **tool names, descriptions, and schemas** and selects the appropriate tool.

---

## 1. The LLM receives the available tools

Conceptually, the LLM receives something like:

```text
Tools available:

1. get_customer
   Get customer information using customer ID.

2. search_orders
   Search a customer's orders.

3. search_products
   Search products by name or category.

4. create_refund
   Create a refund for an existing order.
```

Then the user says:

```text
"Show me my latest order."
```

The LLM determines:

```text
User wants order information
        ↓
search_orders is relevant
        ↓
Call search_orders
```

It may generate:

```json
{
  "name": "search_orders",
  "arguments": {
    "customer_id": "123",
    "limit": 1
  }
}
```

Your application then executes that tool.

---

# 2. The LLM does not literally run through your tools

This is an important distinction.

You might imagine:

```python
if user_wants_order:
    search_orders()
elif user_wants_customer:
    get_customer()
```

That's **your application's hard-coded logic**.

With LLM tool calling, the model is given the tools and their schemas, and the model generates a structured tool call.

Conceptually:

```text
User
 ↓
LLM
 ↓
"I need order information"
 ↓
search_orders(customer_id=123)
```

Your application then takes that tool call and executes the actual function.

---

# 3. How does the LLM know which tool is appropriate?

There are several signals.

### Tool name

```text
search_orders
```

clearly suggests orders.

### Tool description

```text
Search a customer's orders and return order details.
```

makes the purpose clearer.

### Parameter descriptions

```text
customer_id:
The unique ID of the customer.

limit:
Maximum number of orders to return.
```

help the model construct the call.

### User request

```text
"Show my latest order."
```

The model matches the user's intent against the available tools.

---

# 4. Example with multiple tools

Suppose we have:

```text
Tool A:
get_weather(city)

Tool B:
get_stock_price(symbol)

Tool C:
search_news(topic)
```

User:

> "What's Apple's stock price?"

The LLM identifies:

```text
Apple
+
stock price
        ↓
get_stock_price
```

Tool call:

```json
{
  "name": "get_stock_price",
  "arguments": {
    "symbol": "AAPL"
  }
}
```

It doesn't call:

```text
get_weather
```

because weather isn't relevant.

---

# 5. What if no tool is appropriate?

This is also important.

Suppose the available tools are:

```text
get_weather()
get_stock_price()
```

User asks:

> "Explain recursion."

Neither tool is useful.

The LLM can simply answer:

```text
"Recursion is a programming technique..."
```

So:

> **The presence of tools does not mean the LLM must always call a tool.**

It can decide:

```text
Tool needed? → Yes → call tool
Tool needed? → No  → answer directly
```

---

# 6. What if multiple tools are needed?

Now we start getting into **agentic behavior**.

Suppose tools are:

```text
get_customer()
search_orders()
create_refund()
```

User:

> "Find my latest order and refund it."

The LLM may need multiple steps:

```text
User
 ↓
LLM
 ↓
search_orders()
 ↓
Tool result
 ↓
LLM
 ↓
create_refund()
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

For example:

### Step 1

```json
{
  "name": "search_orders",
  "arguments": {
    "customer_id": "123",
    "limit": 1
  }
}
```

Tool returns:

```json
{
  "order_id": "ORD-789",
  "status": "delivered"
}
```

### Step 2

LLM sees the result and decides:

```text
I now know the order ID.
The user wants a refund.
I should call create_refund.
```

Then:

```json
{
  "name": "create_refund",
  "arguments": {
    "order_id": "ORD-789"
  }
}
```

This is the **tool loop** you learned in Phase 1.

---

# 7. Important: Tool selection is not guaranteed to be perfect

LLMs can make mistakes.

For example, suppose we have:

```text
get_order(order_id)
search_orders(customer_id)
```

User says:

> "Show my order 123."

The model might correctly choose:

```text
get_order
```

But if the descriptions are poor, it could potentially choose the wrong tool.

That's why **good tool design and clear schemas matter**.

---

# 8. Tool descriptions are almost like instructions

Bad:

```text
search()
```

Better:

```text
search_orders:
Search the customer's previous orders.
Use this when the user wants to find or inspect orders.
```

Even better:

```text
search_orders:
Search orders belonging to a customer.

Use this when:
- The user asks about previous orders.
- The user wants their latest order.
- The user wants to find an order by status.

Do not use this tool for creating, cancelling, or refunding orders.
```

This gives the LLM much stronger guidance.

---

# 9. Interview-level architecture

You should be able to explain the process like this:

```text
                 User Request
                      ↓
                     LLM
                      ↓
          ┌───────────┴───────────┐
          │                       │
     Tool needed?              No tool
          │                       │
         Yes                      ↓
          ↓                    Response
   Select appropriate
        tool
          ↓
   Generate arguments
          ↓
      Tool call
          ↓
 Application executes
        function
          ↓
     Tool result
          ↓
         LLM
          ↓
    Final response
```

---

# Key interview question

### "How does an LLM decide which tool to call?"

A strong answer:

> **"The LLM receives the available tools along with their names, descriptions, and input schemas. It compares the user's intent with the capabilities described by those tools and generates a structured tool call when a tool is appropriate. The application then executes that tool and sends the result back to the LLM. If no tool is necessary, the LLM can respond directly."**

---

## One important distinction

Don't say:

> "The LLM executes the function."

Usually, that's incorrect.

Say:

> **"The LLM generates a tool call; the application executes the tool."**

That's a very important point for interviews.

### Next: **Tool Arguments**

We'll look at how the LLM converts:

> "Get the latest 5 orders for customer 123"

into structured arguments such as:

```json
{
  "customer_id": 123,
  "limit": 5
}
```

and what happens when the arguments are missing or invalid.
