# Topic 2: Conversation History

Conversation history is the **sequence of previous messages exchanged between the user and the agent**.

It is one of the simplest and most common forms of short-term memory.

---

## 1. Basic idea

Without conversation history:

```text
User → "My name is Sumanth"
Agent → "Nice to meet you"

User → "What is my name?"
Agent → "I don't know"
```

With conversation history:

```text
User → "My name is Sumanth"
Agent → "Nice to meet you"

                 ↓
        Conversation History
                 ↓

User → "What is my name?"
Agent → "Your name is Sumanth"
```

The important point is:

> The LLM doesn't magically remember the previous message. The application sends the previous messages as context.

---

# 2. What does conversation history look like?

Typically, messages are stored like this:

```python
messages = [
    {
        "role": "user",
        "content": "My name is Sumanth"
    },
    {
        "role": "assistant",
        "content": "Nice to meet you, Sumanth!"
    },
    {
        "role": "user",
        "content": "What is my name?"
    }
]
```

Then:

```python
response = llm.invoke(messages)
```

The LLM receives the entire relevant conversation.

Conceptually:

```text
                  Conversation History
                         │
                         ▼
User ────────────────►  LLM
                         │
                         ▼
                     Response
```

---

# 3. Different message types

In an agent system, history isn't necessarily just:

```text
user → assistant
```

You can have several types of messages.

### Human message

```python
HumanMessage(
    content="What is the weather in Hyderabad?"
)
```

### AI message

```python
AIMessage(
    content="I'll check the weather."
)
```

### Tool message

```python
ToolMessage(
    content="32°C and sunny"
)
```

So an agent's history could look like:

```text
Human
  ↓
AI
  ↓
Tool
  ↓
AI
```

For example:

```text
User:
What is the weather in Hyderabad?

Assistant:
I'll check.

Assistant → Tool:
get_weather("Hyderabad")

Tool:
32°C, sunny

Assistant:
The weather is 32°C and sunny.
```

All of this can become part of the agent's short-term state.

---

# 4. Why tool messages matter

This becomes especially important with agents.

Suppose:

```text
User:
What is 20 USD in INR?
```

Agent:

```text
LLM
 ↓
currency_tool
 ↓
₹1,680
 ↓
LLM
 ↓
"20 USD is approximately ₹1,680."
```

The agent may need to maintain:

```text
User request
       ↓
Tool call
       ↓
Tool result
       ↓
Final response
```

Otherwise, the LLM might not know what happened during the tool execution.

---

# 5. Conversation history grows

This creates a major problem.

Imagine a chatbot conversation:

```text
Turn 1     → 500 tokens
Turn 2     → 700 tokens
Turn 3     → 900 tokens
...
Turn 100   → 50,000 tokens
```

If you send everything on every request:

```text
Request 1 → 500 tokens
Request 2 → 1,200 tokens
Request 3 → 2,100 tokens
...
Request 100 → 50,000 tokens
```

So both **cost and latency increase**.

And eventually you may hit the model's context limit.

---

# 6. How do production systems handle this?

They generally don't keep sending unlimited history.

Common approaches are:

### A. Keep recent messages

```text
Old messages
     ↓
discard

Recent messages
     ↓
LLM
```

For example:

```text
Keep last 10 messages
```

---

### B. Summarize old messages

Instead of:

```text
Message 1
Message 2
Message 3
...
Message 50
```

Create:

```text
Summary:
User is building an AI agent using Python.
They are learning tool calling and memory.
They prefer simple explanations.
```

Then:

```text
Summary
+
Recent messages
        ↓
       LLM
```

This is much more efficient.

---

### C. Retrieve relevant history

Instead of sending everything, retrieve only history relevant to the current question.

For example:

```text
1000 previous messages
        ↓
   Retrieval
        ↓
Relevant 5 messages
        ↓
       LLM
```

This starts moving toward **long-term memory / semantic memory**, which we'll cover later.

---

# 7. Conversation history vs agent state

These are related but **not exactly the same**.

### Conversation history

Primarily:

```text
User messages
Assistant messages
Tool messages
```

### Agent state

Can contain much more:

```python
state = {
    "messages": [...],
    "user_id": "123",
    "current_task": "book_flight",
    "selected_flight": "...",
    "tool_result": "...",
    "retry_count": 1
}
```

So:

> **Conversation history can be one component of agent state.**

Think:

```text
Agent State
│
├── messages
├── current task
├── tool results
├── intermediate data
└── other temporary information
```

---

# 8. Example: Travel agent

User:

```text
I want to fly from Hyderabad to Delhi.
```

Agent state:

```python
{
    "messages": [
        "I want to fly from Hyderabad to Delhi."
    ],
    "origin": "Hyderabad",
    "destination": "Delhi"
}
```

User:

```text
I want to travel tomorrow.
```

Now the state can become:

```python
{
    "messages": [
        "I want to fly from Hyderabad to Delhi.",
        "I want to travel tomorrow."
    ],
    "origin": "Hyderabad",
    "destination": "Delhi",
    "date": "tomorrow"
}
```

The **messages** are conversation history.

The extracted fields are **agent state**.

This distinction becomes very important when working with **LangGraph**.

---

# 9. Important interview question

### Q: Does ChatGPT/LLM automatically remember previous conversations?

A good answer:

> Not inherently. The application must provide the relevant conversation context to the model, either through the current request's message history or through a memory system that retrieves relevant information. The model itself doesn't automatically maintain persistent conversational memory between independent API calls.

---

# 10. The limitation

Conversation history gives us:

```text
Context
   +
Continuity
```

But it doesn't solve:

```text
❌ Unlimited memory
❌ Persistent memory
❌ Cross-session memory
❌ Efficient retrieval of old information
```

That's why we need additional memory mechanisms.

---

## Mental model

Keep this hierarchy in mind:

```text
                    Agent Memory
                         │
             ┌───────────┴───────────┐
             │                       │
       Short-term               Long-term
             │                       │
      Conversation              Persistent
         history                  memory
             │                       │
       Current session          Across sessions
```

And:

```text
Conversation History
        ↓
can be part of
        ↓
Agent State
```

### Next topic: **Long-Term Memory**

We'll cover how an agent can remember something **today and still know it in a completely new conversation tomorrow**, including where that information is actually stored.
