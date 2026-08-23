# Phase 3 — Topic 3: Long-Term Memory

**Long-term memory** allows an agent to retain useful information **beyond the current conversation/session**.

The simplest distinction:

> **Short-term memory = remember this conversation.**
> **Long-term memory = remember information across conversations.**

---

## 1. Simple example

### Conversation 1 — Today

```text
User:
I prefer Python examples.

Agent:
Sure, I'll use Python examples.
```

The conversation ends.

### Conversation 2 — Next week

```text
User:
Explain tool calling.
```

A long-term memory system can retrieve:

```text
User preference:
Prefers Python examples
```

Then the agent can respond with a Python-based example.

---

# 2. Why do we need long-term memory?

Conversation history only works well within a session.

Imagine:

```text
Session 1
    ↓
User tells agent 20 important facts
    ↓
Session ends
    ↓
Session 2
    ↓
Conversation history is empty
```

Without long-term memory, the agent starts from scratch.

With long-term memory:

```text
Session 1
    ↓
Important information
    ↓
Persistent Memory
    ↓
Session 2
    ↓
Retrieve relevant memories
    ↓
LLM
```

---

# 3. What should we store?

You generally **shouldn't store everything**.

Store information that is useful across future interactions.

For example:

### User preferences

```text
Prefers Python examples
Prefers concise explanations
```

### User information

```text
Works as a software engineer
Learning AI agents
```

### Important facts

```text
Current project uses LangGraph
```

### Past decisions

```text
User chose PostgreSQL for the project
```

---

# 4. Where is long-term memory stored?

Unlike short-term memory, long-term memory normally requires **persistent storage**.

For example:

```text
                    Agent
                      │
                      ▼
              Memory Manager
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
     SQL DB       Vector DB      Document DB
```

Common choices include:

* PostgreSQL
* Redis
* MongoDB
* Vector databases
* Dedicated memory stores

The choice depends on the type of memory.

---

# 5. Two important types

A useful way to think about long-term memory is:

### Semantic memory

Facts about the user/world.

```text
User prefers Python.
User works with LangGraph.
User's project uses PostgreSQL.
```

### Episodic memory

Past experiences/events.

```text
User previously asked about Azure Key Vault.
Agent recommended using Managed Identity.
User decided to use that approach.
```

A simple distinction:

```text
Semantic:
"What do I know about this user?"

Episodic:
"What happened previously?"
```

---

# 6. Long-term memory + vector database

This is where your **RAG knowledge** becomes useful.

Suppose the agent stores:

```text
Memory 1:
User prefers Python examples.

Memory 2:
User is learning LangGraph.

Memory 3:
User uses Azure.

Memory 4:
User prefers simple explanations.
```

These can be embedded:

```text
Memory
   ↓
Embedding Model
   ↓
Vector
   ↓
Vector Database
```

Later:

```text
User:
Explain agent state.
```

The system can search the memory store:

```text
Current query
     ↓
Embedding
     ↓
Vector Search
     ↓
Relevant memories
     ↓
LLM
```

The LLM then gets:

```text
User prefers Python examples.
User is learning LangGraph.
```

and can tailor the answer.

---

# 7. Important: Long-term memory is NOT simply RAG

They are related, but don't confuse them.

### RAG

Usually:

```text
Question
   ↓
Retrieve knowledge
   ↓
LLM
```

The knowledge is generally **external/domain information**.

Example:

```text
Company documentation
Product documentation
Technical manuals
```

### Long-term agent memory

Usually:

```text
Current interaction
       ↓
Memory
       ↓
Persistent storage
```

The information is often about:

```text
User
Past interactions
Preferences
Past decisions
Experiences
```

So:

> **RAG retrieves external knowledge; long-term memory retrieves persistent information relevant to the agent/user.**

In real systems, they can absolutely use the same underlying vector database technology.

---

# 8. Memory lifecycle

A production agent might work like this:

```text
              User message
                   │
                   ▼
              Load memory
                   │
                   ▼
             Relevant memories
                   │
                   ▼
                  LLM
                   │
                   ▼
              Agent response
                   │
                   ▼
        Decide what to remember
                   │
                   ▼
          Save important memory
```

Notice something important:

**The agent doesn't necessarily save every message.**

It might decide:

```text
User:
I prefer Python.

        ↓

Important preference detected

        ↓

Save to long-term memory
```

But:

```text
User:
What's 2 + 2?

        ↓

Probably don't save
```

---

# 9. Long-term memory vs short-term memory

|              | Short-term          | Long-term                |
| ------------ | ------------------- | ------------------------ |
| Lifetime     | Session             | Persistent               |
| Main purpose | Current context     | Future interactions      |
| Example      | Recent messages     | User preferences         |
| Storage      | Agent state/context | DB/memory store          |
| Scope        | Current session     | User/application         |
| Size         | Limited by context  | Much larger              |
| Retrieval    | Usually direct      | Often searched/retrieved |

---

# 10. Interview answer

If asked:

> **How would you implement long-term memory for an AI agent?**

A strong answer:

> I would persist useful user-specific information or past experiences in a durable storage system. When a new request arrives, I would retrieve memories relevant to the current request and inject them into the agent's context. After the interaction, the system can identify important new information and persist it. Depending on the memory type, I could use a relational database, document store, or vector database for semantic retrieval.

---

# 11. One important production problem

Long-term memory introduces a new challenge:

**What should the agent remember?**

If you store everything:

```text
Millions of interactions
        ↓
Huge memory store
        ↓
Lots of irrelevant memories
```

You need:

* Memory extraction
* Memory relevance
* Memory retrieval
* Memory updating
* Memory deletion
* User isolation
* Privacy/security
* Memory expiration when appropriate

These become important in production agent systems.

---

## Mental model

You should now have:

```text
             Agent Memory
                  │
       ┌──────────┴──────────┐
       │                     │
 Short-term              Long-term
       │                     │
 Current session        Persistent
       │                     │
 Conversation           User facts
 history                Preferences
 Tool results           Past experiences
 Agent state            Past decisions
```

And the key difference:

> **Short-term memory helps the agent remember what is happening now. Long-term memory helps the agent remember what happened before.**

### Next topic: **Agent State**

This is particularly important for **LangGraph** and agent interviews. We'll cover what exactly goes inside an agent's state, how it changes during the agent loop, and why **state is different from memory**.
