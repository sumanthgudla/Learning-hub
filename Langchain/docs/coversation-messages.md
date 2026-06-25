# Topic 6: Chat History Management

---

## 1. What Is It?

Chat History Management is the discipline of correctly storing, retrieving, and passing multi-turn conversation messages using LangChain's message types and history abstractions. While Topic 5 covered **memory strategies** (how much to remember), this topic covers **the mechanics underneath** — the actual message objects, how history is stored, and how to manage it cleanly across turns. At senior level, what matters is understanding **message type semantics**, **the difference between in-memory and persistent history**, and **how to architect stateful conversation systems that scale** — because getting message management wrong causes subtle bugs that only appear in production.

---

## 2. Core Concepts Table

| Concept | What It Is | When To Use |
|---|---|---|
| `HumanMessage` | Message from the user | Every user input turn |
| `AIMessage` | Message from the model | Every model response turn |
| `SystemMessage` | Behavior/persona instruction | Once at conversation start |
| `FunctionMessage` | Result of a tool/function call | Tool-calling workflows |
| `ToolMessage` | Modern replacement for FunctionMessage | Agent tool results (LangChain v0.1+) |
| `BaseChatMessageHistory` | Abstract base for all history stores | Implement for custom backends |
| `InMemoryChatMessageHistory` | RAM-based history store | Dev/testing, single-process apps |
| `RedisChatMessageHistory` | Redis-backed persistent history | Production, multi-instance apps |
| `add_messages()` | Append messages to history | Programmatic history building |
| `clear()` | Wipe all messages in history | Session reset |

---

## 3. Syntax & Code Examples

### Basic — Message Types

```python
from langchain_core.messages import (
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage
)

# SystemMessage — sets model behavior, typically first in list
system  = SystemMessage(content="You are a helpful Python tutor.")

# HumanMessage — what the user said
human   = HumanMessage(content="What is a decorator?")

# AIMessage — what the model replied
ai      = AIMessage(content="A decorator is a function that wraps another function...")

# Inspect message internals
print(human.type)     # → "human"
print(ai.type)        # → "ai"
print(system.type)    # → "system"

# Messages have additional metadata
ai_with_meta = AIMessage(
    content="A decorator wraps a function...",
    response_metadata={"model": "gpt-4o", "finish_reason": "stop"},
    id="msg_abc123"
)
print(ai_with_meta.response_metadata)  # → {"model": "gpt-4o", ...}
```

---

### `InMemoryChatMessageHistory` — Core History Store

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# Create a history store
history = InMemoryChatMessageHistory()

# Add messages
history.add_message(SystemMessage(content="You are a Python tutor."))
history.add_message(HumanMessage(content="What is a generator?"))
history.add_message(AIMessage(content="A generator yields values lazily..."))
history.add_message(HumanMessage(content="Can you show an example?"))
history.add_message(AIMessage(content="Sure! def gen(): yield 1; yield 2"))

# Retrieve all messages
for msg in history.messages:
    print(f"{msg.type:10} | {msg.content[:50]}")
# → system     | You are a Python tutor.
# → human      | What is a generator?
# → ai         | A generator yields values lazily...
# → human      | Can you show an example?
# → ai         | Sure! def gen(): yield 1; yield 2

# Convenience methods
history.add_user_message("What about send()?")       # adds HumanMessage
history.add_ai_message("send() passes values in...")  # adds AIMessage

print(len(history.messages))  # → 7

# Clear history (session reset)
history.clear()
print(len(history.messages))  # → 0
```

---

### Real-World Pattern — Per-Session History Store

```python
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser

# ── Session store ──────────────────────────────────────────
store: dict[str, InMemoryChatMessageHistory] = {}

def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    """Return existing history or create new one for this session."""
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    return store[session_id]

# ── Chain ──────────────────────────────────────────────────
model  = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])
chain = prompt | model | StrOutputParser()

# ── Chat function ──────────────────────────────────────────
def chat(session_id: str, user_input: str) -> str:
    history = get_session_history(session_id)

    response = chain.invoke({
        "history": history.messages,   # pass messages list directly
        "input":   user_input
    })

    # Manually append this turn to history
    history.add_user_message(user_input)
    history.add_ai_message(response)

    return response

# ── Two independent users ──────────────────────────────────
print(chat("user_001", "My name is Sumanth."))
# → "Nice to meet you, Sumanth!"

print(chat("user_002", "My name is Priya."))
# → "Nice to meet you, Priya!"

print(chat("user_001", "What is my name?"))
# → "Your name is Sumanth."   ← user_001's history intact

print(chat("user_002", "What is my name?"))
# → "Your name is Priya."     ← user_002 unaffected by user_001
```

```
Per-Session History Architecture:
──────────────────────────────────────────────────────
  store = {
    "user_001": InMemoryChatMessageHistory
                └── messages: [H, A, H, A]
    "user_002": InMemoryChatMessageHistory
                └── messages: [H, A, H, A]
    "user_003": InMemoryChatMessageHistory
                └── messages: [H, A]
  }
         │
         │ get_session_history(session_id)
         ▼
  Correct history injected per user
