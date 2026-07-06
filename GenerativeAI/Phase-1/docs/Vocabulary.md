# Phase 1 — Topic 3: Vocabulary & Token IDs

## What is it?
A vocabulary is the complete list of all tokens a model knows — every subword, word, punctuation mark, and special symbol it was trained with. Each token in the vocabulary gets assigned a unique integer called a Token ID. When you send text to a model, the tokenizer converts your text into a sequence of these IDs — that list of numbers is literally what the model receives as input.

---

## 1. What a vocabulary looks like

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

# Total vocabulary size
print(tokenizer.vocab_size)   # 50257

# Peek at the vocabulary — it's a dict of {token_string: token_id}
vocab = tokenizer.get_vocab()
print(type(vocab))            # <class 'dict'>
print(len(vocab))             # 50257

# Look up specific tokens
print(vocab["hello"])         # 31373
print(vocab["the"])           # 1169
print(vocab["Ġthe"])          # 262   ← ' the' with leading space
print(vocab["token"])         # 30001
print(vocab["ization"])       # 1634

# Reverse lookup — ID to token string
id_to_token = {v: k for k, v in vocab.items()}
print(id_to_token[262])       # 'Ġthe'
print(id_to_token[50256])     # '<|endoftext|>'  ← special token
```

---

## 2. Text → Token IDs → back to Text

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "I love learning about tokenization"

# Step 1: text → token IDs
input_ids = tokenizer.encode(text)
print(input_ids)
# [40, 1842, 4673, 546, 11241, 1634]

# Step 2: token IDs → back to text
decoded = tokenizer.decode(input_ids)
print(decoded)
# "I love learning about tokenization"

# See the token strings (not IDs) for each piece
tokens = tokenizer.convert_ids_to_tokens(input_ids)
print(tokens)
# ['I', 'Ġlove', 'Ġlearning', 'Ġabout', 'Ġtoken', 'Ġization']
#    ↑ Ġ = space baked into the token

# See ID for each token
for token, id_ in zip(tokens, input_ids):
    print(f"{id_:>6}  →  {repr(token)}")
#    40  →  'I'
#  1842  →  'Ġlove'
#  4673  →  'Ġlearning'
#   546  →  'Ġabout'
# 11241  →  'Ġtoken'
#  1634  →  'Ġization'
```

---

## 3. Special tokens — the non-obvious ones

Every tokenizer adds special tokens beyond normal subwords. These have reserved IDs and carry specific meaning.

```python
from transformers import AutoTokenizer

# ── GPT-2 special tokens ───────────────────────────────────────
tokenizer = AutoTokenizer.from_pretrained("gpt2")
print(tokenizer.eos_token)        # '<|endoftext|>'
print(tokenizer.eos_token_id)     # 50256  ← always the last ID


# ── BERT special tokens ────────────────────────────────────────
bert = AutoTokenizer.from_pretrained("bert-base-uncased")
print(bert.cls_token)    # '[CLS]'   ← always first token
print(bert.sep_token)    # '[SEP]'   ← separates sentences
print(bert.pad_token)    # '[PAD]'   ← fills empty space in batches
print(bert.unk_token)    # '[UNK]'   ← unknown/out-of-vocab token
print(bert.mask_token)   # '[MASK]'  ← for masked language modeling

# BERT adds [CLS] and [SEP] automatically
encoded = bert("Hello world", return_tensors="pt")
tokens = bert.convert_ids_to_tokens(encoded["input_ids"][0])
print(tokens)
# ['[CLS]', 'hello', 'world', '[SEP]']
#      ↑ always added at start and end — they count toward context!


# ── Chat models have even more ─────────────────────────────────
# Llama 2 / Mistral instruction format
# <s>[INST] user message here [/INST] assistant reply </s>
#  ↑                                                   ↑
#  start of sequence token                    end of sequence token
# These are baked into the chat template — the tokenizer handles it
```

---

## 4. Vocabulary size matters

```python
# Different models, different vocab sizes
# GPT-2:            50,257 tokens
# GPT-3 / GPT-4:   100,256 tokens  (cl100k_base)
# BERT:              30,522 tokens
# Llama 2:           32,000 tokens
# Llama 3:          128,256 tokens  ← bigger = fewer tokens per text
# Mistral:           32,000 tokens

import tiktoken

# GPT-4 tokenizer
enc = tiktoken.get_encoding("cl100k_base")
print(enc.n_vocab)    # 100277

# Larger vocab = fewer tokens needed for the same text
# = more efficient use of context window
# But larger vocab = bigger embedding table the model must learn

text = "photosynthesis is a fascinating biological process"

# Smaller vocab (more splits):
# ["photo", "syn", "thesis", " is", " a", " fas", "cin", "ating", ...]
# ↑ 10+ tokens

# Larger vocab (fewer splits):
# ["photosynthesis", " is", " a", " fascinating", " biological", " process"]
# ↑ 6 tokens  — same text, fewer tokens used
```

