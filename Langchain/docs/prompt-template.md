# Topic 2: Prompt Templates

---

## 1. What Is It?

A Prompt Template is a reusable, parameterized blueprint for constructing LLM inputs. Instead of hardcoding strings, you define a template with variables and fill them at runtime. At senior level, what matters is knowing **which template type to use when**, how to compose complex multi-turn prompts, how partial variables work, and how few-shot prompting fits into the template system — because every real LLM app lives or dies on prompt quality and maintainability.

---

## 2. Core Concepts Table

| Concept | What It Is | When To Use |
|---|---|---|
| `PromptTemplate` | String template with `{variables}` | Single string input to LLM (legacy style) |
| `ChatPromptTemplate` | List of role-based message templates | ChatModels — standard modern usage |
| `SystemMessagePromptTemplate` | Template for system role message | Setting model behavior/persona |
| `HumanMessagePromptTemplate` | Template for user role message | User turn in conversation |
| `AIMessagePromptTemplate` | Template for assistant role message | Few-shot examples, simulated history |
| `MessagesPlaceholder` | Injects a dynamic list of messages | Chat history / memory injection |
| `partial()` | Pre-fill some variables, leave others open | Reusable base prompts with fixed context |
| Few-shot template | Injects examples before the real query | Teaching the model output format/style |

---

## 3. Syntax & Code Examples

### Basic — `PromptTemplate`

```python
from langchain_core.prompts import PromptTemplate

# Define template with {variable} placeholders
template = PromptTemplate.from_template(
    "Explain {concept} in simple terms for a {audience}."
)

# .invoke() returns a StringPromptValue — call .text to see the string
result = template.invoke({"concept": "recursion", "audience": "5-year-old"})
print(result.text)
# → "Explain recursion in simple terms for a 5-year-old."
```

---

### Standard Modern Usage — `ChatPromptTemplate`

```python
from langchain_core.prompts import ChatPromptTemplate

# from_messages takes a list of (role, template_string) tuples
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant who speaks like {persona}."),
    ("human",  "Explain {topic} in 2 sentences.")
])

# .invoke() returns a ChatPromptValue — a list of formatted messages
result = prompt.invoke({"persona": "a pirate", "topic": "black holes"})
print(result.messages)
# → [SystemMessage(content="You are a helpful...pirate."),
#    HumanMessage(content="Explain black holes in 2 sentences.")]
```

```
ChatPromptTemplate Structure:
─────────────────────────────────────────
  Template Definition
  ┌──────────────────────────────────┐
  │  ("system", "You are {persona}") │
  │  ("human",  "Explain {topic}")   │
  └──────────────────────────────────┘
            │  .invoke(vars)
            ▼
  Formatted Messages List
  ┌──────────────────────────────────┐
  │  SystemMessage("You are a pirate")│
  │  HumanMessage("Explain black holes")│
  └──────────────────────────────────┘
            │
            ▼  (fed to ChatModel)
         AIMessage(...)
─────────────────────────────────────────
```

---

### Real-World Pattern — `MessagesPlaceholder` for Chat History

```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),  # ← injects any list of messages here
    ("human", "{input}")
])

# Simulating a conversation with existing history
history = [
    HumanMessage(content="My name is Sumanth."),
    AIMessage(content="Nice to meet you, Sumanth!")
]

result = prompt.invoke({
    "history": history,
    "input": "What is my name?"
})

print(result.messages)
# → [SystemMessage(...),
#    HumanMessage("My name is Sumanth."),
#    AIMessage("Nice to meet you, Sumanth!"),
#    HumanMessage("What is my name?")]
```

> This is the standard pattern for **memory-aware chatbots** — `MessagesPlaceholder` is where your memory/history gets injected.

---

### Senior-Level — Partial Variables