──────────────────────────────────────────────────────
```

---

### Senior-Level — Trimming History by Token Count

```python
from langchain_core.messages import trim_messages
from langchain_openai import ChatOpenAI

# trim_messages gives fine-grained control over what history to keep
trimmer = trim_messages(
    max_tokens=200,                        # hard token budget
    strategy="last",                       # keep the LAST N tokens (most recent)
    token_counter=ChatOpenAI(model="gpt-4o-mini"),  # uses model's tokenizer
    include_system=True,                   # always keep SystemMessage
    allow_partial=False,                   # never cut a message in half
    start_on="human"                       # always start on a HumanMessage
)

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

messages = [
    SystemMessage("You are a helpful assistant."),
    HumanMessage("Tell me about LangChain."),
    AIMessage("LangChain is a framework..."),
    HumanMessage("What about LCEL?"),
    AIMessage("LCEL is the pipe syntax..."),
    HumanMessage("What about memory?"),         # ← most recent
    AIMessage("Memory allows chatbots to..."),  # ← most recent
]

trimmed = trimmer.invoke(messages)
for m in trimmed:
    print(f"{m.type:10} | {m.content[:40]}")
# → system     | You are a helpful assistant.   ← always kept
# → human      | What about memory?             ← most recent turns
# → ai         | Memory allows chatbots to...
```

---

### Senior-Level — Persistent History with Redis

```python
from langchain_community.chat_message_histories import RedisChatMessageHistory

# Drop-in replacement for InMemoryChatMessageHistory
# Messages persist across restarts and multiple app instances
history = RedisChatMessageHistory(
    session_id="user_001",
    url="redis://localhost:6379",
    ttl=3600   # auto-expire session after 1 hour
)

history.add_user_message("What is LangChain?")
history.add_ai_message("LangChain is a framework for building LLM apps.")

# Messages survive app restart — stored in Redis
print(history.messages)
# → [HumanMessage("What is LangChain?"), AIMessage("LangChain is...")]

# Session management
history.clear()   # wipe this session
```

```
Storage Backend Comparison:
──────────────────────────────────────────────────────────
  Backend                  | Persistence | Multi-instance | Use Case
  ─────────────────────────────────────────────────────────
  InMemoryChatMessageHistory| ✗ RAM only  | ✗ single proc  | Dev/testing
  RedisChatMessageHistory   | ✓ Redis     | ✓ yes          | Production API
  SQLChatMessageHistory     | ✓ SQL DB    | ✓ yes          | Enterprise apps
  DynamoDBChatMessageHistory| ✓ DynamoDB  | ✓ yes          | AWS serverless
  MongoDBChatMessageHistory | ✓ MongoDB   | ✓ yes          | Document store
──────────────────────────────────────────────────────────
```

---

## 4. Internals / How It Works

### Message Serialization

Every `BaseMessage` serializes to a dict for storage and API transmission:

```python
from langchain_core.messages import HumanMessage, messages_to_dict, messages_from_dict

messages = [
    HumanMessage(content="Hello"),
    AIMessage(content="Hi there!")
]

# Serialize → for storing in DB / Redis
serialized = messages_to_dict(messages)
print(serialized)
# → [
#     {"type": "human", "data": {"content": "Hello", "additional_kwargs": {}}},
#     {"type": "ai",    "data": {"content": "Hi there!", "additional_kwargs": {}}}
#   ]

# Deserialize → back to message objects
restored = messages_from_dict(serialized)
print(type(restored[0]))  # → HumanMessage
```

### How `InMemoryChatMessageHistory` Works Internally

```
InMemoryChatMessageHistory
├── messages: List[BaseMessage]   ← plain Python list in RAM
├── add_message(msg)              → messages.append(msg)
├── add_messages(msgs)            → messages.extend(msgs)
└── clear()                       → messages = []

No threading locks by default — not safe for concurrent writes
in multi-threaded servers without external synchronization
```

### Message Ordering Contract

```
Correct order (model expects this):
[SystemMessage]          ← optional, always first if present
[HumanMessage]           ← turn 1 user
[AIMessage]              ← turn 1 model
[HumanMessage]           ← turn 2 user
[AIMessage]              ← turn 2 model
...
[HumanMessage]           ← current turn (latest)

