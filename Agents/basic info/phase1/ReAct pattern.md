# Phase 1 — Agent Fundamentals

## Topic 9: ReAct Pattern

Now we're at a very important agent concept.

You've already learned:

* LLM
* RAG
* Tools
* Tool calling
* Structured outputs
* Agent state
* Agent loops

**ReAct connects these concepts together.**

---

# 1. What is ReAct?

**ReAct = Reason + Act**

The basic idea is:

> The LLM alternates between deciding what to do and taking actions, then uses the results of those actions to decide what to do next.

Conceptually:

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
...
```

This is why ReAct is closely related to the agent loop you just learned.

---

# 2. Simple example

User asks:

> "What is the current weather in Hyderabad?"

The agent doesn't know the current weather from its training data.

It can use a weather tool.

Conceptually:

```text
User
 ↓
LLM
 ↓
Reason: I need current weather
 ↓
Act: call weather tool
 ↓
Observation: 29°C, cloudy
 ↓
LLM
 ↓
Reason: I now have the answer
 ↓
Final answer
```

So:

```text
Reason → Act → Observe → Reason → ...
```

That's ReAct.

---

# 3. Why was ReAct introduced?

A traditional LLM works like:

```text
Question
   ↓
LLM
   ↓
Answer
```

The problem is that the model may need **external information or actions**.

For example:

> "What is the current balance of my bank account?"

The LLM cannot know this from its parameters.

It needs:

```text
LLM
 ↓
Bank API
 ↓
Account balance
 ↓
LLM
```

ReAct provides a conceptual framework for this kind of behavior.

---

# 4. ReAct example with multiple tools

Suppose you have:

```python
search_web()
calculator()
```

User asks:

> "What is the population of India divided by the population of Japan?"

The agent might do:

```text
Reason
"I need India's population."

Act
search_web("India population")

Observe
"~1.4 billion"
```

Then:

```text
Reason
"I need Japan's population."

Act
search_web("Japan population")

Observe
"~124 million"
```

Then:

```text
Reason
"I need to calculate the ratio."

Act
calculator(1.4 billion / 124 million)

Observe
"~11.3"
```

Then:

```text
Final answer
"India's population is approximately 11.3 times Japan's."
```

The important thing is that the **next action depends on the previous observation**.

---

# 5. ReAct vs Agent Loop

You might be thinking:

> "Isn't this exactly the agent loop?"

Yes.

There is significant overlap.

The agent loop is the **general architecture**:

```text
Observe
 ↓
Decide
 ↓
Act
 ↓
Observe
 ↓
...
```

ReAct is a **specific reasoning-and-action pattern**:

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
```

So you can think:

> **ReAct is one pattern for implementing an agent loop.**

---

# 6. Classic ReAct

The original ReAct research popularized an interaction pattern often represented as:

```text
Thought
Action
Observation
Thought
Action
Observation
...
```

For example:

```text
Thought:
I need to find the capital of France.

Action:
search("capital of France")

Observation:
Paris

Thought:
I now have the answer.

Final:
The capital of France is Paris.
```

You'll often see this represented as:

```text
Thought → Action → Observation
```

---

# 7. Important modern distinction

As an AI Engineer, you should be careful about saying:

> "ReAct means the LLM prints its chain of thought."

That's not the important part.

The important architectural concept is:

```text
LLM decision
      ↓
Tool/action
      ↓
Tool result
      ↓
LLM decision
```

Modern agent frameworks don't necessarily expose the model's private reasoning to the user.

For example, instead of displaying:

```text
Thought:
I should search the database...
```

the application may simply produce a tool call:

```json
{
    "tool": "search_customer",
    "arguments": {
        "customer_id": "123"
    }
}
```

Then the tool returns:

```json
{
    "name": "Rahul",
    "status": "active"
}
```

The model gets that result and continues.

---

# 8. ReAct with tools

Let's connect it to tool calling.

Suppose you define:

```python
def get_order_status(order_id: str):
    ...
```

The ReAct-style flow becomes:

```text
User
 ↓
LLM
 ↓
Decide:
"I need order status"
 ↓
Tool call
 ↓
get_order_status("123")
 ↓
Tool result
 ↓
LLM
 ↓
Decide:
"Order is delayed"
 ↓
Final response
```

Notice how tool calling is the **Act** part.

---

# 9. ReAct + State

Now connect this with the previous topic.

The state might contain:

```python
state = {
    "messages": [],
    "tool_results": [],
    "current_step": None
}
```

After an action:

```text
Action:
get_order_status(123)
```

the result gets added to state:

```python
state = {
    "messages": [...],
    "tool_results": [
        {
            "order_id": "123",
            "status": "delayed"
        }
    ],
    "current_step": "check_refund"
}
```

The next LLM call uses that state.

So:

```text
ReAct
  +
State
  +
Tools
  ↓
Agent
```

