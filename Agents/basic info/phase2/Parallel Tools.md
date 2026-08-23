# Phase 2 — Tool Calling

## 8. Parallel Tool Calls

**Parallel tool calling** means requesting multiple independent tools at the same time instead of waiting for one to finish before starting the next.

This is mainly useful for **reducing latency**.

---

## 1. Simple example

Suppose your agent has:

```text
get_weather(city)
get_stock_price(symbol)
```

User asks:

> "What's the weather in Hyderabad and Apple's stock price?"

These two operations are independent.

```text
             LLM
            /   \
           ↓     ↓
   get_weather   get_stock_price
       ↓             ↓
   Weather        Stock price
       \             /
        \           /
             LLM
              ↓
         Final answer
```

There is no reason to wait for the weather before getting the stock price.

---

## 2. Sequential vs parallel

### Sequential

```text
get_weather()
      ↓
result
      ↓
get_stock_price()
      ↓
result
```

If:

```text
weather = 2 sec
stock   = 3 sec
```

Total ≈ **5 seconds**.

### Parallel

```text
get_weather() ─────→ result
                         \
                          → LLM
                         /
get_stock_price() ──→ result
```

Total is approximately the slower operation:

**max(2, 3) = 3 seconds**

So parallel calls can significantly improve response time.

---

# 3. What does the LLM actually do?

This is a very important interview point.

Don't say:

> "The LLM executes both tools in parallel."

The LLM generally **generates the tool calls**.

For example, it may produce multiple tool calls conceptually:

```json
[
  {
    "name": "get_weather",
    "arguments": {
      "city": "Hyderabad"
    }
  },
  {
    "name": "get_stock_price",
    "arguments": {
      "symbol": "AAPL"
    }
  }
]
```

Then the **application/agent runtime** can execute these calls concurrently.

So:

```text
LLM
 ↓
Generates multiple tool calls
 ↓
Agent runtime
 ↓
Parallel execution
 ↓
Tool results
 ↓
LLM
```

This distinction is important.

---

# 4. When can tools be parallelized?

The key rule is:

> **Tools can run in parallel when they are independent of each other.**

For example:

```text
get_weather("Hyderabad")
get_stock_price("AAPL")
search_news("OpenAI")
```

These don't depend on one another.

They can potentially execute concurrently:

```text
             ┌─ get_weather ──────┐
             │                    │
LLM ─────────┼─ get_stock_price ──┼──→ LLM
             │                    │
             └─ search_news ──────┘
```

---

# 5. When can you NOT parallelize?

Consider:

```text
search_customer()
       ↓
customer_id
       ↓
search_orders(customer_id)
```

You cannot execute:

```text
search_orders(?)
```

before you know the `customer_id`.

Therefore:

```text
search_customer()
       ↓
     result
       ↓
search_orders(customer_id)
```

must be sequential.

Another example:

```text
create_order()
      ↓
order_id
      ↓
create_payment(order_id)
```

You need the order ID before creating the payment.

---

# 6. Parallel + Sequential can exist together

Real agents can have a combination.

Suppose the user asks:

> "Find my latest order, check whether the product is in stock, and tell me the current price."

First:

```text
search_orders()
       ↓
   order_id
```

Then suppose the result gives:

```text
product_id = P123
```

Now you can potentially run:

```text
              ┌─ check_inventory(P123)
              │
P123 ──────────┼─ get_price(P123)
              │
              └─ get_reviews(P123)
```

These three calls are independent.

So:

```text
search_orders()
       ↓
    P123
       ↓
 ┌─────┼─────────┐
 ↓     ↓         ↓
inventory price reviews
 └─────┼─────────┘
       ↓
      LLM
       ↓
 Final answer
```

This is a common production pattern.

---

# 7. Why parallel calls are important in production

Agents often use external services:

```text
Database
API
Vector DB
Search engine
Internal service
```

Each can have network latency.

If you execute everything sequentially:

```text
API 1 → wait
API 2 → wait
API 3 → wait
API 4 → wait
```

latency can become large.

Parallel execution allows:

```text
API 1 ─┐
API 2 ─┤
API 3 ─┼→ wait for all
API 4 ─┘
```

This can make an agent much faster.

---

# 8. But parallel execution has risks

You shouldn't automatically parallelize everything.

### Rate limits

Suppose your API allows:

```text
100 requests/minute
```

If your agent suddenly makes 20 parallel requests for every user, you may hit limits.

### Resource usage

Parallel database queries can increase:

* CPU usage
* Connection usage
* Memory
* Database load

### Dependencies

Some operations aren't independent.

For example:

```text
create_user()
create_user_profile(user_id)
```

The second depends on the first.

### Side effects

Be particularly careful with tools that modify data:

```text
delete_user()
send_email()
charge_card()
create_refund()
```

Parallel execution can cause unintended behavior if operations aren't independent or idempotent.

---

# 9. Read vs write tools

A useful mental model:

### Read operations

Often easier to parallelize:

```text
get_weather()
get_stock_price()
get_customer()
search_products()
```

### Write operations

Need more caution:

```text
create_order()
delete_order()
send_email()
charge_card()
create_refund()
```

This isn't an absolute rule, but writes require more attention to **ordering, duplication, consistency, and authorization**.

---

# 10. Interview Question

### "What is parallel tool calling?"

A strong answer:

> **"Parallel tool calling is when an LLM generates multiple independent tool calls and the agent runtime executes those calls concurrently. It's useful when the calls don't depend on each other's results because it reduces overall latency. Dependent calls must still be executed sequentially."**

---

# 11. The architecture to remember

```text
                    User
                      ↓
                     LLM
                      ↓
              Multiple tool calls
                      ↓
              ┌───────┼───────┐
              ↓       ↓       ↓
           Tool A   Tool B   Tool C
              ↓       ↓       ↓
              └───────┼───────┘
                      ↓
                 Tool results
                      ↓
                     LLM
                      ↓
                 Final answer
```

And if there are dependencies:

```text
Tool A
  ↓
Result A
  ↓
Tool B
  ↓
Result B
```

### The golden rule

> **Independent → Parallel**
> **Dependent → Sequential**

---

### Next topic: **Tool Errors**

This is very important for production agents and interviews: what happens when a tool **times out, returns invalid data, API is unavailable, authentication fails, or the tool itself throws an exception**.
