# Phase 1 — Topic 2: The Agent Loop

Now let's understand the **core mechanism behind an agent**.

If you understand this well, LangGraph will become much easier later.

---

## 1. What is the Agent Loop?

An agent doesn't necessarily make one decision and stop.

It can repeatedly:

```text
Observe → Decide → Act → Observe → Decide → Act → Finish
```

This is the **agent loop**.

### Example

User asks:

> "Find the current weather in Hyderabad and tell me whether I should carry an umbrella."

The agent might do:

```text
User request
     ↓
   Agent
     ↓
Decide: Need weather information
     ↓
Weather Tool
     ↓
Result: 30°C, rain expected
     ↓
Agent observes result
     ↓
Decide: Need to recommend umbrella
     ↓
Final answer
```

---

# 2. The Four Main Steps

### Step 1 — Observe

The agent receives information.

This could be:

* User request
* Tool result
* Database result
* Search result
* Previous agent state

Example:

```text
User:
"Find the price of iPhone 17."
```

The agent observes:

```text
I need current product information.
```

---

### Step 2 — Decide

The LLM determines what should happen next.

For example:

```text
I don't know the current price.
I should search for it.
```

The important part is that the agent chooses an action.

---

### Step 3 — Act

The agent executes the chosen action.

For example:

```python
search_product("iPhone 17")
```

The external system returns:

```text
iPhone 17 → ₹79,999
```

---

### Step 4 — Observe Again

The agent receives the tool result.

Now it can decide:

```text
I have enough information.
I can answer the user.
```

Or:

```text
The search result isn't sufficient.
I need another search.
```

That's what makes it a **loop**.

---

# 3. Simple Agent Loop

Conceptually:

```text
                ┌──────────────┐
                │    User      │
                └──────┬───────┘
                       ↓
                ┌──────────────┐
                │     Agent    │
                └──────┬───────┘
                       ↓
                   Decide
                       ↓
                ┌──────────────┐
                │     Tool     │
                └──────┬───────┘
                       ↓
                  Tool Result
                       ↓
                ┌──────────────┐
                │     Agent    │
                └──────┬───────┘
                       ↓
                 Enough info?
                  /       \
                No         Yes
                ↓           ↓
              Tool       Answer
                ↑
                └───────────
```

---

# 4. Why do we need a loop?

Consider this question:

> "Find the latest information about NVIDIA's new AI chip, compare it with the previous generation, and tell me whether it is faster."

One tool call isn't enough.

The agent might need:

```text
1. Search for new chip
       ↓
2. Search specifications
       ↓
3. Search previous generation
       ↓
4. Compare specifications
       ↓
5. Generate answer
```

A fixed workflow could do this too, but an agent can decide dynamically.

For example:

```text
Search
 ↓
Result is insufficient
 ↓
Search again
 ↓
Now sufficient
 ↓
Compare
 ↓
Answer
```

---

# 5. Agent Loop vs Normal Chain

This distinction is **very important in interviews**.

### Chain

A chain has a predetermined sequence:

```text
Input
 ↓
Step 1
 ↓
Step 2
 ↓
Step 3
 ↓
Output
```

For example:

```text
Question
 ↓
Retriever
 ↓
LLM
 ↓
Answer
```

The flow is predefined.

---

### Agent

The next step can depend on the current state:

```text
Question
 ↓
Agent
 ↓
What should I do?
 ├── Search
 ├── Database
 ├── Calculator
 └── Answer
```

After the tool returns:

```text
Tool result
 ↓
Agent
 ↓
What should I do now?
 ├── Another tool
 └── Finish
```

So:

> **Chain = predefined workflow**

> **Agent = dynamically selected workflow**

---

# 6. ReAct

You'll hear this term frequently in agent interviews.

**ReAct = Reasoning + Acting**

The basic idea is:

```text
Reason
 ↓
Act
 ↓
Observe
 ↓
Reason
 ↓
Act
 ↓
Observe
 ↓
Final answer
```

For example:

```text
Question:
"What is 25 × 17 and what is the weather in Hyderabad?"

Reason:
I need two pieces of information.

Action:
calculator(25 * 17)

Observation:
425

Reason:
I still need weather.

Action:
weather("Hyderabad")

Observation:
30°C, rain

Reason:
I have everything.

Final:
425 and Hyderabad is 30°C with rain expected.
```

The important concept is **iterative decision-making**.

---

# 7. Don't confuse "reasoning" with exposing chain-of-thought

When we talk about an agent "reasoning," we mean the system is making a decision about the next action.

For example:

```text
Need current information → use search tool
```

You don't need to expose or store the model's private chain-of-thought.

In production systems, we generally care about:

```text
Decision
Tool selected
Tool arguments
Tool result
Next decision
```

---

# 8. Let's implement the idea without LangChain

Before using LangGraph, it's useful to understand the underlying mechanism.

Imagine we have:

```python
def calculator(expression):
    return eval(expression)
```

Our conceptual agent could work like:

```python
while True:

    decision = llm(user_input)

    if decision == "calculator":
        result = calculator(expression)

        user_input = result

    elif decision == "finish":
        break
```

This is obviously oversimplified, but notice the important thing:

```text
while True:
    LLM decides
    ↓
    Tool executes
    ↓
    Result goes back to LLM
    ↓
    LLM decides again
```

**That's the heart of an agent.**

LangChain and LangGraph provide abstractions around this idea.

---

# 9. Where State comes in

Soon you'll see:

```text
Agent State
```

The agent needs to keep track of things like:

```python
state = {
    "user_question": "...",
    "messages": [...],
    "tool_results": [...],
    "current_step": "...",
}
```

Then the loop becomes:

```text
State
 ↓
LLM
 ↓
Action
 ↓
Tool
 ↓
Update State
 ↓
LLM
 ↓
Action
 ↓
...
```

This is where **LangGraph becomes extremely useful**.

We'll get to that later.

---

# Interview Question

Suppose you have:

```text
User
 ↓
LLM
 ↓
Search Tool
 ↓
LLM
 ↓
Database Tool
 ↓
LLM
 ↓
Answer
```

Would you call this a **chain or an agent**?

And what would change in the architecture to make it clearly agentic?