```python
from langchain_core.prompts import ChatPromptTemplate
from datetime import datetime

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an assistant. Today's date is {date}. Language: {language}."),
    ("human", "{question}")
])

# partial() pre-fills some variables now, leaves others for later
# Useful for variables that are fixed at app startup but vary at runtime
prompt_english = prompt.partial(
    date=datetime.now().strftime("%Y-%m-%d"),  # fixed at startup
    language="English"                          # fixed per deployment config
)

# Later, only the remaining variable needs to be provided
result = prompt_english.invoke({"question": "What is LCEL?"})
print(result.messages[0].content)
# → "You are an assistant. Today's date is 2026-06-23. Language: English."
```

---

### Senior-Level — Few-Shot Prompt Template

```python
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

# Step 1: Define what each example looks like
example_prompt = ChatPromptTemplate.from_messages([
    ("human", "{input}"),
    ("ai",    "{output}")
])

# Step 2: Provide the examples
examples = [
    {"input": "2+2",   "output": "4"},
    {"input": "5*3",   "output": "15"},
    {"input": "10/2",  "output": "5"},
]

# Step 3: Build the few-shot block
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples
)

# Step 4: Wrap in a full ChatPromptTemplate
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a calculator. Only respond with the number."),
    few_shot_prompt,         # ← injects all examples as alternating Human/AI messages
    ("human", "{input}")
])

result = final_prompt.invoke({"input": "8*7"})
for msg in result.messages:
    print(f"{msg.type}: {msg.content}")
# → system: You are a calculator. Only respond with the number.
# → human:  2+2
# → ai:     4
# → human:  5*3
# → ai:     15
# → human:  10/2
# → ai:     5
# → human:  8*7
```

```
Few-Shot Structure in final prompt:
─────────────────────────────────────
  SystemMessage  ("You are a calculator...")
  HumanMessage   ("2+2")        ← example 1
  AIMessage      ("4")          ← example 1 response
  HumanMessage   ("5*3")        ← example 2
  AIMessage      ("15")         ← example 2 response
  HumanMessage   ("10/2")       ← example 3
  AIMessage      ("5")          ← example 3 response
  HumanMessage   ("8*7")        ← REAL query
─────────────────────────────────────
```

---

## 4. Internals / How It Works

### What `.invoke()` Actually Returns

```
PromptTemplate.invoke()     → StringPromptValue
                               └── .text  → str

ChatPromptTemplate.invoke() → ChatPromptValue
                               └── .messages → List[BaseMessage]
                               └── .to_messages() → same list
```

Internally, `ChatPromptTemplate` stores a list of `BaseMessagePromptTemplate` objects. When `.invoke()` is called, each template formats its variables and produces a `BaseMessage`. The result is a `ChatPromptValue` — a thin wrapper around `List[BaseMessage]` that a `ChatModel` knows how to consume.

### How Variables Are Resolved

```
Template string: "Hello {name}, you are {age} years old."

Step 1: Python's str.format_map() is called internally
Step 2: Missing variables → raises KeyError (not a silent fail)
Step 3: Extra variables → silently ignored by default
```

### `partial()` Internals

`partial()` returns a **new `PromptTemplate` instance** with some `input_variables` pre-filled into `partial_variables`. The original template is not mutated. This is important — it's safe to create multiple partials from one base template.

---

## 5. Interview Questions

**Q1: What's the difference between `PromptTemplate` and `ChatPromptTemplate`?**

> `PromptTemplate` produces a single formatted string — it's for legacy `LLM` (completion) models. `ChatPromptTemplate` produces a list of role-tagged messages (`SystemMessage`, `HumanMessage`, etc.) — it's for modern `ChatModel` APIs. In any new code, always use `ChatPromptTemplate`.

**Q2: What is `MessagesPlaceholder` and why is it essential for chatbots?**

> `MessagesPlaceholder` is a slot inside a `ChatPromptTemplate` that accepts a dynamic list of messages at runtime. It's how you inject conversation history or memory into a prompt — without it, every call to your chatbot is stateless and the model has no memory of previous turns.

**Q3: What are partial variables and when would you use them in production?**

