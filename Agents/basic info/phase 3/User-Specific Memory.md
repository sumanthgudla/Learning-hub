# Phase 3 — Topic 8: User-Specific Memory

**User-specific memory** is information an agent stores about a particular user and can reuse across different sessions.

The key idea:

> **Session memory belongs to a conversation. User-specific memory belongs to the user.**

---

## 1. Simple example

### Session 1

```text
User:
I prefer Python examples.

Agent:
Sure.
```

Session ends.

### Session 2

```text
User:
Explain tool calling.
```

The agent retrieves:

```text
User memory:
Preference → Python examples
```

So it responds with a Python example.

The important part is that **Session 2 is a different conversation**, but the agent still knows the preference.

---

# 2. User memory vs session memory

Consider:

```text
User
│
├── Session A
│   ├── "I'm booking a flight"
│   └── "Tomorrow"
│
├── Session B
│   └── "Explain tool calling"
│
└── User Memory
    ├── Prefers Python
    ├── Prefers concise answers
    └── Uses Azure
```

### Session memory

```text
"User is currently booking a flight."
```

### User-specific memory

```text
"User prefers Python."
```

The first is relevant to **one conversation**.

The second can be relevant to **many future conversations**.

---

# 3. What should user-specific memory contain?

Good candidates include:

### Preferences

```text
prefers_python = true
response_style = "concise"
```

### Stable information

```text
primary_language = "English"
technical_background = "software engineer"
```

### Repeated choices

```text
usually_prefers_morning_flights = true
```

### Important past decisions

```text
preferred_database = "PostgreSQL"
```

The key is **usefulness across future interactions**.

---

# 4. Don't store everything

This is a very important production principle.

Suppose the user says:

```text
What is 15 * 20?
```

You probably don't want:

```text
Memory:
User asked what 15 * 20 is.
```

But if the user says:

```text
From now on, use Python examples when explaining programming.
```

That's potentially useful as persistent memory.

So an agent may have a process like:

```text
Conversation
     ↓
Memory extraction
     ↓
Is this useful later?
     │
   ┌─┴─┐
  Yes  No
   │    │
   ▼    ▼
 Store  Ignore
```

---

# 5. User-specific memory architecture

A basic architecture:

```text
                    User Request
                         │
                         ▼
                       Agent
                         │
            ┌────────────┴────────────┐
            │                         │
            ▼                         ▼
     Session Memory             User Memory
       thread_id                  user_id
            │                         │
            ▼                         ▼
      Current state            Persistent facts
```

Before generating a response, the system can retrieve relevant user memories:

```text
User request
     ↓
Retrieve user memories
     ↓
Relevant memories
     ↓
LLM
     ↓
Response
```

---

# 6. Where is user memory stored?

There are several possibilities.

### Relational database

For structured information:

```text
user_id | preference       | value
--------|------------------|--------
123     | response_style   | concise
123     | code_language    | python
```

This is useful when you know exactly what you're storing.

---

### Document database

You could store:

```json
{
    "user_id": "123",
    "preferences": {
        "language": "python",
        "style": "concise"
    }
}
```

---

### Vector database

Useful when memories are more free-form:

```text
User memory:
"The user prefers Python examples and generally wants
simple explanations rather than highly theoretical ones."
```

You can embed this memory and retrieve it semantically.

```text
Current request
      ↓
Embedding
      ↓
Vector search
      ↓
Relevant user memories
```

---

# 7. Structured vs semantic memory

This is a useful design decision.

Suppose you know:

```text
User prefers Python.
```

Structured storage is often better:

```python
{
    "user_id": "123",
    "preferred_language": "python"
}
```

You don't need vector search for something this simple.

But suppose the memory is:

```text
The user generally prefers practical explanations
with Python examples and dislikes overly theoretical answers.
```

Semantic retrieval could be useful.

So:

> **Use structured storage when the memory has a well-defined schema. Use semantic retrieval when the memory is unstructured and needs similarity-based retrieval.**

A production system can use **both**.

---

# 8. Updating memory

User-specific memory shouldn't be immutable.

Suppose initially:

```text
User preference:
Java
```

Later:

```text
User:
I've switched to Python. Use Python from now on.
```

The memory should change:

```text
Before:
preferred_language = Java

After:
preferred_language = Python
```

So memory needs operations such as:

```text
CREATE
READ
UPDATE
DELETE
```

You can think of this as **CRUD for memory**.

---

# 9. Memory retrieval

You don't necessarily want to send every memory to the LLM.

Suppose a user has:

```text
1000 stored memories
```

Current question:

```text
Explain LangGraph state.
```

You don't want:

```text
1000 memories
     ↓
     LLM
```

Instead:

```text
1000 memories
     ↓
Retriever
     ↓
Relevant memories
     ↓
LLM
```