---

## 5. What the model actually receives

```python
import torch
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")
tokenizer.pad_token = tokenizer.eos_token   # GPT-2 has no pad token by default

texts = [
    "Hello",
    "Hello world",
    "Hello world, how are you?"
]

# Tokenize a batch — sequences padded to same length
batch = tokenizer(
    texts,
    padding=True,        # pad shorter sequences
    truncation=True,     # cut sequences longer than max_length
    max_length=10,
    return_tensors="pt"  # return PyTorch tensors
)

print(batch["input_ids"])
# tensor([[31373, 50256, 50256, 50256, 50256],   ← "Hello" + 4 pads
#         [31373,   995, 50256, 50256, 50256],   ← "Hello world" + 3 pads
#         [31373,   995,    11,   703,   389]])  ← "Hello world, how are"

print(batch["attention_mask"])
# tensor([[1, 0, 0, 0, 0],    ← only first token is real
#         [1, 1, 0, 0, 0],    ← first two are real
#         [1, 1, 1, 1, 1]])   ← all real (truncated to 5)

# This tensor of integers is EXACTLY what goes into the model
# The model's first layer (embedding table) converts each ID
# into a vector of floats — that's the next topic
```

---

## How it works under the hood

Think of the vocabulary as a giant dictionary hanging on the wall — 50,000 entries, each with a unique number. The tokenizer is the person who looks at your sentence, breaks it into the right chunks, then looks each chunk up in the dictionary and writes down its number. That list of numbers is passed to the model. The model never sees letters — only numbers. Its very first operation is to look each number up in an "embedding table" (like another dictionary) and swap it for a long list of floats. From that point on, it's pure math.

---

## Interview Questions They Actually Ask

**Q1: What is a vocabulary in the context of LLMs, and how big is it typically?**
> A vocabulary is the fixed set of all tokens a model knows, each mapped to a unique integer ID. Sizes range from ~30K (BERT, Llama 2) to ~100K (GPT-4) to ~128K (Llama 3). A larger vocabulary means fewer tokens per piece of text — more efficient use of the context window — but requires a larger embedding table that the model must learn during training.

**Q2: What happens when a token is not in the vocabulary?**
> With subword tokenizers like BPE, this essentially never happens — any text can be broken into known subwords, and as a last resort individual bytes are always in the vocabulary. Older word-level tokenizers had an `[UNK]` (unknown) token for out-of-vocabulary words, which caused the model to lose all meaning for that word.

**Q3: What are special tokens and why do they matter?**
> Special tokens are reserved entries in the vocabulary that signal structure to the model — `[CLS]` marks the start of a BERT input, `[SEP]` separates segments, `[PAD]` fills batches to equal length, `<|endoftext|>` tells GPT the document is over. They matter because they consume context window space, affect model behavior, and must match what the model was trained with — using the wrong special tokens can silently degrade performance.

**Q4: Why does padding exist and what is the attention mask?**
> GPUs process text in batches, and batches must be rectangular (all same length). Shorter sequences get padded with a special `[PAD]` token to match the longest sequence. The attention mask is a 0/1 array telling the model which tokens are real (1) and which are just padding (0) — so the model ignores padding positions and doesn't let them influence its computations.

**Q5: If two words look similar — like "token" and "Token" — do they have the same ID?**
> Usually not. Most tokenizers are case-sensitive, so "token" and "Token" map to different IDs. Some models (like BERT base uncased) lowercase everything first so they do map to the same ID. GPT-style models are case-sensitive — "Token", "token", and "TOKEN" are typically three different token IDs with three different embedding vectors.

---

## Common mistakes & traps

- Forgetting special tokens count toward the context window — if you're near the limit, `[CLS]` and `[SEP]` can push you over.
- Using `tokenizer.encode()` vs `tokenizer()` — they behave slightly differently. `tokenizer()` returns a dict with `input_ids`, `attention_mask`, etc. `tokenizer.encode()` returns just the list of IDs. In production always use `tokenizer()` so you get the attention mask too.
- Assuming vocabulary size = number of unique words in training data — it's not. The vocabulary is built by the BPE algorithm on character/byte frequencies, not word frequencies.
- Not setting a `pad_token` for GPT-style models — they don't have one by default. The common fix is `tokenizer.pad_token = tokenizer.eos_token` but be aware this means padding and end-of-text share an ID.
- Hard-coding token IDs — `50256` is the EOS token for GPT-2 but not for other models. Always use `tokenizer.eos_token_id`, never magic numbers.
- Thinking `tokenizer.decode()` always gives back the exact original string — it usually does, but padding tokens, special tokens, and byte-level differences can cause minor changes.

---

Say **next** for Topic 4: Context Window!