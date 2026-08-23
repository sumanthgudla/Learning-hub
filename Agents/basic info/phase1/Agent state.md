# Phase 1 — Agent Fundamentals

## Topic 7: Agent State

You already understand that an agent works in a loop:

```text
Observe → Reason → Act → Observe → ...
```

Now the important question is:

> **What does the agent remember between these steps?**

That is **agent state**.

---

## 1. What is Agent State?

**Agent state is the information maintained by the agent while it is executing a task.**

Think of it as the agent's **working memory**.

For example, suppose the user says:

> "Find the best laptop under ₹80,000 and compare it with the MacBook Air."

The agent may need to remember:

```text
state = {
    user_request,
    search_results,
    selected_products,
    comparison_data,
    current_step,
    tool_results
}
```

The state changes as the agent progresses.

---

# 2. Why does an agent need state?

Consider this:

```text
User
 ↓
LLM
 ↓
Search tool
 ↓
Search results
```

The LLM now needs to use those search results.

If the agent doesn't maintain them, the next step doesn't know what happened.

So:

```text
Step 1:
Search for laptops

        ↓

State:
{
    search_results: [...]
}

        ↓

Step 2:
Compare the laptops

        ↓

State:
{
    search_results: [...],
    comparison: {...}
}
```

The state carries information from one step to the next.

---

# 3. Simple example

Imagine an agent solving:

> "What's the weather in Hyderabad and should I carry an umbrella?"

The process might be:

### Step 1

```text
User request:
What's the weather in Hyderabad?
```

State:

```python
{
    "user_request": "What's the weather in Hyderabad?",
    "city": "Hyderabad"
}
```

### Step 2

Agent calls:

```python
get_weather("Hyderabad")
```

Tool returns:

```text
Rainy, 24°C
```

State becomes:

```python
{
    "user_request": "What's the weather in Hyderabad?",
    "city": "Hyderabad",
    "weather": "Rainy, 24°C"
}
```

### Step 3

LLM sees the state and decides:

```text
It is raining → recommend carrying an umbrella.
```

Final answer:

```text
It's rainy in Hyderabad, so you should carry an umbrella.
```

---

# 4. State is not the same as memory

This distinction is important.

### Agent state

Usually represents the **current execution/task**.

```text
Current task
     ↓
Agent state
     ↓
Task completed
```

### Long-term memory

Information retained across conversations/tasks.

```text
Conversation 1
      ↓
Memory
      ↓
Conversation 2
```

For example:

```text
State:
"Current order ID = 123"

Memory:
"User prefers vegetarian restaurants"
```

The order ID is probably temporary state.

The restaurant preference might be long-term memory.

---

# 5. What can be stored in state?

Almost anything the agent needs.

Common examples:

### User input

```python
state["user_query"]
```

### Conversation messages

```python
state["messages"]
```

### Tool results

```python
state["tool_results"]
```

### Current task

```python
state["task"]
```

### Current step

```python
state["current_step"]
```

### Intermediate results

```python
state["search_results"]
```

### Agent decision

```python
state["next_action"]
```

### Errors

```python
state["error"]
```

---

# 6. Agent State in LangGraph

This is where your previous LangGraph learning connects directly.

In LangGraph, you typically define a state:

```python
from typing import TypedDict


class AgentState(TypedDict):
    messages: list
    current_step: str
    tool_result: str
```

Then nodes operate on that state.

For example:

```text
              ┌──────────────┐
              │    Agent     │
              └──────┬───────┘
                     │
                     ↓
                Tool call
                     │
                     ↓
              ┌──────────────┐
              │ Tool Result  │
              └──────┬───────┘
                     │
                     ↓
                Agent again
```

The state flows through these nodes.

---

# 7. State is the shared context of the workflow

Think about a LangGraph like this:

```text
                 STATE
                   │
        ┌──────────┼──────────┐
        ↓          ↓          ↓
      Agent      Search      Tool
        │          │          │
        └──────────┼──────────┘
                   ↓
              Updated State
```

Each node can:

1. Read the state
2. Perform some work
3. Update the state

For example:

```python
def search_node(state):
    results = search(state["user_query"])

    return {
        "search_results": results
    }
```

The next node can access:

```python
state["search_results"]
```

---

# 8. State enables the Agent Loop

Remember the agent loop:

```text
Observe
   ↓
Reason
   ↓
Act
   ↓
Observe result
   ↓
Reason
   ↓
Act
   ↓
...
```

State is what makes this possible.

For example:

```text
State 1
{
  user_query
}

     ↓ Agent

State 2
{
  user_query,
  selected_tool
}

     ↓ Tool

State 3
{
  user_query,
  selected_tool,
  tool_result
}

     ↓ Agent

State 4
{
  user_query,
  selected_tool,
  tool_result,
  final_answer
}
```

Without state, the agent wouldn't have a reliable way to carry intermediate information through the loop.

---

# 9. State vs Context

You will hear both terms in AI engineering.

They are related but not exactly identical.

### Context

Information provided to the LLM for a particular invocation.

```text
System prompt
+
Conversation
+
Retrieved documents
+
Tool results
```

### State

The broader information maintained by the agent/workflow.

```text
State
├── messages
├── tool results
├── task information
├── intermediate results
├── current step
└── metadata
```

The agent can use state to **construct the context** sent to the LLM.

---

# 10. State in a production agent

Imagine a customer-support agent.

User:

> "My order 123 hasn't arrived."

State might become:

```python
{
    "user_query": "My order 123 hasn't arrived.",
    "order_id": "123",
    "customer_id": "C456",
    "order_status": None,
    "tool_calls": [],
    "messages": [],
    "next_action": None,
    "final_answer": None
}
```

The agent calls:

```text
get_order_status(123)
```

State becomes:

```python
{
    "user_query": "...",
    "order_id": "123",
    "customer_id": "C456",
    "order_status": "Delayed",
    "tool_calls": [
        "get_order_status"
    ],
    "next_action": "contact_shipping",
    "final_answer": None
}
```

Then another tool may be called.

Eventually:

```python
{
    ...
    "order_status": "Delayed",
    "next_action": None,
    "final_answer": "Your order is delayed..."
}
```

That is a real agent workflow.

---

# 11. Why state is extremely important for production agents

In a simple demo:

```text
User → LLM → Answer
```

you don't need much state.

But production agents often have:

```text
User
 ↓
Agent
 ↓
Tool
 ↓
Agent
 ↓
Tool
 ↓
Agent
 ↓
Human approval
 ↓
Tool
 ↓
Agent
 ↓
Final answer
```

Now you need to track:

* What the user asked
* What tools were called
* What tools returned
* What decisions were made
* What step you're currently on
* Whether an error occurred
* Whether human approval is required

That's why **state becomes a fundamental part of agent architecture**.

---

# 12. Interview question

### "What is agent state?"

A good answer:

> **Agent state is the information maintained throughout an agent's execution. It contains things such as user input, conversation messages, tool results, intermediate results, current task information, and execution status. Each agent step can read and update this state, allowing the agent to maintain context across multiple reasoning and tool-calling iterations.**

That's a strong AI Engineer answer.

---

# 13. Simple mental model

Remember this:

```text
                AGENT STATE
                     │
        ┌────────────┼────────────┐
        ↓            ↓            ↓
    User Input    Tool Results   Messages
        │            │            │
        └────────────┼────────────┘
                     ↓
                   Agent
                     ↓
                New Decision
                     ↓
                  Tool
                     ↓
              Updated State
                     ↓
                  Agent
                     ↓
                   ...
```

### Key takeaway

> **State is the agent's working memory during execution.**

And this connects directly to LangGraph:

> **LangGraph is essentially giving you a structured way to build workflows/agents where state flows between nodes and can be updated as the workflow progresses.**

---

### Next topic

**Topic 8 — Why agents need loops**

This is where we'll go deeper into **why a single LLM call isn't enough for an agent**, and how the loop actually enables planning, tool usage, verification, and retrying.