For example:

```text
Retrieved:
- User is learning LangGraph.
- User prefers Python examples.
```

Those are relevant.

---

# 10. User ID is critical

User-specific memory needs a reliable identifier.

For example:

```text
user_id = 12345
```

Storage:

```text
user_12345
   ↓
memories
```

When the user makes a request:

```text
Authenticated User
       ↓
    user_id
       ↓
Retrieve memories
       ↓
Agent
```

This also provides an important security boundary.

You must prevent:

```text
User A
   ↓
access
   ↓
User B's memory
```

That would be a serious data isolation problem.

---

# 11. Session memory + user memory together

This is what a real personalized agent might do.

Suppose:

```text
User ID:
123

Session ID:
abc
```

The request arrives:

```text
Explain RAG.
```

The system retrieves:

### Session memory

```text
Current conversation:
User is currently learning AI agents.
```

### User memory

```text
Prefers Python examples.
Prefers simple explanations.
```

Then:

```text
                  User Request
                       │
          ┌────────────┴────────────┐
          ▼                         ▼
   Session Memory              User Memory
          │                         │
          └────────────┬────────────┘
                       ▼
                  Context
                       │
                       ▼
                      LLM
                       │
                       ▼
                   Response
```

This creates personalization without requiring the user to repeat everything.

---

# 12. Memory extraction

A more advanced architecture has a dedicated memory step.

```text
User message
     ↓
Agent
     ↓
Response
     ↓
Memory extraction
     ↓
Important information?
     │
   ┌─┴─┐
  Yes  No
   │    │
   ▼    ▼
Update  Ignore
memory
```

For example:

```text
User:
I have switched from Java to Python.
Please use Python in future examples.
```

Memory extraction:

```text
{
    "type": "preference",
    "key": "programming_language",
    "value": "Python"
}
```

Then persist it.

---

# 13. Memory can become stale

This is another production problem.

Suppose memory says:

```text
User works with Java.
```

But six months later:

```text
User now works with Python.
```

If you never update memory, the agent keeps using outdated information.

Therefore, a good memory system needs:

```text
Memory
  ↓
Validate / update
  ↓
Replace old information
```

Some memories may also have:

* Timestamp
* Confidence
* Source
* Expiration
* Last-used time

For example:

```python
{
    "user_id": "123",
    "memory": "Prefers Python examples",
    "created_at": "...",
    "updated_at": "...",
    "confidence": 0.95
}
```

---

# 14. Memory deletion is also important

A production system should support:

```text
Create memory
Read memory
Update memory
Delete memory
```

For example, a user may say:

> Forget that I prefer Java.

The system should be able to locate and remove/update that memory.

This is important both technically and from a privacy perspective.

---

# 15. Interview question

### "How would you design user-specific memory for an AI agent?"

A strong answer:

> I would separate user-level memory from session state. Session state would contain the current conversation and temporary execution information, while user memory would contain persistent facts and preferences associated with the authenticated user ID. I would store structured memories in a relational or document database and use semantic retrieval, potentially with a vector database, for unstructured memories. On each request, I would retrieve only relevant memories and provide them to the agent. After the interaction, a memory extraction process could create or update useful memories, while also supporting deletion and handling stale information.

---

# 16. Complete Phase 3 picture

You have now covered the major memory concepts:

```text
                 AGENT MEMORY & STATE
                         │
          ┌──────────────┴──────────────┐
          │                             │
    Short-Term Memory             Long-Term Memory
          │                             │
          ▼                             ▼
 Conversation History            User-Specific Memory
          │                             │
          ▼                             ▼
     Agent State                 Persistent Storage
          │
          ▼
 State Persistence
          │
          ▼
    Checkpoints
          │
          ▼
 Session / Thread ID
```

### Remember these definitions

| Concept                  | Meaning                                                  |
| ------------------------ | -------------------------------------------------------- |
| **Short-term memory**    | Temporary context for the current interaction            |
| **Conversation history** | Previous user/assistant/tool messages                    |
| **Agent state**          | Everything the agent currently needs to execute          |
| **State persistence**    | Saving agent state durably                               |
| **Checkpoint**           | Snapshot of state at a specific execution point          |
| **Session memory**       | State/history associated with one conversation           |
| **Long-term memory**     | Information retained across sessions                     |
| **User-specific memory** | Persistent information associated with a particular user |

### The most important distinction

```text
Session ID / Thread ID
        ↓
"What is happening in this conversation?"

User ID
        ↓
"What should I remember about this user?"
```

That completes the core **Phase 3 — Agent Memory & State** topics.

The next major phase after this would typically be **Agent Planning & Reasoning**, where we move from *"what does the agent remember?"* to *"how does the agent decide what to do?"*.
