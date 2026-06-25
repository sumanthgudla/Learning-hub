Got it! Here's the full topic queue locked in:

1. **LangChain Architecture Overview**
2. Prompt Templates
3. LLM & Chat Model Integration
4. Output Parsers

---

# Topic 1: LangChain Architecture Overview

---

## 1. What Is It?

LangChain is a framework for building LLM-powered applications by chaining together modular components — prompts, models, parsers, retrievers, memory, and tools. At senior level, what matters is understanding **why** the architecture evolved: the old "Chain" classes were rigid and hard to compose, so LangChain introduced **LCEL (LangChain Expression Language)** — a pipe-based system where every component is a `Runnable`, making chains composable, streamable, and batchable by default.

---

## 2. Core Concepts Table

| Concept | What It Is | Why It Matters |
|---|---|---|
| `LLM` | Takes a string, returns a string | Legacy, stateless text completion |
| `ChatModel` | Takes messages, returns a message | Modern standard (OpenAI, Anthropic, etc.) |
| `Runnable` | Base interface every component implements | Enables `.invoke()`, `.stream()`, `.batch()` |
| `LCEL` | Pipe `\|` syntax to chain Runnables | Replaces legacy Chain classes |
| `.invoke()` | Run chain with one input, get one output | Standard single call |
| `.stream()` | Get output token-by-token as a generator | For streaming UIs |
| `.batch()` | Run chain over a list of inputs in parallel | For bulk processing |
| `RunnablePassthrough` | Passes input through unchanged | Used to forward original input alongside transforms |
| `RunnableLambda` | Wraps any Python function as a Runnable | Custom logic inside a chain |
| `RunnableParallel` | Runs multiple Runnables on same input simultaneously | Fan-out pattern |

---

## 3. Syntax & Code Examples

### Basic — LLM vs ChatModel

```python
from langchain_openai import OpenAI, ChatOpenAI
from langchain_core.messages import HumanMessage

# --- Legacy LLM (string in, string out) ---
llm = OpenAI(model="gpt-3.5-turbo-instruct")
result = llm.invoke("What is the capital of France?")
print(result)  # → " Paris"

# --- Modern ChatModel (messages in, message out) ---
chat = ChatOpenAI(model="gpt-4o")
result = chat.invoke([HumanMessage(content="What is the capital of France?")])
print(result.content)   # → "Paris"
print(type(result))     # → AIMessage
```

---

### LCEL Pipe Syntax — Building a Chain

```python
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Each piece is a Runnable
prompt = ChatPromptTemplate.from_template("Tell me a joke about {topic}")
model = ChatOpenAI(model="gpt-4o")
parser = StrOutputParser()

# | is the LCEL pipe operator — chains Runnables left to right
chain = prompt | model | parser

result = chain.invoke({"topic": "Python"})
print(result)  # → "Why do Python devs prefer dark mode? Because light attracts bugs!"
```

```
LCEL Data Flow:
─────────────────────────────────────────────────────
  {"topic": "Python"}
        │
        ▼
  [ChatPromptTemplate]  → formats into ChatPromptValue (list of messages)
        │
        ▼
  [ChatOpenAI]          → sends to API, returns AIMessage
        │
        ▼
  [StrOutputParser]     → extracts .content string
        │
        ▼
  "Why do Python devs..."
─────────────────────────────────────────────────────
```

---

### `.stream()` and `.batch()`

```python
# Stream — yields chunks as they arrive (token by token)
for chunk in chain.stream({"topic": "cats"}):
    print(chunk, end="", flush=True)
# → prints the joke incrementally as tokens arrive

# Batch — runs over multiple inputs in parallel
results = chain.batch([
    {"topic": "Python"},
    {"topic": "JavaScript"},
    {"topic": "Java"}
])
# → returns a list of 3 joke strings, fetched concurrently
```

---

### Senior-Level — `RunnableParallel` and `RunnablePassthrough`

```python
from langchain_core.runnables import RunnableParallel, RunnablePassthrough

# Fan-out: run two different chains on the same input simultaneously
chain = RunnableParallel({
    "joke":    ChatPromptTemplate.from_template("Tell a joke about {topic}") | model | parser,
    "fact":    ChatPromptTemplate.from_template("Give a fact about {topic}") | model | parser,
    "original": RunnablePassthrough()   # just passes the input dict through unchanged
})

result = chain.invoke({"topic": "Python"})
print(result["joke"])      # → joke string
print(result["fact"])      # → fact string
print(result["original"])  # → {"topic": "Python"}  ← original input preserved
```

```
RunnableParallel Flow:

        {"topic": "Python"}
               │
       ┌───────┼───────────┐
       ▼       ▼           ▼
  [joke       [fact      [RunnablePassthrough]
   chain]      chain]
       │       │           │
       └───────┴───────────┘
               │
        {"joke": ..., "fact": ..., "original": ...}
```

---

### Senior-Level — `RunnableLambda` for custom logic

```python
from langchain_core.runnables import RunnableLambda

# Wrap any Python function as a Runnable — plugs into LCEL pipe
def shout(text: str) -> str:
    return text.upper() + "!!!"

chain = (
    ChatPromptTemplate.from_template("Say hello to {name}")
    | model
    | StrOutputParser()
    | RunnableLambda(shout)   # ← custom post-processing step
)

result = chain.invoke({"name": "Sumanth"})
print(result)  # → "HELLO, SUMANTH!!!"
```

---

## 4. Internals / How It Works

