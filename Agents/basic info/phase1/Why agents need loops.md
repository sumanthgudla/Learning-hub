# Phase 1 — Agent Fundamentals

## Topic 8: Why Agents Need Loops

This is one of the **most important concepts in agentic AI**.

You already know:

* LLM → generates an answer
* Tool calling → allows the LLM to use external tools
* State → stores information between steps

Now we connect them:

> **An agent uses a loop because it often cannot solve a task in one LLM call.**

---

# 1. Normal LLM vs Agent

### Normal LLM

```text
User
 ↓
LLM
 ↓
Answer
```

One request → one response.

For example:

> "Explain RAG."

The LLM can answer immediately.

---

### Agent

An agent may need to perform several actions:

```text
User
 ↓
LLM
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Another Tool
 ↓
Result
 ↓
LLM
 ↓
Final Answer
```

That's a **loop**.

---

# 2. Simple example

Suppose the user asks:

> "Find the current stock price of Microsoft and tell me whether it increased today."

The LLM cannot reliably answer this from its training knowledge because it needs current information.

The agent might do:

### Iteration 1

```text
LLM:
I need the current Microsoft stock price.

Action:
get_stock_price("MSFT")
```

Tool returns:

```text
$520
```

---

### Iteration 2

The LLM now has:

```text
Current price = $520
```

But the user asked whether it increased.

The agent needs another piece of information:

```text
Previous close = $515
```

So:

```text
LLM
 ↓
get_previous_close("MSFT")
```

Tool returns:

```text
$515
```

---

### Iteration 3

Now the LLM has:

```text
Current = $520
Previous = $515
```

It can calculate:

```text
Increase = $5
```

And answer:

> Microsoft is up $5 today.

The agent needed **multiple iterations**.

---

# 3. The Agent Loop

The general pattern is:

```text
┌─────────────────────┐
│       Observe       │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│       Reason        │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│        Act          │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   Observe result    │
└──────────┬──────────┘
           ↓
        Continue?
       /          \
     Yes           No
      │             │
      └──→ Loop     ↓
               Final Answer
```

The important part is:

```text
Continue?
```

The agent decides whether it has enough information to finish.

---

# 4. Why can't we just use one LLM call?

Because many tasks are **dynamic**.

Consider:

> "Find the cheapest flight from Hyderabad to London next weekend, check the baggage allowance, and tell me whether the cheapest option allows 23kg baggage."

The agent doesn't know beforehand exactly what it needs to do.

It may need:

```text
1. Search flights
2. Compare prices
3. Select cheapest flight
4. Search baggage policy
5. Check baggage allowance
6. Compare against 23kg
7. Answer
```

The number and type of steps may change depending on the results.

That's the key reason agents use loops.

---

# 5. Loop enables dynamic decision making

Suppose:

```text
Search flights
     ↓
Cheapest flight = Airline A
     ↓
Check baggage
     ↓
Airline A allows 15kg
     ↓
Not enough
     ↓
Check next cheapest flight
     ↓
Airline B allows 23kg
     ↓
Answer
```

The next action depends on the **previous tool result**.

You cannot completely determine the workflow beforehand.

This is called **dynamic execution**.

---

# 6. Loop + State

This is where your previous topic becomes important.

The loop needs state.

For example:

```python
state = {
    "user_query": "...",
    "search_results": [],
    "selected_flight": None,
    "baggage_info": None,
    "final_answer": None
}
```

Iteration 1:

```text
Search flights
```

State:

```python
{
    "search_results": [...]
}
```

Iteration 2:

```text
Select cheapest flight
```

State:

```python
{
    "search_results": [...],
    "selected_flight": "Airline A"
}
```

Iteration 3:

```text
Check baggage
```

State:

```python
{
    "search_results": [...],
    "selected_flight": "Airline A",
    "baggage_info": "15kg"
}
```

The state allows the loop to continue intelligently.

---

# 7. Loop enables retries

Another important reason for loops is **failure handling**.

Suppose:

```text
Agent
 ↓
API call
 ↓
ERROR
```

A non-agentic workflow might simply fail.

An agent can reason:

```text
Tool failed.

Maybe the API requires a different parameter.

Retry with corrected parameter.
```

Then:

```text
Agent
 ↓
Tool
 ↓
Error
 ↓
Agent
 ↓
Retry
 ↓
Success
```

So loops allow:

* Retry
* Correction
* Alternative tools
* Recovery from errors

---

# 8. Loop enables verification

Suppose an agent needs to generate SQL.

It produces:

```sql
SELECT * FROM customers WHERE age > 30;
```

The agent could execute it.

The database returns:

```text
ERROR: column "age" doesn't exist
```

The agent sees the error and tries again:

```sql
SELECT * FROM customers WHERE customer_age > 30;
```

Database:

```text
Success
```

This is a very useful agent pattern:

```text
Generate
 ↓
Execute
 ↓
Check result
 ↓
Fix
 ↓
Execute again
```

Without a loop, there is no natural mechanism for iterative correction.

---

# 9. Loop enables multi-step reasoning through actions

Be careful with the term **reasoning** here.

The important point isn't that the agent exposes its private chain-of-thought.

Instead, from an architecture perspective, the agent can make a decision, take an action, observe the result, and make the next decision.

For example:

```text
Decision:
Search customer

Action:
search_customer()

Observation:
Customer found

Decision:
Get order history

Action:
get_orders()

Observation:
3 orders found

Decision:
Check latest order

Action:
get_order_status()

Observation:
Delayed

Decision:
Answer user
```

This is much more powerful than:

```text
User → LLM → Answer
```

---

# 10. Why the loop is the "agentic" part

This is a useful way to think about it:

### LLM

```text
Input → Output
```

### RAG

```text
Question
 ↓
Retrieve
 ↓
LLM
 ↓
Answer
```

Usually a relatively fixed pipeline.

### Agent

```text
Input
 ↓
LLM
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
LLM
 ↓
Decision
 ↓
Tool
 ↓
Observation
 ↓
...
 ↓
Answer
```

The ability to **decide what to do next based on what happened previously** is a major part of agentic behavior.

---

# 11. Fixed workflow vs Agent loop

This distinction is extremely important for production systems.

### Fixed workflow

You know the steps beforehand:

```text
Input
 ↓
Retrieve documents
 ↓
Generate answer
 ↓
Validate
 ↓
Return
```

You don't need an agent.

---

### Agent

The next step depends on the current situation:

```text
Input
 ↓
Agent
 ↓
What should I do?
 ├── Search?
 ├── Database?
 ├── API?
 ├── Ask user?
 └── Finish?
```

The agent dynamically chooses.

---

# 12. Don't make every system an agent

This is a very important production lesson.

A loop introduces:

* More latency
* More LLM calls
* More token usage
* More complexity
* More failure possibilities
* Harder debugging
* Potentially unpredictable behavior

So if the task can be solved with:

```text
Input
 ↓
LLM
 ↓
Output
```

don't build an agent.

If it can be solved with:

```text
Input
 ↓
Retriever
 ↓
LLM
 ↓
Output
```

don't automatically build an agent.

Use an agent when **dynamic decision-making and iterative actions actually provide value**.

---

# 13. A production example

Imagine an AI support agent:

```text
User:
"My order hasn't arrived and I want a refund."
```

The agent might do:

```text
Iteration 1
    ↓
Identify customer
    ↓
Iteration 2
    ↓
Get order
    ↓
Iteration 3
    ↓
Check delivery status
    ↓
Iteration 4
    ↓
Determine refund eligibility
    ↓
Iteration 5
    ↓
Request refund
    ↓
Iteration 6
    ↓
Verify refund
    ↓
Final response
```

Notice that every iteration produces information needed for the next decision.

That's why the loop exists.

---

# 14. The core formula

Remember this:

```text
Agent = LLM + Tools + State + Loop
```

And the loop is essentially:

```text
while not done:

    observe()

    decide()

    act()

    update_state()
```

Conceptually:

```python
while not state["done"]:

    decision = llm(state)

    result = execute_tool(decision)

    state = update_state(state, result)
```

This is obviously simplified, but it captures the fundamental architecture.

---

# 15. Interview answer

If an interviewer asks:

> **Why do agents need loops?**

A strong answer is:

> **Agents need loops because many real-world tasks are not solvable through a single LLM call. The agent needs to observe the current state, decide on the next action, execute a tool or operation, observe the result, update its state, and continue until the task is complete. The loop enables multi-step execution, dynamic tool selection, retries, error recovery, and verification.**

That's the answer you should remember.

---

## Mental model

```text
              ┌───────────────┐
              │     User      │
              └───────┬───────┘
                      ↓
              ┌───────────────┐
              │      LLM      │
              │ Decide next   │
              │     action    │
              └───────┬───────┘
                      ↓
                   Tool
                      ↓
                  Result
                      ↓
              ┌───────────────┐
              │     State     │
              └───────┬───────┘
                      ↓
                    LLM
                      ↓
                  Continue?
                 /        \
               Yes         No
                │           │
                └─── loop   ↓
                       Final answer
```

### The key idea

**A tool gives an agent the ability to act.
State gives it memory of the current task.
The loop allows it to repeatedly act based on new information.**

Next in your Phase 1 sequence is **ReAct pattern** — this will tie together the LLM's decision, tool/action, observation, and loop into one well-known agent architecture.
