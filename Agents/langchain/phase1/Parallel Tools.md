# Topic 11 — Parallel Tool Calls

Now we move from **multiple tools** to **executing multiple tools efficiently**.

The key idea:

> If multiple tool calls are independent of each other, they can potentially be executed at the same time.

---

## 1. Sequential execution

Suppose the LLM requests:

```text
get_weather("Hyderabad")
get_stock_price("AAPL")
search_news("AI")
```

If we execute them one after another:

```text
get_weather
    ↓
wait
    ↓
get_stock_price
    ↓
wait
    ↓
search_news
```

If each takes 2 seconds:

```text
2 + 2 + 2 = 6 seconds
```

---

## 2. Parallel execution

If the tools don't depend on each other:

```text
             LLM
              ↓
       ┌──────┼──────┐
       ↓      ↓      ↓
   Weather   Stock   News
       ↓      ↓      ↓
       └──────┼──────┘
              ↓
           Results
              ↓
             LLM
```

They can execute concurrently.

If each takes approximately 2 seconds:

```text
max(2, 2, 2) ≈ 2 seconds
```

instead of:

```text
2 + 2 + 2 = 6 seconds
```

That's the major benefit.

---

# 3. Example

Suppose:

```python
@tool
def get_weather(city: str):
    """Get weather for a city."""
    ...


@tool
def get_stock_price(symbol: str):
    """Get stock price."""
    ...


@tool
def search_news(topic: str):
    """Search recent news."""
    ...
```

The LLM might generate:

```text
get_weather(city="Hyderabad")

get_stock_price(symbol="AAPL")

search_news(topic="AI")
```

These are independent.

There is no requirement that:

```text
weather result → stock request
```

or:

```text
stock result → news request
```

So they can potentially run concurrently.

---

# 4. Async execution in Python

For I/O-bound tools, Python's `asyncio` is commonly used.

Conceptually:

```python
import asyncio

results = await asyncio.gather(
    get_weather.ainvoke({"city": "Hyderabad"}),
    get_stock_price.ainvoke({"symbol": "AAPL"}),
    search_news.ainvoke({"topic": "AI"})
)
```

The important concept is:

```text
ainvoke()
```

means asynchronous invocation.

And:

```python
asyncio.gather(...)
```

allows multiple async operations to run concurrently.

---

# 5. Why `.ainvoke()`?

You previously saw:

```python
tool.invoke(...)
```

That's synchronous execution.

```python
result = tool.invoke(...)
```

means:

> Execute this and wait for the result.

With:

```python
await tool.ainvoke(...)
```

you can use asynchronous execution.

So:

```text
invoke()
→ synchronous

ainvoke()
→ asynchronous
```

---

# 6. Important: async doesn't automatically mean parallel

This distinction is important.

Simply writing:

```python
await tool1.ainvoke(...)
await tool2.ainvoke(...)
```

does **not** necessarily execute them concurrently.

That can still be:

```text
Tool 1
 ↓
wait
 ↓
Tool 2
```

To run independent operations concurrently, you can use something like:

```python
await asyncio.gather(
    tool1.ainvoke(...),
    tool2.ainvoke(...)
)
```

Conceptually:

```text
             gather()
              /   \
             ↓     ↓
          Tool 1 Tool 2
             ↓     ↓
             └──┬──┘
                ↓
             Results
```

---

# 7. When should you parallelize?

Only when tool calls are **independent**.

Example:

```text
get_weather(Hyderabad)
get_stock_price(AAPL)
```

Independent:

```text
Weather doesn't need stock result.
Stock doesn't need weather result.
```

Parallelization makes sense.

---

# 8. When should you NOT parallelize?

Consider:

```text
search_customer("Sumanth")
```

returns:

```json
{
    "customer_id": 123
}
```

Then:

```text
get_orders(customer_id=123)
```

The second call depends on the first.

Therefore:

```text
search_customer
      ↓
customer_id
      ↓
get_orders
```

You can't start:

```text
get_orders()
```

before knowing:

```text
customer_id
```

So this needs sequential execution.

---

# 9. A simple rule

Ask:

> **Does Tool B need the result of Tool A?**

If **yes**:

```text
A → B
```

Sequential.

If **no**:

```text
A ─┐
   ├→ Results
B ─┘
```

Potentially parallel.

---

# 10. Real-world example

Imagine an AI travel assistant.

User:

> "Find the weather in Paris, current EUR/USD exchange rate, and recent Paris travel news."

The LLM could identify:

```text
get_weather("Paris")

get_exchange_rate("EUR", "USD")

search_news("Paris travel")
```

All three are independent.

So:

```text
                    LLM
                     ↓
              ┌──────┼──────┐
              ↓      ↓      ↓
           Weather  FX     News
              ↓      ↓      ↓
              └──────┼──────┘
                     ↓
                   LLM
                     ↓
              Final response
```