### The `Runnable` Protocol

Every component in LangChain implements the `Runnable` abstract base class from `langchain_core`. This gives every piece a **uniform interface**:

```
Runnable (ABC)
├── .invoke(input)         → single input → single output
├── .stream(input)         → single input → Iterator of chunks
├── .batch(inputs)         → list of inputs → list of outputs (parallel via threadpool)
└── .ainvoke / .astream / .abatch  → async versions
```

### How the `|` Pipe Operator Works

```python
# This line:
chain = prompt | model | parser

# Is exactly equivalent to:
from langchain_core.runnables import RunnableSequence
chain = RunnableSequence(first=prompt, middle=[model], last=parser)
```

Python's `__or__` dunder method is overridden on `Runnable` to return a `RunnableSequence`. No magic — just operator overloading.

### LLM vs ChatModel Internally

```
LLM:
  Input:  str
  Output: str
  API:    /completions endpoint

ChatModel:
  Input:  List[BaseMessage]  (HumanMessage, AIMessage, SystemMessage)
  Output: AIMessage
  API:    /chat/completions endpoint
```

ChatModels are now the standard. The `LLM` class exists for legacy completion-style models only.

---

## 5. Interview Questions

**Q1: What problem did LCEL solve that the old Chain classes didn't?**

> Old chains like `LLMChain`, `SequentialChain` were rigid class hierarchies. Adding streaming, batching, or async required separate code paths per chain type. LCEL makes every component a `Runnable` with a uniform interface — so streaming, batching, and async work automatically on any chain you build, without extra code.

**Q2: What's the difference between `LLM` and `ChatModel` in LangChain?**

> `LLM` takes a raw string and returns a string — it maps to completion-style APIs. `ChatModel` takes a list of `BaseMessage` objects (Human/AI/System) and returns an `AIMessage` — it maps to chat/completions APIs. Modern work always uses `ChatModel`; `LLM` is legacy.

**Q3: How does `.batch()` work internally — is it actually parallel?**

> Yes. `.batch()` uses a `ThreadPoolExecutor` under the hood to run `.invoke()` for each input concurrently. For async chains, `.abatch()` uses `asyncio.gather`. You can control parallelism with the `max_concurrency` parameter.

**Q4: When would you use `RunnableParallel` vs sequential LCEL?**

> Use `RunnableParallel` when you want to run multiple independent chains on the **same input simultaneously** — e.g., generate a summary AND extract keywords from the same document in one pass. Use sequential LCEL (`|`) when the output of one step is the input of the next.

**Q5: What is `RunnablePassthrough` and when is it critical?**

> `RunnablePassthrough` passes the input through unchanged. It's critical in RAG chains where you need to carry the original question forward after retrieval — e.g., `{"context": retriever, "question": RunnablePassthrough()}` so both the retrieved docs and the original question reach the prompt template together.

---

## 6. Practice Problems

### Beginner — `langchain_arch_prac01_basic_lcel_chain.py`

**Task:** Build a simple LCEL chain that:
- Takes a `{"country": "..."}` input
- Uses a prompt: `"What is the capital of {country}?"`
- Calls a ChatModel
- Parses the output to a plain string
- Prints the result

**Expected:**
```
Input:  {"country": "Japan"}
Output: "Tokyo"
```

---

### Senior — `langchain_arch_prac02_parallel_fan_out.py`

**Task:** Build a `RunnableParallel` chain that takes `{"text": "..."}` and simultaneously produces:
- `"summary"` — a one-sentence summary of the text
- `"sentiment"` — positive / negative / neutral classification
- `"keywords"` — 3 keywords as a comma-separated list
- `"original"` — the original input text (using `RunnablePassthrough`)

Then post-process the result with a `RunnableLambda` that formats everything into a clean report string and prints it.

**Expected output shape:**
```
=== Analysis Report ===
Original: "LangChain is a powerful framework..."
Summary:  LangChain simplifies building LLM apps.
Sentiment: Positive
Keywords: LangChain, framework, LLM
```

---

## 7. Common Mistakes & Senior Traps

- **Using `LLMChain` in new code** — it's legacy. Interviewers will notice. Always use LCEL + `ChatPromptTemplate | ChatModel | Parser`.

- **Forgetting that `|` returns a `RunnableSequence`, not a new class** — the chain is lazy; nothing runs until `.invoke()` / `.stream()` / `.batch()` is called.

- **Treating `.stream()` like `.invoke()`** — `.stream()` returns a generator; you must iterate it. Assigning it to a variable and printing it gives you a generator object, not the text.

```python
# WRONG
result = chain.stream({"topic": "cats"})
print(result)  # → <generator object ...>

# RIGHT
for chunk in chain.stream({"topic": "cats"}):
    print(chunk, end="")
```

- **Not using `RunnablePassthrough` in RAG chains** — a very common mistake is losing the original question after the retrieval step, so the prompt template can't fill the `{question}` variable.

- **Confusing `.batch()` parallelism with true async** — `.batch()` uses threads, not async coroutines. For true async concurrency (e.g., inside FastAPI), use `.abatch()` with `await`.

- **`RunnableLambda` input type assumption** — the lambda receives whatever the previous step outputs. If the previous step returns an `AIMessage`, your lambda gets an `AIMessage`, not a string. Always pair with `StrOutputParser` first if you want plain text.

---

Take your time with the practice problems, and say **"next"** when you're ready for **Topic 2: Prompt Templates**!