Breaking this order causes model confusion:
❌ Two consecutive HumanMessages
❌ AIMessage before any HumanMessage
❌ SystemMessage in the middle of history
```

---

## 5. Interview Questions

**Q1: What's the difference between `HumanMessage`, `AIMessage`, and `SystemMessage` semantically?**

> `SystemMessage` sets the model's behavior and persona — it's an instruction to the model, not a conversation turn. `HumanMessage` represents user input. `AIMessage` represents the model's response. The model is trained to treat these differently: system instructions have highest authority, human messages are the task, and AI messages are prior responses to condition on. Mixing them up causes the model to behave unexpectedly.

**Q2: Why use `InMemoryChatMessageHistory` over a plain Python list?**

> `InMemoryChatMessageHistory` implements `BaseChatMessageHistory`, giving it a standard interface (`add_message`, `add_messages`, `clear`, `messages`). This means you can swap it for `RedisChatMessageHistory` or any other backend without changing your chat logic — same interface, different storage. A plain list has no interface contract and can't be swapped.

**Q3: How would you architect per-user conversation history in a production FastAPI app?**

> Use a session store dict mapping `session_id → ChatMessageHistory` instance. For production, back it with Redis (`RedisChatMessageHistory`) so history survives restarts and works across multiple app instances. Set a TTL on Redis keys to auto-expire inactive sessions and manage memory. Inject history via `MessagesPlaceholder` in the prompt, keyed by session ID on each request.

**Q4: What is `trim_messages` and how is it different from window memory?**

> `trim_messages` is a stateless utility function — it takes a list of messages and trims it to fit within a token budget, always preserving the `SystemMessage` and starting on a `HumanMessage`. Window memory (`ConversationBufferWindowMemory`) is stateful — it's a memory object that manages history over time. Use `trim_messages` when you manage history yourself as a list; use window memory when you want LangChain to manage it automatically.

**Q5: What happens if you pass messages in the wrong order to a ChatModel?**

> Most models will still respond but quality degrades unpredictably. OpenAI's API technically allows any order but the model is trained on alternating Human/AI turns — two consecutive `HumanMessage`s confuse it. Some API providers enforce ordering and will raise a validation error. Always ensure history follows: System → [Human, AI]* → Human pattern.

---

## 6. Practice Problems

### Beginner — `chathistory_prac01_message_store.py`

**Task:** Create an `InMemoryChatMessageHistory` and:
1. Add a `SystemMessage` setting the assistant as a "Python tutor"
2. Simulate 3 full conversation turns using `add_user_message` and `add_ai_message`
3. Print all messages with their type and content
4. Clear the history and confirm it's empty
5. Print the total message count before and after clear

**Expected:**
```
Before clear: 7 messages
system     | You are a Python tutor.
human      | What is a list comprehension?
ai         | A list comprehension is...
...
After clear: 0 messages
```

---

### Senior — `chathistory_prac02_multisession_faq.py`

**Task:** Build a stateful multi-session FAQ assistant that:
1. Uses `InMemoryChatMessageHistory` with a `get_session_history(session_id)` factory
2. Uses `trim_messages` to keep each session's history under 300 tokens before each call
3. Wires everything into an LCEL chain with `MessagesPlaceholder`
4. Simulates 2 users (`session_a`, `session_b`) having completely independent conversations — at least 4 turns each
5. After all turns, prints both sessions' full history side by side
6. Asks both sessions `"What have we discussed?"` — each should recall only their own conversation

**Expected:**
```
Session A history: 8 messages (trimmed if over budget)
Session B history: 8 messages (trimmed if over budget)

Session A: "We discussed Python decorators and generators."
Session B: "We discussed RAG pipelines and vector databases."
```

---

## 7. Common Mistakes & Senior Traps

- **Appending to history before the model call** — if you add the human message to history before invoking the chain, the model sees its own current question in history and gets confused.

```python
# WRONG — human message added before model responds
history.add_user_message(user_input)        # ← too early
response = chain.invoke({"history": history.messages, "input": user_input})
history.add_ai_message(response)

# RIGHT — add both turns after the model responds
response = chain.invoke({"history": history.messages, "input": user_input})
history.add_user_message(user_input)        # ← after invoke
history.add_ai_message(response)            # ← after invoke
```

- **Using `InMemoryChatMessageHistory` in multi-worker deployments** — each worker process has its own RAM. User A hits worker 1, their history is there. Next request hits worker 2 — history is gone. Always use a shared persistent store (Redis, DB) in multi-worker production.

- **Not handling `SystemMessage` in `trim_messages`** — if you trim without `include_system=True`, the system prompt gets dropped from history. The model loses its persona and behavior instructions silently.

- **Confusing `history.messages` (list) with `history` (object)** — `MessagesPlaceholder` needs a list:

```python
# WRONG — passing the history object itself
chain.invoke({"history": history, "input": user_input})

# RIGHT — passing the messages list
chain.invoke({"history": history.messages, "input": user_input})
```

- **Growing `store` dict indefinitely** — in a long-running server, every new `session_id` adds an entry. Without eviction, this leaks memory. Add TTL logic or use Redis with `ttl` parameter.

```python
import time

store = {}
SESSION_TTL = 3600  # 1 hour

def get_session_history(session_id: str):
    now = time.time()
    # Evict expired sessions
    expired = [k for k, v in store.items() if now - v["created"] > SESSION_TTL]
    for k in expired:
        del store[k]

    if session_id not in store:
        store[session_id] = {
            "history": InMemoryChatMessageHistory(),
            "created": now
        }
    return store[session_id]["history"]
```

- **`ToolMessage` vs `FunctionMessage`** — `FunctionMessage` is legacy from OpenAI's old function-calling API. Always use `ToolMessage` in new code. Mixing them causes serialization errors in some LangChain versions.

---

Say **"next"** when you're ready for **Topic 7: RunnableWithMessageHistory**!