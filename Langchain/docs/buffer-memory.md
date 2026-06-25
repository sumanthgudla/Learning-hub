Got it! New topic queue locked in:

5. **Conversation Memory Types**
6. **Chat History Management**
7. **RunnableWithMessageHistory**

---

# Topic 5: Conversation Memory Types

---

## 1. What Is It?

Conversation Memory gives your LLM app the ability to remember past turns of a conversation. Without it, every call to the model is stateless — it has no idea what was said before. At senior level, what matters is understanding **which memory strategy to use given token constraints**, **why naive buffer memory breaks in production**, and **the trade-offs between accuracy (buffer), recency (window), and compression (summary)** — because memory is where most chatbot production failures originate.

---

## 2. Core Concepts Table

| Memory Type | What It Stores | Token Cost | Best For |
|---|---|---|---|
| `ConversationBufferMemory` | Full history, every message | Grows unboundedly | Short sessions, prototyping |
| `ConversationBufferWindowMemory` | Last `k` turns only | Fixed ceiling | Production chatbots with turn limit |
| `ConversationSummaryMemory` | LLM-generated summary of history | Compressed, grows slowly | Long sessions needing context |
| `ConversationSummaryBufferMemory` | Summary of old + buffer of recent | Bounded by token limit | Best of both — production default |
| `ConversationTokenBufferMemory` | Recent messages up to token limit | Hard token ceiling | When you need strict cost control |

---

## 3. Syntax & Code Examples

### Basic — `ConversationBufferMemory`

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    return_messages=True,   # return List[BaseMessage] not a string
    memory_key="history"    # key used in the prompt template
)

# Manually save turns (simulating a conversation)
memory.save_context(
    {"input": "My name is Sumanth."},
    {"output": "Nice to meet you, Sumanth!"}
)
memory.save_context(
    {"input": "I work at Pegasystems."},
    {"output": "That's a great company!"}
)

# Load everything back
print(memory.load_memory_variables({}))
# → {"history": [
#     HumanMessage("My name is Sumanth."),
#     AIMessage("Nice to meet you, Sumanth!"),
#     HumanMessage("I work at Pegasystems."),
#     AIMessage("That's a great company!")
#   ]}
```

```
Buffer Memory — grows with every turn:
─────────────────────────────────────────────
Turn 1:  [H][A]                     ~50 tokens
Turn 2:  [H][A][H][A]              ~100 tokens
Turn 5:  [H][A][H][A][H][A][H][A][H][A]  ~250 tokens
Turn 50: ████████████████████████  ~2500 tokens  ← hits context limit!
─────────────────────────────────────────────
```

---

### `ConversationBufferWindowMemory` — Fixed Window

```python
from langchain.memory import ConversationBufferWindowMemory

# k=3 means keep only the last 3 human+AI turn pairs
memory = ConversationBufferWindowMemory(
    k=3,
    return_messages=True,
    memory_key="history"
)

# Simulate 5 turns
for i in range(1, 6):
    memory.save_context(
        {"input": f"Message {i}"},
        {"output": f"Response {i}"}
    )

print(memory.load_memory_variables({}))
# → Only turns 3, 4, 5 are retained — turns 1 and 2 are gone
# {"history": [
#   HumanMessage("Message 3"), AIMessage("Response 3"),
#   HumanMessage("Message 4"), AIMessage("Response 4"),
#   HumanMessage("Message 5"), AIMessage("Response 5"),
# ]}
```

```
Window Memory (k=3) — sliding window:
─────────────────────────────────────────────
After turn 1:  [T1]
After turn 2:  [T1][T2]
After turn 3:  [T1][T2][T3]
After turn 4:      [T2][T3][T4]   ← T1 dropped
After turn 5:          [T3][T4][T5]   ← T2 dropped
─────────────────────────────────────────────
```

---

### Real-World Pattern — `ConversationSummaryMemory`

```python
from langchain.memory import ConversationSummaryMemory
from langchain_openai import ChatOpenAI

# Needs an LLM to generate summaries
memory = ConversationSummaryMemory(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    return_messages=True,
    memory_key="history"
)

memory.save_context(
    {"input": "I'm building a RAG pipeline for a legal document system."},
    {"output": "That's interesting! What vector database are you using?"}
)
memory.save_context(
    {"input": "I'm using Pinecone with text-embedding-3-small."},
    {"output": "Good choice. Have you handled chunking strategy yet?"}
)
memory.save_context(
    {"input": "Yes, I'm using recursive character splitting at 512 tokens."},
    {"output": "Smart. What retrieval strategy — top-k or MMR?"}
)

print(memory.load_memory_variables({}))
# → {"history": [
#     SystemMessage(content="The human is building a RAG pipeline for legal
#     documents using Pinecone with text-embedding-3-small and recursive
#     character splitting at 512 tokens. Discussion is now on retrieval strategy.")
#   ]}
# ↑ Entire conversation compressed into one SystemMessage
```

```
Summary Memory — compresses as it grows:
─────────────────────────────────────────────
Turn 1-3:  [H][A][H][A][H][A]
                    │
                    ▼ LLM summarizes
           [SystemMessage: "User is building RAG..."]