---

# 10. ReAct in LangGraph

This should look familiar to you.

A simplified LangGraph could look like:

```text
              ┌───────────┐
              │   Agent   │
              └─────┬─────┘
                    │
             tool needed?
              /           \
            Yes            No
             ↓              ↓
        ┌─────────┐      Final
        │  Tools  │
        └────┬────┘
             │
             ↓
       Tool result
             │
             └──────────────┐
                            ↓
                         Agent
```

This is essentially a ReAct-style agent.

The agent:

1. Receives state
2. Decides whether a tool is needed
3. Calls the tool
4. Receives the result
5. Updates state
6. Goes back to the agent
7. Decides again
8. Eventually finishes

---

# 11. ReAct vs RAG

This is a common interview question.

### RAG

Usually:

```text
Question
 ↓
Retriever
 ↓
Documents
 ↓
LLM
 ↓
Answer
```

The retrieval process is generally predefined.

### ReAct

The LLM can decide what action to take:

```text
Question
 ↓
LLM
 ↓
Should I search?
 ↓
Search
 ↓
Result
 ↓
LLM
 ↓
Should I search again?
 ↓
Another search
 ↓
...
```

So the key difference is **dynamic decision-making**.

---

# 12. ReAct vs fixed workflow

Suppose you have:

```text
Step 1 → Search
Step 2 → Summarize
Step 3 → Validate
```

This is a fixed workflow.

You don't necessarily need an agent.

But suppose:

```text
Search
 ↓
Result
 ↓
LLM decides:
  ├── Search again
  ├── Use calculator
  ├── Query database
  ├── Ask user
  └── Finish
```

Now an agent/ReAct-style approach makes more sense.

---

# 13. Advantages of ReAct

### 1. Tool usage

The model can interact with external systems.

### 2. Dynamic execution

The next action depends on the previous result.

### 3. Multi-step tasks

It can solve tasks requiring several operations.

### 4. Error recovery

It can observe errors and potentially try another action.

### 5. Verification

It can perform an action and then check the result.

---

# 14. Problems with ReAct

ReAct isn't magic.

It introduces several challenges.

### More LLM calls

```text
LLM → Tool → LLM → Tool → LLM
```

means higher latency and cost.

### Wrong tool selection

The model may choose the wrong tool.

### Infinite loops

A poorly designed agent could keep doing:

```text
Search
 ↓
Search
 ↓
Search
 ↓
Search
 ↓
...
```

So production agents need limits.

For example:

```python
MAX_ITERATIONS = 10
```

### Incorrect arguments

The LLM might call:

```python
get_customer(customer_id="ABC")
```

when the tool expects an integer.

Structured tool schemas and validation help here.

---

# 15. Production ReAct needs guardrails

A production agent shouldn't simply be:

```text
while True:
    LLM()
```

You need controls such as:

```text
Maximum iterations
Maximum tool calls
Timeouts
Tool validation
Permission checks
Error handling
Human approval
Cost limits
```

For example:

```text
Agent
 ↓
Decision
 ↓
Check:
  Is this tool allowed?
  Are arguments valid?
  Have we exceeded limits?
 ↓
Tool
```

This is especially important when tools can perform destructive operations.

---

# 16. Interview answer

If asked:

> **What is the ReAct pattern?**

A strong answer:

> **ReAct stands for Reasoning and Acting. It is an agent pattern where an LLM alternates between deciding what action to take, invoking a tool or performing an action, observing the result, and then using that result to determine the next step. This allows agents to dynamically perform multi-step tasks instead of generating a single response.**

If they ask:

> **How does ReAct relate to tool calling?**

Say:

> **Tool calling provides the mechanism for the action part of ReAct. The LLM decides which tool to call and with what arguments, receives the tool result, and then continues the loop.**

---

# 17. Your complete Phase 1 picture so far

You can now connect everything:

```text
                    AGENT
                      │
                      ↓
                    State
                      │
                      ↓
                     LLM
                      │
               Decide next action
                      │
              ┌───────┴────────┐
              ↓                ↓
          Tool call          Finish
              │                │
              ↓                ↓
          Tool result       Final answer
              │
              ↓
        Update State
              │
              ↓
             LLM
              │
              └──────→ Loop
```

And the conceptual pattern is:

```text
        ┌─────────┐
        │ Reason  │
        └────┬────┘
             ↓
        ┌─────────┐
        │  Act    │
        └────┬────┘
             ↓
        ┌─────────┐
        │ Observe │
        └────┬────┘
             ↓
           Repeat
```

### The key takeaway

**ReAct is not a separate magical type of LLM. It is an agent execution pattern that combines model decisions, actions/tool calls, observations, state, and iteration.**

The **final topic in Phase 1** is:

### **When NOT to use an Agent**

This is actually very important for interviews because a good AI engineer should not answer every problem with *"Let's build an agent."*
