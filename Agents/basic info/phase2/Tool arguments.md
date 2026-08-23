# Phase 2 — Tool Calling

## 4. Tool Arguments

A **tool argument** is the input that the LLM provides when it decides to call a tool.

For example, we have:

```python
def get_weather(city: str):
    ...
```

Here:

```text
Tool name  → get_weather
Argument   → city
Value      → "Hyderabad"
```

The LLM needs to produce the correct value for `city`.

---

## 1. Simple example

User:

> "What's the weather in Hyderabad?"

Tool schema:

```json
{
  "name": "get_weather",
  "description": "Get the current weather for a city",
  "parameters": {
    "type": "object",
    "properties": {
      "city": {
        "type": "string"
      }
    },
    "required": ["city"]
  }
}
```

The LLM generates a tool call conceptually:

```json
{
  "name": "get_weather",
  "arguments": {
    "city": "Hyderabad"
  }
}
```

Your application then executes:

```python
get_weather("Hyderabad")
```

---

# 2. Multiple arguments

Consider:

```python
def search_orders(
    customer_id: int,
    status: str,
    limit: int
):
    ...
```

The user says:

> "Show me the last 5 delivered orders for customer 123."

The LLM extracts the required information:

```text
customer_id → 123
status      → "delivered"
limit       → 5
```

And generates:

```json
{
  "name": "search_orders",
  "arguments": {
    "customer_id": 123,
    "status": "delivered",
    "limit": 5
  }
}
```

Your application executes:

```python
search_orders(
    customer_id=123,
    status="delivered",
    limit=5
)
```

---

# 3. Where do the argument values come from?

Usually, they come from the **user's request**.

For example:

> "Find flights from Delhi to Mumbai tomorrow."

The tool might be:

```python
def search_flights(
    source: str,
    destination: str,
    date: str
):
    ...
```

The LLM extracts:

```text
source      → Delhi
destination → Mumbai
date        → tomorrow
```

and produces:

```json
{
  "name": "search_flights",
  "arguments": {
    "source": "Delhi",
    "destination": "Mumbai",
    "date": "tomorrow"
  }
}
```

---

# 4. Arguments don't always come directly from the user

This is particularly important for **agents**.

Suppose the user says:

> "Refund my latest order."

The user didn't provide an order ID.

You have:

```text
search_orders(customer_id)
create_refund(order_id)
```

The agent can do:

```text
User
 ↓
search_orders(customer_id=123)
 ↓
Result:
order_id = ORD-789
 ↓
create_refund(order_id="ORD-789")
```

Here:

```text
customer_id
```

came from the user's/session context, while:

```text
order_id
```

came from the **previous tool result**.

So tool arguments can come from:

* User input
* Conversation context
* Previous tool results
* Application/session state
* Other trusted application data

---

# 5. Required vs Optional Arguments

Consider:

```python
def search_products(
    query: str,
    category: str = None,
    limit: int = 10
):
    ...
```

Here:

```text
query     → required
category  → optional
limit     → optional
```

User:

> "Find iPhone 17."

The LLM can generate:

```json
{
  "query": "iPhone 17"
}
```

The application can use:

```text
category = None
limit = 10
```

But if the schema says:

```text
query is required
```

the LLM should provide it.

---

# 6. What happens when information is missing?

Suppose:

```python
def book_flight(
    source: str,
    destination: str,
    date: str
):
    ...
```

User:

> "Book me a flight to Mumbai."

We have:

```text
destination → Mumbai
source      → ?
date        → ?
```

The required information is missing.

The agent should **not blindly invent values**.

It should ask:

> "Sure. What city are you flying from, and what date would you like to travel?"

This is an important agent behavior.

---

# 7. Type matters

Suppose the schema says:

```json
{
  "limit": {
    "type": "integer"
  }
}
```

The expected value is:

```json
{
  "limit": 5
}
```

rather than:

```json
{
  "limit": "five"
}
```

The schema tells the LLM what type of value is expected.

Other common types:

```text
string
integer
number
boolean
array
object
```

For example:

```json
{
  "include_cancelled": {
    "type": "boolean"
  }
}
```

The LLM should generate:

```json
{
  "include_cancelled": true
}
```

---

# 8. Enums are very useful

Suppose you have:

```python
def search_orders(status):
    ...
```

Valid statuses are only:

```text
pending
shipped
delivered
cancelled
```

You can describe the argument as an enum:

```json
{
  "status": {
    "type": "string",
    "enum": [
      "pending",
      "shipped",
      "delivered",
      "cancelled"
    ]
  }
}
```

Now the LLM has a constrained set of choices.

If the user says:

> "Show delivered orders."

The LLM produces:

```json
{
  "status": "delivered"
}
```

---

# 9. Argument validation

Even with a schema, you should **validate tool arguments before executing the tool**.

For example:

```python
def create_refund(order_id, amount):
    ...
```

LLM generates:

```json
{
  "order_id": "ORD-123",
  "amount": -500
}
```

You don't want your application blindly executing that.

Your application should validate:

```text
Is order_id valid?
Is amount numeric?
Is amount > 0?
Does the order exist?
Is the user authorized?
```

Then execute the tool only if validation succeeds.

This becomes extremely important in production agents.

---

# 10. Never blindly trust LLM arguments

This is a key production/interview point.

The LLM is probabilistic.

So don't think:

```text
LLM → arguments → execute immediately
```

Instead:

```text
LLM
 ↓
Tool call
 ↓
Validate arguments
 ↓
Check permissions/business rules
 ↓
Execute tool
 ↓
Return result
```

For example, for:

```text
delete_customer(customer_id)
```

you should have authorization checks **outside the LLM**.

The LLM should not be trusted to decide:

> "This user is allowed to delete customer 123."

That should be enforced by your application/backend.

---

# 11. Complete example

User:

> "Show me the last 3 delivered orders for customer 123."

Tool:

```python
def search_orders(
    customer_id: int,
    status: str,
    limit: int
):
    ...
```

### Step 1 — LLM understands request

```text
customer_id = 123
status = delivered
limit = 3
```

### Step 2 — LLM creates tool call

```json
{
  "name": "search_orders",
  "arguments": {
    "customer_id": 123,
    "status": "delivered",
    "limit": 3
  }
}
```

### Step 3 — Application validates

```text
customer_id → valid
status → valid enum
limit → valid integer
```

### Step 4 — Application executes

```python
search_orders(123, "delivered", 3)
```

### Step 5 — Tool returns

```json
{
  "orders": [
    {"id": "ORD-100", "status": "delivered"},
    {"id": "ORD-101", "status": "delivered"},
    {"id": "ORD-102", "status": "delivered"}
  ]
}
```

Then the result goes back to the LLM, which produces the user-facing response.

---

# The complete picture so far

You have now learned:

```text
1. Tool
      ↓
2. Tool Schema
      ↓
3. LLM chooses tool
      ↓
4. LLM generates arguments
      ↓
5. Application executes tool
```

The next step is **Tool Execution** — what actually happens inside your application after the LLM generates the tool call, and how the tool result is sent back to the LLM.
