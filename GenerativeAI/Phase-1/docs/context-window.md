# Phase 1 — Topic 4: Context Window

## What is it?
The context window is the maximum number of tokens a model can see at one time. Everything the model knows about your conversation — your instructions, the chat history, any documents you've pasted in, and the response it's generating — must fit inside this window. If it doesn't fit, the oldest content gets cut off and the model simply cannot see it. It's the model's entire working memory for that request.

---

## 1. The basics

```python
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")  # GPT-4's tokenizer

def count_tokens(text):
    return len(enc.encode(text))

# Context window limits by model (as of 2024)
limits = {
    "GPT-3.5-turbo":  16_385,
    "GPT-4":         128_000,
    "GPT-4o":        128_000,
    "Claude 3.5":    200_000,
    "Llama 3 8B":    128_000,
    "Gemini 1.5 Pro": 1_000_000,
}

# Rough real-world estimates
# 1 token ≈ 0.75 English words
# 1,000 tokens ≈ 750 words ≈ 1.5 pages of text
# 128,000 tokens ≈ ~300 pages / a short novel
# 1,000,000 tokens ≈ ~750,000 words ≈ several books

# Check if your text fits
system_prompt = "You are a helpful assistant."
user_message = "Summarize this document: " + "word " * 5000

total_tokens = count_tokens(system_prompt) + count_tokens(user_message)
model_limit = 16_385

if total_tokens > model_limit:
    print(f"Too long! {total_tokens} tokens > {model_limit} limit")
    print(f"Over by {total_tokens - model_limit} tokens")
else:
    print(f"Fine. {total_tokens} / {model_limit} tokens used")
```

---

## 2. What counts toward the context window

Everything in a single API call is counted together — there is no free space.

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

# A typical chat API call looks like this:
messages = [
    {
        "role": "system",
        "content": "You are a helpful coding assistant."
    },
    {
        "role": "user",
        "content": "What is a Python decorator?"
    },
    {
        "role": "assistant",
        "content": "A decorator is a function that wraps another function..."
    },
    {
        "role": "user",
        "content": "Can you show me an example?"
    }
]

# ALL of this eats context:
# 1. System prompt
# 2. Every past user message
# 3. Every past assistant message
# 4. The new user message
# 5. The response the model is about to generate (output tokens)
# 6. Special formatting tokens added between messages

total = sum(len(enc.encode(m["content"])) for m in messages)
print(f"Messages use ~{total} tokens")
# Add ~4 tokens per message for role/formatting overhead
total_with_overhead = total + (4 * len(messages)) + 2
print(f"With overhead: ~{total_with_overhead} tokens")

# The model's OUTPUT also counts
# If context limit = 128K and your input = 127K tokens,
# the model can only generate ~1K tokens of response
```

---

## 3. What happens when you exceed the limit

```python
# There are two strategies when content is too long:

# ── Strategy 1: Truncation (cut it off) ───────────────────────
def truncate_to_limit(text, max_tokens=4000, model="cl100k_base"):
    enc = tiktoken.get_encoding(model)
    tokens = enc.encode(text)

    if len(tokens) <= max_tokens:
        return text   # already fits

    # Cut from the END (keep the beginning)
    truncated_tokens = tokens[:max_tokens]
    return enc.decode(truncated_tokens)

long_doc = "word " * 10000   # 10,000 tokens
short_doc = truncate_to_limit(long_doc, max_tokens=4000)
print(len(enc.encode(short_doc)))   # 4000


# ── Strategy 2: Sliding window (keep recent context) ──────────
def sliding_window_messages(messages, max_tokens=4000):
    """Keep system prompt + as many recent messages as fit."""
    system = [m for m in messages if m["role"] == "system"]
    convo  = [m for m in messages if m["role"] != "system"]

    system_tokens = sum(len(enc.encode(m["content"])) for m in system)
    budget = max_tokens - system_tokens

    # Add messages from the end (most recent) until we run out of budget
    kept = []
    for msg in reversed(convo):
        msg_tokens = len(enc.encode(msg["content"])) + 4
        if budget - msg_tokens < 0:
            break
        kept.insert(0, msg)
        budget -= msg_tokens

    return system + kept

# This is roughly what ChatGPT does when conversations get long
```

---

## 4. Input tokens vs output tokens

```python
import openai

client = openai.OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "Explain what a context window is in 3 sentences."}
    ],
    max_tokens=200    # ← cap how many tokens the model can OUTPUT
)

# Usage breakdown
usage = response.usage
print(f"Input tokens:  {usage.prompt_tokens}")       # tokens you sent
print(f"Output tokens: {usage.completion_tokens}")   # tokens model generated
print(f"Total tokens:  {usage.total_tokens}")        # sum of both

# Why this matters for cost:
# OpenAI charges separately for input and output tokens
# Output tokens are usually 2–3x more expensive than input tokens
# GPT-4o (June 2024): $5 per 1M input, $15 per 1M output

