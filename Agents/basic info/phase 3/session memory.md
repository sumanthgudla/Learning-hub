# Phase 3 — Topic 7: Session-Based Memory

**Session-based memory** means maintaining memory for a specific **conversation/session** using a unique identifier such as `session_id`, `conversation_id`, or `thread_id`.

The key idea:

> **A session is a boundary around a particular interaction.**

---

## 1. Why do we need sessions?

Imagine two users are using your AI agent:

```text
User A:
My order number is 12345.

User B:
My order number is 98765.
```

The agent must never mix them up.

You need something like:

```text
User A → session_A
User B → session_B
```

Then:

```text
session_A
    ↓
User A's conversation/state

session_B
    ↓
User B's conversation/state
```

---

# 2. Basic architecture

A simple architecture looks like:

```text
                 User
                   │
                   ▼
              Your API
                   │
             session_id
                   │
                   ▼
             Memory Store
                   │
        ┌──────────┴──────────┐
        ▼                     ▼
   Session A              Session B
        │                     │
   Messages              Messages
   State                  State
```

For example:

```text
session_id = "abc123"
```

might correspond to:

```text
{
    "messages": [
        "My order is 12345",
        "Check its status"
    ]
}
```

While:

```text
session_id = "xyz789"
```

has:

```text
{
    "messages": [
        "My order is 98765",
        "Cancel it"
    ]
}
```

---

# 3. Session memory is usually short-term memory

This is an important distinction.

Suppose:

```text
Session A
─────────
User:
My order number is 12345.

Agent:
Got it.

User:
What's its status?
```

The agent remembers `12345`.

That's **session-based short-term memory**.

When the session ends:

```text
Session A
    ↓
Conversation ends
```

you might eventually expire or delete that session's state.

---

# 4. Session vs user

These are **not necessarily the same thing**.

A user can have multiple sessions:

```text
User 123
│
├── Session A
│   └── Flight booking conversation
│
├── Session B
│   └── Hotel booking conversation
│
└── Session C
    └── General question
```

So:

```text
User
 └── many sessions
```

A session represents a particular interaction, while the user represents the person/account.

---

# 5. Example

Suppose you have an AI shopping assistant.

### Session 1

```text
session_id = "session_001"

User:
I'm looking for running shoes.

Agent:
What size?

User:
Size 10.
```

State:

```python
{
    "session_id": "session_001",
    "category": "running shoes",
    "size": 10
}
```

Now the user starts another conversation.

### Session 2

```text
session_id = "session_002"

User:
I need a laptop.
```

State:

```python
{
    "session_id": "session_002",
    "category": "laptop"
}
```

The agent shouldn't automatically assume the user is still looking for running shoes.

That's the purpose of session boundaries.

---

# 6. Session-based memory with a database

A simplified database table might look like:

```text
sessions
────────────────────────────────────
session_id    user_id    created_at
abc123        user_1     ...
xyz789        user_2     ...
def456        user_1     ...
```

And another table:

```text
messages
────────────────────────────────────
session_id    role       message
abc123        user       Hello
abc123        assistant  Hi!
abc123        user       Check my order
```

Then when a request arrives:

```text
POST /chat

{
    "session_id": "abc123",
    "message": "Check my order"
}
```

Your backend does:

```text
1. Receive session_id
2. Load session state
3. Add new user message
4. Run agent
5. Update state
6. Persist state
7. Return response
```

---

# 7. Session memory in an agent

The flow becomes:

```text
                 User
                   │
                   ▼
             session_id
                   │
                   ▼
          Load session state
                   │
                   ▼
                  LLM
                   │
              ┌────┴────┐
              ▼         ▼
            Tool      Response
              │
              ▼
         Update state
              │
              ▼
        Save session state
```

On the next request:

```text
Same session_id
       ↓
Load previous state
       ↓
Continue conversation
```

---

# 8. Session-based memory in LangGraph

This connects directly with the previous checkpoint topic.

In LangGraph, you can associate graph execution with a **thread identifier**.

Conceptually:

```text
thread_id = "user123-session456"
```

Then:

```text
Request 1
    ↓
LangGraph
    ↓
State
    ↓
Checkpoint
    ↓
thread_id = user123-session456
```

Later:

```text
Request 2
    ↓
same thread_id
    ↓
Load checkpoint/state
    ↓
Continue
```

So the thread ID effectively identifies the conversation/workflow whose state should be loaded.

---

# 9. Session memory vs long-term memory

This is one of the most important comparisons in this phase.

| Session Memory                  | Long-Term Memory                   |
| ------------------------------- | ---------------------------------- |
| Usually session-scoped          | User/application scoped            |
| Current conversation            | Across conversations               |
| Temporary context               | Persistent information             |
| Recent messages/state           | Facts/preferences/past experiences |
| Identified by session/thread ID | Often identified by user ID        |
| May expire                      | Usually persists longer            |

Example:

### Session memory

```text
session_123

User:
I'm booking a flight to Delhi.

Agent:
What date?

User:
Tomorrow.
```

### Long-term memory

```text
user_456

Preference:
User prefers aisle seats.
```

A new session could retrieve the long-term preference.

---

# 10. User can have both

A production agent might use:

```text
                User
                 │
        ┌────────┴────────┐
        │                 │
   Session Memory     Long-Term Memory
        │                 │
   thread_id           user_id
        │                 │
   Current chat       Persistent facts
```

When a request arrives:

```text
User request
     │
     ├──────────────► Load session state
     │
     └──────────────► Retrieve relevant long-term memories
                              │
                              ▼
                             LLM
```

Now the agent has:

```text
Current conversation
        +
Relevant persistent memories
        ↓
       LLM
```

---

# 11. Important production concerns

Session-based memory sounds simple, but production systems need to handle:

### Isolation

User A's state must never be exposed to User B.

```text
❌ session_A → User B
```

### Expiration

Old sessions may need to be deleted after some period.

```text
session created
     ↓
active
     ↓
inactive
     ↓
expired
     ↓
deleted/archived
```

### Concurrency

Two requests may arrive for the same session simultaneously.

```text
Request A ──┐
            ├── session_123
Request B ──┘
```

You need to avoid corrupting or overwriting state.

### Security

Never blindly trust a client-provided session ID.

Your backend should verify that the authenticated user is authorized to access that session.

---

# 12. Interview question

### "How would you implement conversation memory for multiple users?"

A strong answer:

> I would assign each conversation a unique session or thread ID and associate it with the authenticated user. On every request, the backend would load the state associated with that session, process the request, update the state, and persist it. I would also enforce authorization so users can only access their own sessions. For longer-term personalization, I would maintain a separate user-level memory store keyed by the user ID.

---

# 13. Complete picture so far

You now have:

```text
                    AGENT MEMORY
                         │
            ┌────────────┴────────────┐
            │                         │
       Short-Term                  Long-Term
            │                         │
      Session Memory            Persistent Memory
            │                         │
       thread_id                  user_id
            │                         │
      Conversation              Preferences
      Agent state               Past facts
      Tool results              Past experiences
            │
            ▼
       Checkpoints
            │
            ▼
    State Persistence
```

The most important distinction:

> **Session memory tells the agent what is happening in this conversation.**

> **User-specific long-term memory tells the agent what it should remember about the user across conversations.**

### Next topic: **User-Specific Memory**

We'll look at how to design memory specifically around a user, how memories are created/updated/retrieved, and how this differs from simply storing conversation history.
