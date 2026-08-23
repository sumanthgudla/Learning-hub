# Phase 3 — Topic 6: Checkpoints

A **checkpoint** is a **saved snapshot of an agent's state at a particular point in its execution**.

The easiest way to remember it:

> **Checkpoint = save point for an agent.**

Think of a video game:

```text
Start
  ↓
Level 1 ✓
  ↓
💾 Checkpoint
  ↓
Level 2 ✓
  ↓
💾 Checkpoint
  ↓
Game crashes
  ↓
Load last checkpoint
  ↓
Continue from Level 2
```

Agents can work similarly.

---

## 1. Why do agents need checkpoints?

Consider a multi-step agent:

```text
User
 ↓
Search documents
 ↓
Analyze documents
 ↓
Call external API
 ↓
Generate report
 ↓
Send report
```

Suppose the API call fails.

Without checkpoints:

```text
Start again
 ↓
Search documents
 ↓
Analyze documents
 ↓
Call API again
```

That can be expensive and slow.

With checkpoints:

```text
Search ✓
 ↓
💾 Checkpoint
 ↓
Analyze ✓
 ↓
💾 Checkpoint
 ↓
API ❌
```

You can recover from the most recent valid checkpoint.

---

# 2. What does a checkpoint contain?

A checkpoint can contain the agent's state at that moment.

For example:

```python
state = {
    "messages": [...],
    "task": "research",
    "documents": [...],
    "analysis": "...",
    "api_result": None
}
```

A checkpoint might save:

```text
Checkpoint #1
────────────────────
Task: research
Documents: [doc1, doc2, doc3]
Analysis: completed
API result: None
Current step: call_api
```

Later:

```text
Checkpoint #2
────────────────────
Task: research
Documents: [doc1, doc2, doc3]
Analysis: completed
API result: {...}
Current step: generate_report
```

Each checkpoint represents a different point in the workflow.

---

# 3. Checkpoint vs state

This distinction is important.

### State

The **current state**:

```text
Current State
─────────────
Step: 3
Status: running
Result: ...
```

### Checkpoint

A **saved version of state**:

```text
Checkpoint
──────────
Step: 3
Status: running
Result: ...
Timestamp: ...
```

So:

> **State is what exists now. A checkpoint is a persisted snapshot of that state.**

---

# 4. Multiple checkpoints

An agent may create multiple checkpoints:

```text
             Agent Execution

Start
  │
  ▼
State 1
  │
  ▼
💾 Checkpoint 1
  │
  ▼
State 2
  │
  ▼
💾 Checkpoint 2
  │
  ▼
State 3
  │
  ▼
💾 Checkpoint 3
  │
  ▼
State 4
```

If something goes wrong at State 4:

```text
State 4 ❌
   ↓
Load Checkpoint 3
   ↓
Continue
```

---

# 5. Checkpoints in LangGraph

This is especially important for your agent learning.

LangGraph uses a **checkpointer** to persist graph state.

Conceptually:

```text
             LangGraph
                 │
                 ▼
               State
                 │
                 ▼
            Checkpointer
                 │
                 ▼
             Storage
```

The checkpointer is responsible for saving and retrieving checkpoints.

You can think of it as:

```text
Graph
 ↓
"Save my current state."
 ↓
Checkpointer
 ↓
Database
```

Then later:

```text
Graph
 ↓
"I need to resume."
 ↓
Checkpointer
 ↓
Load checkpoint
 ↓
Restore state
```

---

# 6. Thread ID / session ID

How does the system know **which checkpoint belongs to which conversation?**

Usually, you provide an identifier such as:

```text
thread_id
```

For example:

```text
thread_id = "user-123-session-456"
```

The persistence layer can then organize checkpoints:

```text
Thread A
 ├── Checkpoint 1
 ├── Checkpoint 2
 └── Checkpoint 3

Thread B
 ├── Checkpoint 1
 └── Checkpoint 2
```

When Thread A continues:

```text
thread_id = "user-123-session-456"
```

the agent can retrieve the appropriate state/checkpoint.

---

# 7. Checkpoints enable pause and resume

This is one of the most useful capabilities.

Imagine:

```text
Agent
 ↓
Prepare payment
 ↓
⏸ Human approval required
```

The agent saves:

```text
💾 Checkpoint
```

Then the application can safely stop execution.

Later:

```text
Human:
Approved
```

The agent loads the checkpoint:

```text
Checkpoint
    ↓
Restore state
    ↓
Continue
    ↓
Make payment
```

This is extremely useful for **human-in-the-loop agents**.

---

# 8. Checkpoints and failures

Suppose an agent has:

```text
Step 1 → Search ✓
Step 2 → Analyze ✓
Step 3 → API call ✓
Step 4 → Database update ❌
```

Checkpoint after Step 3:

```text
💾 Checkpoint 3
```

The system can potentially recover:

```text
Load Checkpoint 3
      ↓
Retry Step 4
```

instead of:

```text
Start from Step 1
```

This is one reason checkpoints are useful in production.

---

# 9. Checkpoint ≠ long-term memory

Don't mix these concepts.

### Checkpoint

```text
"Where was my agent in its workflow?"
```

Example:

```text
Current task:
Process refund

Order:
12345

Step:
Waiting for payment confirmation
```

### Long-term memory

```text
"What should the agent remember about the user?"
```

Example:

```text
User prefers email notifications.
```

So:

```text
Checkpoint
    ↓
Resume execution

Long-term memory
    ↓
Remember information
```

---

# 10. Checkpoint ≠ conversation history

Conversation history is mostly:

```text
User → ...
AI → ...
User → ...
Tool → ...
```

A checkpoint can contain much more:

```python
{
    "messages": [...],
    "current_step": "payment",
    "order_id": "12345",
    "payment_status": "pending",
    "retry_count": 1,
    "tool_results": [...]
}
```

Therefore:

> **Conversation history can be part of a checkpoint, but a checkpoint represents the broader agent state.**

---

# 11. A complete picture

Now connect everything you've learned:

```text
                    AGENT
                      │
                      ▼
                   STATE
                      │
          ┌───────────┴───────────┐
          │                       │
 Conversation History        Other State
          │                       │
          │                Tool results
          │                Current task
          │                Intermediate data
          │                Status
          │
          └───────────┬───────────┘
                      │
                      ▼
                 CHECKPOINT
                      │
                      ▼
                Persistent Store
```

Separately:

```text
              LONG-TERM MEMORY
                     │
                     ▼
             Persistent Store
                     │
                     ▼
        User preferences / facts
        Past experiences / decisions
```

---

# 12. Interview answer

If an interviewer asks:

> **What is a checkpoint in an agent system?**

You can answer:

> A checkpoint is a persisted snapshot of an agent's state at a particular point in its execution. It allows the system to recover or resume a workflow after failures, pauses, or human approval. In frameworks such as LangGraph, a checkpointer persists graph state and associates it with a thread or conversation identifier so that the state can later be restored.

That's a strong production-level answer.

---

## One-line mental model

Remember these four:

```text
Short-term memory
→ What happened in this conversation?

Agent state
→ What does the agent currently know?

Checkpoint
→ Where did the agent save its progress?

Long-term memory
→ What should the agent remember across conversations?
```

### Next topic: **Session-Based Memory**

We'll connect `session_id/thread_id` with short-term memory and see how a real application keeps **User A's conversation separate from User B's**, including a practical architecture.