cost_per_1m_input  = 5.00
cost_per_1m_output = 15.00

input_cost  = (usage.prompt_tokens / 1_000_000) * cost_per_1m_input
output_cost = (usage.completion_tokens / 1_000_000) * cost_per_1m_output
total_cost  = input_cost + output_cost

print(f"Cost: ${total_cost:.6f}")
```

---

## 5. Context window in practice — the real gotchas

```python
# ── Gotcha 1: Long system prompts eat into user space ──────────
system_prompt = open("my_big_instructions.txt").read()
system_tokens = count_tokens(system_prompt)
print(f"System prompt: {system_tokens} tokens")
# If this is 10,000 tokens, your user only has 118,000 left

# ── Gotcha 2: RAG chunks must fit ─────────────────────────────
# When you retrieve 5 documents to inject into the prompt:
retrieved_docs = ["doc1 content...", "doc2 content...", ...]
doc_tokens = sum(count_tokens(d) for d in retrieved_docs)
print(f"Retrieved docs: {doc_tokens} tokens")
# This must leave room for: system prompt + user question + answer

# ── Gotcha 3: "Lost in the middle" problem ────────────────────
# Research shows LLMs perform WORST on information placed
# in the MIDDLE of a long context window
# They remember the START (primacy) and END (recency) best
# Put the most important info at the beginning or end

# ── Gotcha 4: Bigger context ≠ better attention ───────────────
# A 1M token context window does NOT mean the model
# attends equally to all 1M tokens
# Performance degrades on very long contexts
# Use RAG instead of stuffing everything in context

# ── Gotcha 5: reserve space for output ────────────────────────
MAX_CONTEXT = 128_000
RESERVED_FOR_OUTPUT = 2_000   # tokens you want the model to generate

input_budget = MAX_CONTEXT - RESERVED_FOR_OUTPUT   # 126,000
# Never fill the full context or model has no room to respond
```

---

## How it works under the hood

Think of the context window like a whiteboard. The model can only see what's written on that whiteboard right now — nothing more. Every time you send a message, the entire conversation gets written on the whiteboard from scratch. The model reads the whole thing left to right, then writes its response at the end. When the whiteboard is full, you have to erase the oldest writing to make room. The model has no memory of anything that was erased — it's completely gone. This is fundamentally different from human memory, which stores things long-term. Every single API call starts with a blank whiteboard and everything must be re-written on it.

---

## Interview Questions They Actually Ask

**Q1: What is a context window and what counts toward it?**
> The context window is the maximum number of tokens a model can process in a single call. Everything counts: the system prompt, the entire conversation history, any documents injected into the prompt, the user's current message, and the model's output. All of it must fit within the limit — nothing is free.

**Q2: What is the difference between input tokens and output tokens?**
> Input tokens are everything you send to the model — the prompt, history, documents. Output tokens are what the model generates in response. Both count toward the context window limit. They're also priced separately by API providers, with output tokens typically costing 2–3x more than input tokens.

**Q3: Does a larger context window mean better performance on long documents?**
> Not necessarily. Research shows LLMs suffer from the "lost in the middle" problem — they pay most attention to content at the very beginning and very end of the context, and often miss information buried in the middle. A 1M token context window doesn't mean uniform attention across all 1M tokens. RAG (retrieval) is often better than stuffing a huge document into the context.

**Q4: What happens when a conversation exceeds the context window?**
> The oldest messages get truncated — dropped to make room for new ones. The model has no memory of what was cut. Different systems handle this differently: some cut from the beginning (lose oldest messages), some summarize old messages first, some use external memory stores. The model itself is unaware anything was lost.

**Q5: Why do you need to reserve output tokens when building prompts?**
> The context window is shared between input and output. If your input fills 127,999 of a 128,000 token window, the model can only generate 1 token of response. In production you always reserve a budget for the expected output length — typically 500–2,000 tokens — and ensure your input stays within `max_context - output_budget`.

---

## Common mistakes & traps

- Assuming the context window resets between turns — it doesn't. Each API call sends the full history every time. The "memory" in a chat app is just re-sending old messages each turn.
- Forgetting to account for the system prompt in your token budget — a detailed system prompt can easily be 500–2,000 tokens.
- Not setting `max_tokens` on API calls — without it, the model might try to generate a very long response, unexpectedly consuming your budget and increasing cost.
- Thinking "128K context = can process a 128K token document" — you also need tokens for the system prompt, the question, and the answer. Your actual document budget is smaller.
- Putting the most critical information in the middle of a long prompt — due to the "lost in the middle" problem, put key instructions at the top or bottom.
- Measuring document length in words or characters to check if it fits — always measure in tokens using `tiktoken` or your model's tokenizer.

---

Say **next** for Topic 5: Positional Encoding!