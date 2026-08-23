# Phase 3 — Topic 4: Agent State

**Agent state** is the data that represents **everything the agent currently needs to know to continue its workflow**.

A simple way to think about it:

> **State = the agent's current working situation.**

This is especially important in **LangGraph**, where the state is passed between nodes.

---

## 1. Simple example

Suppose we build a travel agent.

User says:

> Book me a flight from Hyderabad to Delhi tomorrow.

The agent might maintain:

```python
state = {
    "messages": [...],
    "origin": "Hyderabad",
    "destination": "Delhi",
    "date": "2026-08-17",
    "selected_flight": None,
    "booking_status": "not_booked"
}
```

This is the **agent state**.

As the agent works, the state changes.

---

## 2. State changes during the agent loop

Imagine:

```text
User request
     ↓
Agent State
     ↓
LLM decides
     ↓
Search Flights
     ↓
Update State
     ↓
Book Flight
     ↓
Update State
     ↓
Final Response
```

Initially:

```python
{
    "origin": "Hyderabad",
    "destination": "Delhi",
    "date": "tomorrow",
    "selected_flight": None
}
```

After searching:

```python
{
    "origin": "Hyderabad",
    "destination": "Delhi",
    "date": "tomorrow",
    "selected_flight": "AI-502"
}
```

After booking:

```python
{
    "origin": "Hyderabad",
    "destination": "Delhi",
    "date": "tomorrow",
    "selected_flight": "AI-502",
    "booking_status": "confirmed"
}
```

So state is **dynamic**.

---

# 3. State vs conversation history

This is an important distinction.

Conversation history might be:

```python
messages = [
    "Book a flight from Hyderabad to Delhi",
    "Tomorrow",
    "Choose the cheapest one"
]
```

But state could be:

```python
state = {
    "messages": [...],
    "origin": "Hyderabad",
    "destination": "Delhi",
    "date": "2026-08-17",
    "selected_flight": "AI-502",
    "booking_status": "confirmed"
}
```

Therefore:

> **Conversation history is usually one part of agent state.**

Think:

```text
Agent State
│
├── messages
├── user information
├── current task
├── tool results
├── intermediate values
├── selected options
├── status
└── retry information
```

---

# 4. State vs memory

This distinction is even more important.

### Agent state

Represents:

> **What is happening right now?**

Example:

```python
{
    "current_task": "book_flight",
    "selected_flight": "AI-502",
    "booking_status": "pending"
}
```

### Long-term memory

Represents:

> **What should the agent remember for future interactions?**

Example:

```text
User prefers aisle seats.
User usually prefers morning flights.
```

So:

```text
                Agent
                  │
        ┌─────────┴─────────┐
        │                   │
      State               Memory
        │                   │
    Current task       Persistent info
    Tool results       User preferences
    Messages           Past experiences
    Status             Long-term facts
```

---

# 5. State in LangGraph

This is where the concept becomes very practical.

You can define a state schema:

```python
from typing import TypedDict

class AgentState(TypedDict):
    messages: list
    task: str
    result: str
```

Then nodes operate on that state.

For example:

```python
def agent_node(state: AgentState):
    # read state
    messages = state["messages"]

    # call LLM
    response = llm.invoke(messages)

    return {
        "messages": [response]
    }
```

Another node:

```python
def tool_node(state: AgentState):
    # read state
    ...
    
    return {
        "result": "Tool result"
    }
```

Conceptually:

```text
             State
               │
               ▼
          Agent Node
               │
          updated State
               │
               ▼
           Tool Node
               │
          updated State
               │
               ▼
          Agent Node
```

The state travels through the graph.

---

# 6. Why does an agent need state?

Without state, each step would be isolated.

Imagine:

```text
Node 1:
Find customer

        ↓

Node 2:
???
```

Node 2 wouldn't know what Node 1 discovered.

With state:

```text
Node 1
  ↓
state.customer_id = 123
  ↓
Node 2
  ↓
uses customer_id = 123
```

So state allows different parts of the agent workflow to **share information**.

---

# 7. State is not necessarily just data

State can contain different kinds of information:

```python
state = {
    "messages": [...],
    "user_id": "123",
    "current_step": "search_flights",
    "search_results": [...],
    "selected_item": None,
    "retry_count": 2,
    "error": None
}
```

This allows the agent to know:

* What has happened?
* What is happening now?
* What should happen next?
* What information has already been obtained?
* Did something fail?

---

# 8. State enables agent loops

Remember the agent loop you learned earlier:

```text
Observe
   ↓
Reason
   ↓
Act
   ↓
Observe result
   ↓
Repeat
```

State is what carries information between these iterations.

For example:

```text
Iteration 1
───────────
State:
task = "find flight"
results = []

       ↓

Tool call

       ↓

Iteration 2
───────────
State:
task = "find flight"
results = [flight1, flight2, flight3]

       ↓

LLM chooses flight

       ↓

Iteration 3
───────────
State:
task = "find flight"
results = [...]
selected = flight2
```

---

# 9. State can contain intermediate results

This is particularly useful in complex agents.

For example, a research agent:

```python
state = {
    "query": "Compare Azure and AWS",
    "search_results": [],
    "sources": [],
    "analysis": "",
    "final_answer": ""
}
```

Workflow:

```text
Search
  ↓
search_results
  ↓
Analyze
  ↓
analysis
  ↓
Generate answer
  ↓
final_answer
```

All nodes communicate through state.

---

# 10. The key relationship

You should now understand these three concepts:

```text
Short-term memory
        │
        ▼
Conversation history
        │
        ▼
     Agent State
```

But more precisely:

```text
Agent State
│
├── Conversation history
├── Current task
├── Tool results
├── Intermediate results
├── Status
└── Other temporary data
```

And separately:

```text
Long-term Memory
│
├── User preferences
├── Persistent facts
├── Past experiences
└── Past decisions
```

---

## Interview answer

If asked:

> **What is agent state?**

You can say:

> Agent state is the structured representation of the agent's current execution context. It can contain conversation messages, tool results, intermediate values, task information, status, and other data required by different steps of the workflow. In frameworks like LangGraph, nodes read from and update this shared state as the agent progresses through its workflow.

---

### Next topic: **State Persistence**

Now we move from:

**"What is the current state?"**

to:

**"What happens if the application crashes or the user comes back later?"**

That's where **state persistence and checkpoints** become important.
