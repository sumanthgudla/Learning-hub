# Phase 2 — Tool Calling

## 6. Tool Results

After the application executes a tool, it produces a **tool result**.

The result is then sent back to the LLM so that the LLM can decide what to do next.

The complete flow is:

```text
User
 ↓
LLM
 ↓
Tool Call
 ↓
Application executes tool
 ↓
Tool Result
 ↓
LLM
 ↓
Final answer OR another tool call
```

---

## 1. Simple example

User:

> "What is the weather in Hyderabad?"

LLM generates:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Hyderabad"
  }
}
```

Your application executes:

```python
result = get_weather("Hyderabad")
```

Suppose the tool returns:

```json
{
  "city": "Hyderabad",
  "temperature": 32,
  "condition": "Sunny"
}
```

This is the **tool result**.

The application sends it back to the LLM.

The LLM can then respond:

> "It's currently 32°C and sunny in Hyderabad."

---

# 2. Tool result vs final answer

These are different.

### Tool result

```json
{
  "temperature": 32,
  "condition": "Sunny"
}
```

This is generally **machine-oriented structured data**.

### Final answer

```text
It's currently 32°C and sunny in Hyderabad.
```

This is **user-oriented natural language**.

The LLM converts:

```text
Tool result
     ↓
LLM
     ↓
User-friendly response
```

---

# 3. Why should tool results be structured?

Suppose your database tool returns:

```text
Customer 123 has 4 orders. The latest order was ORD-789,
placed on August 10, delivered on August 14, and cost ₹4,500.
```

The LLM can understand it.

But structured data is generally easier to work with:

```json
{
  "customer_id": 123,
  "order_count": 4,
  "latest_order": {
    "order_id": "ORD-789",
    "date": "2026-08-10",
    "status": "delivered",
    "amount": 4500
  }
}
```

Now the LLM has explicit fields.

It can easily reason:

```text
order_id = ORD-789
status = delivered
amount = 4500
```

---

# 4. Tool results can contain errors

A tool doesn't always succeed.

For example:

```text
get_customer(123)
```

might return:

```json
{
  "error": "Customer not found"
}
```

The LLM receives this result.

It can then respond:

> "I couldn't find a customer with ID 123."

Or it could potentially try another approach.

---

# 5. Tool result can trigger another tool call

This is where agents become interesting.

Suppose the user says:

> "Refund my latest order."

Available tools:

```text
search_orders()
create_refund()
```

### First tool call

```json
{
  "name": "search_orders",
  "arguments": {
    "customer_id": 123,
    "limit": 1
  }
}
```

Tool result:

```json
{
  "order_id": "ORD-789",
  "status": "delivered",
  "amount": 4500
}
```

Now the LLM sees:

```text
I have the order ID.
User wants a refund.
I should call create_refund.
```

It generates:

```json
{
  "name": "create_refund",
  "arguments": {
    "order_id": "ORD-789"
  }
}
```

Second tool executes.

Result:

```json
{
  "success": true,
  "refund_id": "REF-456",
  "amount": 4500
}
```

The LLM can finally answer:

> "Your refund of ₹4,500 has been created. The refund ID is REF-456."

So:

```text
User
 ↓
LLM
 ↓
search_orders
 ↓
Tool result
 ↓
LLM
 ↓
create_refund
 ↓
Tool result
 ↓
LLM
 ↓
Final answer
```

This is the **agent loop in action**.

---

# 6. Tool result is new information for the LLM

Think of each tool as giving the LLM a new piece of information.

For example:

```text
LLM
 │
 ├── search_customer()
 │       ↓
 │   customer information
 │
 ├── search_orders()
 │       ↓
 │   order information
 │
 └── create_refund()
         ↓
     refund information
```

The LLM uses those results to determine its next action.

---

# 7. Tool result should contain useful information

Suppose the tool performs an operation:

```python
def create_refund(order_id):
    # refund logic
    return True
```

Returning only:

```text
true
```

isn't very informative.

Better:

```json
{
  "success": true,
  "order_id": "ORD-789",
  "refund_id": "REF-456",
  "amount": 4500,
  "status": "refund_created"
}
```

Now the LLM has enough information to give a useful response.

---

# 8. Success and failure should be distinguishable

A good tool result often has a clear structure.

For example:

```json
{
  "success": true,
  "data": {
    "order_id": "ORD-789",
    "status": "delivered"
  },
  "error": null
}
```

Failure:

```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "ORDER_NOT_FOUND",
    "message": "Order ORD-789 does not exist"
  }
}
```

This makes it easier for the agent to determine what happened.

---

# 9. Don't expose unnecessary internal information

Suppose your database throws:

```text
psycopg2.errors.UniqueViolation:
duplicate key value violates unique constraint...
```

You generally shouldn't send raw internal errors directly to the user.

Instead, your tool layer can return something meaningful:

```json
{
  "success": false,
  "error": {
    "code": "CUSTOMER_ALREADY_EXISTS",
    "message": "A customer with this email already exists."
  }
}
```

The LLM can then communicate that appropriately.

---

# 10. Tool result can affect the next decision

This is the key concept to remember.

The LLM doesn't simply:

```text
Tool → Final Answer
```

It can do:

```text
Tool
 ↓
Result
 ↓
LLM evaluates result
 ↓
 ┌──────────────┬───────────────┐
 ↓              ↓               ↓
Answer       Another tool     Retry
```

For example:

```text
search_orders()
       ↓
"No orders found"
       ↓
LLM
       ↓
Ask user for another order ID
```

Or:

```text
get_customer()
       ↓
Customer found
       ↓
LLM
       ↓
search_orders()
```

Or:

```text
get_weather()
       ↓
API timeout
       ↓
LLM / runtime
       ↓
Retry
```

---

# Interview Question

### "What happens after a tool executes?"

A strong answer:

> **"The tool returns a result to the agent runtime, which passes that result back to the LLM as part of the conversation. The LLM then interprets the result and decides whether to provide the final response, call another tool, or handle an error."**

---

# Your Agent Loop So Far

You should now understand this entire cycle:

```text
                 ┌───────────────┐
                 │     User      │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │      LLM      │
                 └───────┬───────┘
                         ↓
                  Choose a tool
                         ↓
                  Generate args
                         ↓
                 ┌───────────────┐
                 │  Tool Call    │
                 └───────┬───────┘
                         ↓
                 ┌───────────────┐
                 │  Application  │
                 └───────┬───────┘
                         ↓
                 Execute function
                         ↓
                 ┌───────────────┐
                 │ Tool Result   │
                 └───────┬───────┘
                         ↓
                        LLM
                         ↓
               ┌─────────┴─────────┐
               ↓                   ↓
          Another tool         Final answer
```

### Next topic: **Multiple Tools**

We'll look at how an agent handles many tools, how it chooses between them, and the difference between **sequential tool calls** and **parallel tool calls**.