> `partial()` pre-fills some template variables while leaving others open. In production, you use this for values that are fixed at app startup — like today's date, a user's language preference, or a deployment-specific system context — so downstream code only needs to pass the truly dynamic variables (like the user's question).

**Q4: How does few-shot prompting work in LangChain templates?**

> `FewShotChatMessagePromptTemplate` takes a list of example dicts and an `example_prompt` template, and expands them into alternating `HumanMessage`/`AIMessage` pairs. These are injected into the final `ChatPromptTemplate` before the real query. This teaches the model the expected output format without fine-tuning.

**Q5: What happens if you forget a variable when calling `.invoke()`?**

> LangChain raises a `KeyError` immediately — it calls Python's `str.format_map()` internally, which fails hard on missing keys. This is a deliberate design choice: silent failures in prompts are dangerous because the model receives a malformed prompt and produces unpredictable output.

---

## 6. Practice Problems

### Beginner — `prompttemplates_prac01_basic_chat_prompt.py`

**Task:** Build a `ChatPromptTemplate` that:
- Has a system message: `"You are a {role} expert."`
- Has a human message: `"Answer this in {style} style: {question}"`
- Invoke it with `role="Python"`, `style="bullet points"`, `question="What are decorators?"`
- Print the formatted messages list

**Expected:**
```
SystemMessage: "You are a Python expert."
HumanMessage:  "Answer this in bullet points style: What are decorators?"
```

---

### Senior — `prompttemplates_prac02_memory_fewshot_chain.py`

**Task:** Build a full chain that combines:
1. A `ChatPromptTemplate` with:
   - A system message defining a "code reviewer" persona
   - A `FewShotChatMessagePromptTemplate` with 2 examples of (bad code → review)
   - A `MessagesPlaceholder` for chat history
   - A human message for the current code snippet
2. Use `partial()` to pre-fill the system message with today's date
3. Wire it into an LCEL chain with a `ChatModel` and `StrOutputParser`
4. Call it twice, passing the first response as history in the second call

**Expected:** The second response should reference the first review, showing the model remembers context.

---

## 7. Common Mistakes & Senior Traps

- **Using `PromptTemplate` with a `ChatModel`** — it technically works (LangChain coerces it) but it loses the role structure. The model gets a single user message with no system prompt. Always match `ChatPromptTemplate` → `ChatModel`.

- **Putting `MessagesPlaceholder` after the human message** — order matters. History must come *before* the current human turn, otherwise the conversation flow is broken.

```python
# WRONG — history after current input
ChatPromptTemplate.from_messages([
    ("system", "..."),
    ("human", "{input}"),
    MessagesPlaceholder("history"),  # ← model sees current question before history
])

# RIGHT
ChatPromptTemplate.from_messages([
    ("system", "..."),
    MessagesPlaceholder("history"),  # ← history first
    ("human", "{input}"),
])
```

- **Passing `[]` vs omitting history** — if `MessagesPlaceholder` has `optional=False` (default), passing an empty list `[]` is fine. But if you forget to pass the key entirely, you get a `KeyError`. Set `optional=True` if history may genuinely be absent.

```python
MessagesPlaceholder(variable_name="history", optional=True)
```

- **Mutating a template after `partial()`** — `partial()` returns a new object. Changes to the original after calling `partial()` do NOT affect the partial copy.

- **Few-shot examples in the wrong order** — `FewShotChatMessagePromptTemplate` places examples *before* the final human message. If you manually add examples after the query, the model treats them as your expected output format, which completely breaks behavior.

- **Forgetting that `invoke()` returns a `PromptValue`, not a string** — a common mistake when debugging:

```python
# WRONG — printing the PromptValue object
result = prompt.invoke({"topic": "Python"})
print(result)   # → ChatPromptValue(messages=[...])  ← not what you want

# RIGHT — inspect the messages
print(result.messages)         # → list of message objects
print(result.to_messages())    # → same thing
```

---

Say **"next"** when you're ready for **Topic 3: LLM & Chat Model Integration**!