Turn 4:    [SystemMessage: "User is building RAG..."][H][A]

Turn 5-7:  New turns added → LLM re-summarizes
           [SystemMessage: "User is building RAG with MMR retrieval..."]
─────────────────────────────────────────────
```

---

### Senior-Level — `ConversationSummaryBufferMemory`

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

# Best of both worlds:
# - Keeps recent messages as-is (full fidelity)
# - Summarizes older messages when token limit is exceeded
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    max_token_limit=200,    # when buffer exceeds this, oldest turns get summarized
    return_messages=True,
    memory_key="history"
)

# First few turns go into buffer as-is
memory.save_context({"input": "What is LangChain?"}, {"output": "It's a framework..."})
memory.save_context({"input": "What is LCEL?"}, {"output": "It's the pipe syntax..."})
memory.save_context({"input": "What is a Runnable?"}, {"output": "It's the base interface..."})
# ... more turns until token limit exceeded ...
memory.save_context({"input": "What is a ChatModel?"}, {"output": "It takes messages..."})

print(memory.load_memory_variables({}))
# → {"history": [
#     SystemMessage("Human asked about LangChain, LCEL, and Runnables..."),  ← summarized
#     HumanMessage("What is a ChatModel?"),   ← recent turns kept verbatim
#     AIMessage("It takes messages...")
#   ]}
```

```
SummaryBuffer Memory — hybrid approach:
─────────────────────────────────────────────────
     OLDER TURNS              RECENT TURNS
  ┌─────────────────┐    ┌──────────────────────┐
  │ SystemMessage:  │    │ HumanMessage (turn N-2)│
  │ "Summary of    │    │ AIMessage    (turn N-2)│
  │  turns 1-5..." │    │ HumanMessage (turn N-1)│
  └─────────────────┘    │ AIMessage    (turn N-1)│
                         │ HumanMessage (turn N)  │
   Compressed            │ AIMessage    (turn N)  │
   (low tokens)          └──────────────────────┘
                          Full fidelity (recent)
─────────────────────────────────────────────────
```

---

### Senior-Level — Wiring Memory into an LCEL Chain

```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

model = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)

memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    max_token_limit=500,
    return_messages=True,
    memory_key="history"
)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful AI assistant."),
    MessagesPlaceholder(variable_name="history"),  # ← memory injected here
    ("human", "{input}")
])

chain = prompt | model | StrOutputParser()

def chat(user_input: str) -> str:
    # Load memory into history
    history = memory.load_memory_variables({})["history"]

    # Run chain
    response = chain.invoke({
        "history": history,
        "input": user_input
    })

    # Save this turn to memory
    memory.save_context({"input": user_input}, {"output": response})

    return response

# Multi-turn conversation
print(chat("My name is Sumanth and I work in Hyderabad."))
print(chat("I specialise in LangChain and RAG pipelines."))
print(chat("What do you know about me so far?"))
# → "You told me your name is Sumanth, you work in Hyderabad
#    and specialise in LangChain and RAG pipelines."
```

---

## 4. Internals / How It Works

### Where Messages Live

```
Memory object
├── chat_memory: ChatMessageHistory
│   └── messages: List[BaseMessage]   ← actual storage
├── load_memory_variables({})          ← formats for prompt
└── save_context(inputs, outputs)      ← appends to messages
```

All memory types wrap a `ChatMessageHistory` object internally. The difference between them is only in **how they format that history** when `load_memory_variables()` is called.

### Token Counting in `ConversationSummaryBufferMemory`

```
On every save_context() call:
    1. Append new messages to buffer
    2. Count tokens of entire buffer using tiktoken
    3. If total > max_token_limit:
         a. Take oldest messages
         b. Call LLM: "Summarize this conversation so far: [messages]"
         c. Replace those messages with SystemMessage(summary)
    4. Return — buffer now within token limit
```

### `return_messages=True` vs `False`

```python
# return_messages=False (default) → string format
memory.load_memory_variables({})
# → {"history": "Human: Hi\nAI: Hello!"}  ← flat string

# return_messages=True → message objects
memory.load_memory_variables({})
# → {"history": [HumanMessage("Hi"), AIMessage("Hello!")]}
```

Always use `return_messages=True` with `ChatPromptTemplate` + `MessagesPlaceholder`. The string format is for legacy `PromptTemplate` only.

---

## 5. Interview Questions

**Q1: Why does `ConversationBufferMemory` break in production?**

> It appends every message indefinitely. Long conversations exceed the model's context window — typically 4k–128k tokens depending on the model. When you hit the limit, the API throws a context length error. In production you need either a window, token budget, or summary strategy to keep memory bounded.

**Q2: What are the trade-offs between `ConversationWindowMemory` and `ConversationSummaryMemory`?**

