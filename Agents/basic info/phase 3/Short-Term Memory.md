# Phase 3 — Agent Memory & State

## Topic 1: Short-Term Memory

Short-term memory is **what an agent remembers during the current interaction/session**.

Think of it as the agent's **working memory**.

### 1. Why do agents need short-term memory?

Consider this conversation:

**User:** My name is Sumanth.
**Agent:** Nice to meet you, Sumanth.

Then:

**User:** What is my name?
**Agent:** Your name is Sumanth.

How did the agent know?

Because the previous conversation was provided to the LLM as **conversation history**.

Without that history:

```text
User: What is my name?
        ↓
      LLM
        ↓
"I don't know"
```

With short-term memory:

```text
Conversation
    ↓
Short-term memory
    ↓
LLM
    ↓
Response
```

---

# 2. What is actually stored?

Usually, the agent maintains a sequence of messages:

```text
[
    HumanMessage("My name is Sumanth"),
    AIMessage("Nice to meet you, Sumanth"),
    HumanMessage("What is my name?")
]
```

The LLM receives this information when generating the next response.

So technically, **short-term memory is often conversation history + temporary agent state**.

---

# 3. Simple example

Imagine a customer-support agent.

```text
User:
My order number is 12345.

Agent:
Got it.

User:
Can you check its status?

Agent:
Sure, I'll check order 12345.
```

The second request doesn't contain `12345`.

The agent knows it because the previous interaction is still available.

Conceptually:

```text
User: My order number is 12345
              ↓
       Short-term memory
              ↓
User: Check its status
              ↓
            LLM
              ↓
     remembers order = 12345
```

---

# 4. Short-term memory ≠ LLM memory

This is an important interview point.

**The LLM itself does not permanently remember previous conversations.**

Instead, the application sends previous messages back to the LLM.

For example:

```python
messages = [
    {"role": "user", "content": "My name is Sumanth"},
    {"role": "assistant", "content": "Nice to meet you"},
    {"role": "user", "content": "What is my name?"}
]

response = llm.invoke(messages)
```

The LLM can answer because the application included the previous messages.

So:

> **Short-term memory is primarily an application-level mechanism for maintaining context across turns.**

---

# 5. Short-term memory in an Agent

Now add tools.

Suppose the user says:

```text
User:
What is the weather in Hyderabad?
```

Agent:

```text
User request
    ↓
Agent state
    ↓
LLM
    ↓
Decides: call weather tool
    ↓
Weather tool
    ↓
Tool result
    ↓
Agent state
    ↓
LLM
    ↓
Final answer
```

The temporary state might contain:

```python
{
    "messages": [
        HumanMessage("What is the weather in Hyderabad?"),
        AIMessage(tool_call="get_weather"),
        ToolMessage("32°C, sunny"),
        AIMessage("The weather is 32°C and sunny.")
    ]
}
```

This entire sequence can be considered part of the agent's **short-term context/state**.

---

# 6. Short-term memory has a limitation

The biggest problem is the **context window**.

Suppose the conversation becomes:

```text
Message 1
Message 2
Message 3
...
Message 10,000
```

You cannot keep adding unlimited conversation history to every LLM call.

Eventually:

```text
Context window exceeded
```

or the request becomes expensive and slower.

Therefore, production agents often use techniques such as:

* Trimming old messages
* Summarizing conversation history
* Keeping only relevant messages
* Storing important information separately
* Using checkpoints

We'll learn these later.

---

# 7. Short-term vs Long-term memory

This distinction is extremely important.

| Short-term memory            | Long-term memory            |
| ---------------------------- | --------------------------- |
| Current conversation/session | Across sessions             |
| Temporary                    | Persistent                  |
| Usually recent context       | User-specific information   |
| Conversation history         | Stored facts/preferences    |
| May disappear after session  | Can remain for months/years |

Example:

### Short-term

```text
User:
My order number is 12345.

Agent:
I'll check it.

User:
What is its status?
```

The agent remembers `12345` during the conversation.

### Long-term

Today:

```text
User:
I prefer Python examples.
```

Next month:

```text
New conversation
```

The agent could still know:

```text
User prefers Python examples.
```

That is **long-term/user-specific memory**, not ordinary short-term memory.

---

# 8. Interview definition

If an interviewer asks:

> **What is short-term memory in an AI agent?**

A good answer is:

> Short-term memory is the temporary context maintained by an agent during a conversation or session. It typically contains recent conversation messages and intermediate agent state, such as tool calls and tool results. This context is provided to the LLM so that it can maintain continuity across multiple turns. Unlike long-term memory, it is generally session-scoped and doesn't need to persist indefinitely.

---

# 9. One important mental model

Remember this:

```text
              ┌──────────────────┐
User ────────►│                  │
              │   Agent State    │
              │                  │
              │ Conversation     │
              │ Tool calls       │
              │ Tool results     │
              │ Temporary data   │
              └────────┬─────────┘
                       │
                       ▼
                      LLM
                       │
                       ▼
                    Response
```

The key idea:

> **Short-term memory gives the agent continuity within a session.**

Next, the natural topic is **Conversation History** — we'll see exactly how messages are maintained, passed to the LLM, and why simply storing the entire history doesn't scale.