This is an ideal parallel-tool scenario.

---

# 11. Multiple tool calls returned by the LLM

Conceptually, the model might return:

```python
[
    {
        "name": "get_weather",
        "args": {"city": "Paris"}
    },
    {
        "name": "get_exchange_rate",
        "args": {
            "from_currency": "EUR",
            "to_currency": "USD"
        }
    },
    {
        "name": "search_news",
        "args": {"topic": "Paris travel"}
    }
]
```

The execution layer can inspect these calls.

It determines:

```text
Are they independent?
       ↓
      Yes
       ↓
Execute concurrently
```

---

# 12. Parallel tool calls vs parallel LLM calls

Don't confuse these.

### Parallel tool calls

One LLM response requests:

```text
Tool A
Tool B
Tool C
```

and the tools execute concurrently.

### Parallel LLM calls

You actually invoke multiple model requests:

```text
LLM request 1
LLM request 2
LLM request 3
```

These are different concepts.

Our current topic is:

> **Parallel tool execution.**

---

# 13. Production benefit: latency

Suppose you have three APIs:

```text
Weather API → 800 ms
Stock API   → 500 ms
News API    → 1000 ms
```

Sequential:

```text
800 + 500 + 1000
= 2300 ms
```

Potential concurrent execution:

```text
max(800, 500, 1000)
≈ 1000 ms
```

So you can potentially reduce tool-execution latency from:

```text
2.3 seconds
```

to roughly:

```text
1 second
```

There will be overhead in a real system, so it's not always exactly the mathematical maximum.

---

# 14. Parallel execution isn't always safe

Consider:

```text
create_order()
update_inventory()
send_confirmation_email()
```

These may have dependencies.

For example:

```text
create_order
     ↓
order_id
     ↓
send_confirmation_email
```

You can't send an email containing an order ID that doesn't exist yet.

Similarly:

```text
create_order
     ↓
update_inventory
```

may have business-ordering requirements.

So don't blindly parallelize every tool.

---

# 15. Side effects make this more important

Suppose we have:

```text
delete_user()
send_email()
update_database()
```

These can change system state.

Parallel execution could create race conditions or inconsistent states.

For example:

```text
update_customer()
delete_customer()
```

running concurrently can cause unpredictable behavior.

Therefore, parallelism should consider:

* Data dependencies
* Ordering requirements
* Side effects
* Transactions
* Idempotency
* Race conditions

---

# 16. Error handling with parallel tools

Suppose we execute:

```text
Weather → SUCCESS
Stock   → SUCCESS
News    → FAILURE
```

You need to decide what the application should do.

Possible strategy:

```text
Weather → result
Stock   → result
News    → error
```

Then return all results to the LLM.

The LLM could answer:

> "I found the weather and stock information, but the news service is currently unavailable."

This is much better than failing the entire request unnecessarily.

---

# 17. Parallel tools in LangGraph

Since you're learning LangGraph as well, this concept is particularly important.

A graph can have:

```text
             START
               ↓
              LLM
          /    |    \
         ↓     ↓     ↓
     Weather  Stock  News
         \     |     /
          ↓    ↓    ↓
             LLM
              ↓
             END
```

The branches can execute concurrently when the graph structure allows it.

This is one reason graph-based agent architectures are powerful.

---

# 18. Important interview question

### Q: How would you optimize an agent that needs to call three independent APIs?

A strong answer:

> "If the three tool calls are independent, I would execute them concurrently rather than sequentially. In Python, for I/O-bound tools I could use asynchronous execution with `ainvoke()` and `asyncio.gather()`, or use the concurrency mechanisms provided by the agent framework. This reduces total latency from roughly the sum of the individual latencies to approximately the maximum latency among the calls, plus overhead."

That's a **Senior AI Engineer-level answer**.

---

# 19. The mental model

Remember:

```text
Independent
   ↓
Parallel

Dependent
   ↓
Sequential
```

For example:

```text
Weather ─────┐
Stock ───────┼──→ LLM
News ────────┘
```

versus:

```text
Search customer
       ↓
Customer ID
       ↓
Get orders
       ↓
Order details
```

---

# 20. Where we are now

You've completed:

```text
1. What is a LangChain Tool?       ✅
2. @tool                            ✅
3. Tool descriptions                ✅
4. Tool arguments                   ✅
5. Pydantic schemas                 ✅
6. Binding tools to LLM             ✅
7. LLM choosing tools               ✅
8. Tool execution                   ✅
9. Tool results                     ✅
10. Multiple tools                  ✅
11. Parallel tool calls             ✅
```

Remaining:

```text
12. Tool Errors
13. Retries
14. Tool Validation
```

### Next → Tool Errors

We'll learn what happens when a tool fails because of **invalid arguments, API failures, timeouts, database errors, authentication failures, or business errors**, and how the agent should respond instead of crashing.