> Window memory is fast and cheap — no extra LLM calls — but loses old context entirely. Summary memory preserves a compressed version of old context but costs an extra LLM call every time it summarizes, adding latency. `ConversationSummaryBufferMemory` is the production default — it keeps recent turns verbatim for fidelity and compresses older turns to control cost.

**Q3: What does `max_token_limit` control in `ConversationSummaryBufferMemory`?**

> It's the token budget for the raw message buffer. When the buffer exceeds this limit, the oldest messages are summarized by the LLM and replaced with a `SystemMessage` containing the summary. This keeps the total memory footprint bounded while preserving recent context at full fidelity.

**Q4: Why must you pass `return_messages=True` when using `MessagesPlaceholder`?**

> `MessagesPlaceholder` expects a `List[BaseMessage]` to inject into the prompt. With `return_messages=False`, memory returns a flat string — `MessagesPlaceholder` can't inject that. The type mismatch causes either a silent formatting error or an exception depending on LangChain version.

**Q5: Where is conversation history actually stored in LangChain memory objects?**

> In a `ChatMessageHistory` object attached as `memory.chat_memory`. Its `.messages` attribute is a `List[BaseMessage]`. All memory types wrap this — they differ only in how they process and format that list when `load_memory_variables()` is called. This means you can swap memory strategies without changing storage — just change the wrapper.

---

## 6. Practice Problems

### Beginner — `convmemory_prac01_window_chatbot.py`

**Task:** Build a simple chatbot using `ConversationBufferWindowMemory` with `k=3`. Simulate 5 conversation turns manually using `save_context()`. After all 5 turns, print the memory contents and verify only the last 3 turns are present.

**Expected:**
```
Memory after 5 turns:
HumanMessage: "Turn 3 input"
AIMessage:    "Turn 3 output"
HumanMessage: "Turn 4 input"
AIMessage:    "Turn 4 output"
HumanMessage: "Turn 5 input"
AIMessage:    "Turn 5 output"
```

---

### Senior — `convmemory_prac02_summary_buffer_chatbot.py`

**Task:** Build a full multi-turn chatbot using `ConversationSummaryBufferMemory` with `max_token_limit=150` that:
1. Wires memory into an LCEL chain via `MessagesPlaceholder`
2. Has a `chat(user_input)` helper function that loads memory, invokes chain, saves context
3. After each turn, prints the current memory state showing whether it's in buffer or summary form
4. Run at least 6 turns with enough content to trigger summarization
5. On the final turn ask `"What have we discussed so far?"` — model should give a coherent summary

**Expected:**
```
Turn 1-3: memory shows raw [HumanMessage, AIMessage] pairs
Turn 4+:  memory shows SystemMessage (summary) + recent raw turns
Final: model accurately recalls earlier topics from the summary
```

---

## 7. Common Mistakes & Senior Traps

- **Using `ConversationBufferMemory` in production without a token limit** — the most common mistake. Works in demos, crashes under real usage when conversations get long.

- **Forgetting `return_messages=True`** — causes a type mismatch with `MessagesPlaceholder`. The error is not always obvious.

```python
# WRONG
memory = ConversationBufferMemory(memory_key="history")
# load_memory_variables returns {"history": "Human: ...\nAI: ..."}
# MessagesPlaceholder chokes on a string

# RIGHT
memory = ConversationBufferMemory(memory_key="history", return_messages=True)
# returns {"history": [HumanMessage(...), AIMessage(...)]}
```

- **Not saving context after every turn** — memory only updates when `save_context()` is called explicitly. If you forget, the chatbot has goldfish memory — remembers nothing between calls.

- **Using the LLM summary model as the chat model** — `ConversationSummaryMemory` needs an LLM to summarize. Using your expensive primary model (gpt-4o) for this wastes money. Use a cheap fast model (gpt-4o-mini) for summarization.

```python
# WRONG — expensive model doing cheap summarization work
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-4o"),   # overkill
    max_token_limit=500
)

# RIGHT — cheap model for summarization
memory = ConversationSummaryBufferMemory(
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    max_token_limit=500
)
```

- **`ConversationSummaryMemory` on short conversations** — it summarizes every turn even when history is tiny. This adds latency and cost with no benefit. Only use summary-based memory once history exceeds ~300–500 tokens; use `ConversationSummaryBufferMemory` which handles this automatically.

- **Sharing a memory object across users** — a common architectural mistake. One memory object = one conversation. In multi-user apps, each user session needs its own memory instance, or you get conversation bleed between users.

```python
# WRONG — global memory shared across all users
memory = ConversationBufferWindowMemory(k=5)

# RIGHT — per-session memory
sessions = {}
def get_memory(session_id: str):
    if session_id not in sessions:
        sessions[session_id] = ConversationBufferWindowMemory(k=5, return_messages=True)
    return sessions[session_id]
```

---

Say **"next"** when you're ready for **Topic 6: Chat History Management**!