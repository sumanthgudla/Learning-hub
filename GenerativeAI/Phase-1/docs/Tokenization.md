# Phase 1 — Topic 2: Tokenization

## What is it?
Tokenization is the process of splitting raw text into smaller chunks called **tokens** — the basic units a language model actually sees and processes. A token is not always a word; it can be a whole word, a piece of a word, a single character, or even punctuation. Every LLM has a tokenizer that converts your text into a sequence of tokens before anything else happens.

---

## 1. Why not just split on spaces?

Splitting on spaces seems obvious but breaks down fast.

```python
text = "I'm running unhappiness tokenization."

# Naive space split
print(text.split())
# ['I'm', 'running', 'unhappiness', 'tokenization.']

# Problems:
# 1. "I'm" should probably be ["I", "'m"]
# 2. "unhappiness" → a model that never saw it is stuck
# 3. "tokenization." has a period glued to it
# 4. Every new word = new vocabulary entry → vocabulary explodes
# 5. Rare words and typos never seen in training → unknown token

# Word-level tokenization breaks on out-of-vocabulary words
vocab = {"I", "am", "running", "fast"}
tokens = ["unhappiness"]   # ← not in vocab → UNK (unknown)
# Model sees <UNK> and loses all meaning
```

---

## 2. Subword tokenization — the real solution

Modern tokenizers split words into meaningful subpieces. This keeps vocabulary small while handling any word ever — even made-up ones.

```python
# Conceptual illustration (not real tokenizer code yet)

# "unhappiness" gets split into known subwords
"unhappiness"  →  ["un", "happiness"]       # or
"unhappiness"  →  ["un", "happy", "ness"]   # depending on tokenizer

# "tokenization" gets split too
"tokenization"  →  ["token", "ization"]

# Common words stay whole
"run"    →  ["run"]
"the"    →  ["the"]
"I"      →  ["I"]

# New/rare words still work
"ChatGPT"  →  ["Chat", "G", "PT"]
"GPT-4"    →  ["G", "PT", "-", "4"]
"sumanth"  →  ["su", "man", "th"]    # never seen before, still handled
```

---

## 3. The three main tokenization methods

```python
# ── 1. Word-level ──────────────────────────────────────────────
# Split on whitespace/punctuation. One token = one word.
# Vocab: 50,000–100,000 words
# Problem: out-of-vocabulary words become <UNK>

text = "I love tokenization"
tokens = text.split()          # ['I', 'love', 'tokenization']


# ── 2. Character-level ─────────────────────────────────────────
# One token = one character.
# Vocab: tiny (~256 chars)
# Problem: sequences get very long; "hello" = 5 tokens
#          model has to learn that h-e-l-l-o = a word

tokens = list("hello")         # ['h', 'e', 'l', 'l', 'o']


# ── 3. Subword-level (what all modern LLMs use) ────────────────
# Split into frequent subword pieces.
# Vocab: ~32,000–100,000 subwords
# Best of both worlds: compact + handles unknown words

# BPE (Byte Pair Encoding) — used by GPT-2, GPT-3, GPT-4, Llama
# WordPiece — used by BERT (adds ## prefix to subwords)
# SentencePiece — used by T5, Llama 2, Mistral (language-agnostic)

# WordPiece example (BERT style):
"unhappiness"  →  ["un", "##happy", "##ness"]
#                        ↑ ## means "continues previous token"

# BPE example (GPT style):
"unhappiness"  →  ["un", "happiness"]
```

---

## 4. Using a real tokenizer

```python
# pip install transformers tiktoken

# ── tiktoken (OpenAI's tokenizer — used by GPT-3.5, GPT-4) ────
import tiktoken

enc = tiktoken.get_encoding("cl100k_base")   # GPT-4's encoding

text = "Hello, I am learning tokenization!"

tokens = enc.encode(text)
print(tokens)
# [9906, 11, 358, 1097, 6975, 4037, 2065, 0]

print(len(tokens))   # 8 tokens

# Decode back to text
print(enc.decode(tokens))   # "Hello, I am learning tokenization!"

# See what each token looks like as text
for token_id in tokens:
    print(repr(enc.decode([token_id])))
# 'Hello'  ','  ' I'  ' am'  ' learning'  ' token'  'ization'  '!'
#  ↑ notice the space is PART of the token: ' am' not 'am'


# ── HuggingFace tokenizer (works for any model) ────────────────
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("gpt2")

text = "Tokenization is fun!"
result = tokenizer(text)

print(result["input_ids"])      # [30642, 1634, 318, 1257, 0]
print(result["attention_mask"]) # [1, 1, 1, 1, 1]  ← 1 = real token

# Convert IDs back to tokens (strings)
tokens = tokenizer.convert_ids_to_tokens(result["input_ids"])
print(tokens)   # ['Token', 'ization', 'Ġis', 'Ġfun', '!']
#                                        ↑ Ġ = space in GPT-2
```

---

## 5. How BPE (Byte Pair Encoding) works — the idea

```python
# BPE builds vocabulary by merging the most frequent pairs of characters

# Start: every character is its own token
corpus = ["low", "lower", "newest", "widest"]
# Vocabulary: {l, o, w, e, r, n, s, t, i, d}

# Step 1: count all adjacent pairs
# ('l','o') appears 2x  ← most frequent
# ('o','w') appears 2x
# etc.

# Step 2: merge the most frequent pair → "lo" becomes one token
# Now vocab includes: {lo, w, e, r, n, s, t, i, d}

# Step 3: repeat — next most frequent pair gets merged
# ('lo','w') → "low"

# After many merges you get subwords like:
# "low", "lower", "est", "new", "wide" etc.
# These are the tokens in your final vocabulary

# Key insight: common words stay whole, rare words split into pieces
# "the" → always one token (very frequent)
# "photosynthesis" → ["photo", "syn", "thesis"] or similar
```

---

## 6. Tokens ≠ words — the gotcha everyone hits

```python
import tiktoken
enc = tiktoken.get_encoding("cl100k_base")

def count_tokens(text):
    return len(enc.encode(text))

# Surprises:
print(count_tokens("Hello"))          # 1 token
print(count_tokens("hello"))          # 1 token
print(count_tokens("HELLO"))          # 1 token  (same word, same token)

print(count_tokens("ChatGPT"))        # 3 tokens: Chat + G + PT
print(count_tokens("tokenization"))   # 2 tokens: token + ization
print(count_tokens("Sumanth"))        # 3 tokens: Su + man + th

# Numbers are expensive!
print(count_tokens("1000000"))        # 3 tokens: 100 + 000 + 0 ... varies
print(count_tokens("one million"))    # 2 tokens

# Non-English is more expensive (more bytes per character)
print(count_tokens("hello"))          # 1 token
print(count_tokens("नमस्ते"))          # 7–9 tokens  (Hindi)
print(count_tokens("你好"))            # 3–4 tokens  (Chinese)

# Whitespace matters
print(count_tokens("dog"))            # 1 token
print(count_tokens(" dog"))           # 1 token (space is baked IN: ' dog')
print(count_tokens("  dog"))          # 2 tokens (extra space = its own token)
```

---

## How it works under the hood

Think of BPE like building a language from Lego bricks. You start with individual letters (smallest bricks). Then you notice certain combinations appear constantly together — "th", "ing", "tion" — so you create a single brick for each. You keep doing this, creating bigger and bigger bricks for the most common combinations, until you have a set of ~50,000 bricks that can build almost any word efficiently. Common words like "the" get their own single brick. Rare words like "photosynthesis" get assembled from 2–3 bricks. A word the model has never seen — "sumanth" — still gets assembled from bricks it knows. The tokenizer is just the instruction manual that tells you which bricks to use for any given text.

---

## Interview Questions They Actually Ask

**Q1: What is a token and why don't LLMs just use words?**
> A token is the atomic unit of text a model processes — typically a subword chunk. Models don't use whole words because word-level vocabularies explode in size, can't handle new/rare words, and don't work across languages. Subword tokenization keeps the vocabulary manageable (~50K tokens) while still being able to represent any text, including words never seen during training.

**Q2: What is BPE and how does it work?**
> Byte Pair Encoding builds a vocabulary by starting with individual characters and repeatedly merging the most frequently co-occurring pair into a single token. After thousands of merges you end up with a vocabulary of common subwords. Common words become single tokens; rare words get split into recognizable pieces.

**Q3: Why does the same English text use fewer tokens than equivalent text in Hindi or Chinese?**
> English characters map to ASCII bytes 1:1, so one character is often one token. Non-Latin scripts need 2–4 bytes per character in UTF-8, and since BPE operates on bytes, each character may become multiple tokens. This means non-English languages are "more expensive" — they consume more of the model's context window for the same amount of information.

**Q4: What is the relationship between tokens and the context window?**
> A model's context window (e.g. 128K tokens for GPT-4) is measured in tokens, not words or characters. If your text tokenizes to more tokens than the context window allows, the model can't process it. Roughly, 1 token ≈ 0.75 English words, so 128K tokens ≈ ~96,000 words. But this ratio changes for code, numbers, and non-English text.

**Q5: What does the `attention_mask` returned by a HuggingFace tokenizer mean?**
> It's a list of 1s and 0s — 1 means "real token, pay attention to this", 0 means "padding token, ignore this". When you batch multiple sequences of different lengths together, shorter sequences get padded with dummy tokens to match the longest one. The attention mask tells the model which tokens are real and which are just padding.

---

## Common mistakes & traps

- Assuming 1 token = 1 word when estimating API costs or context usage — use `tiktoken` to count exactly.
- Not accounting for special tokens — tokenizers add `[CLS]`, `[SEP]`, `<s>`, `</s>` etc. around your text. These count toward the context window too.
- Forgetting that numbers tokenize badly — "2024" might be 1–3 tokens depending on the tokenizer. Tables of numbers are very token-heavy.
- Using the wrong tokenizer for the wrong model — GPT-4 uses `cl100k_base`, GPT-2 uses a different one, BERT uses WordPiece. Mixing them gives wrong token counts.
- Thinking the tokenizer "understands" the splits — it's purely statistical, not linguistic. "therapist" might tokenize as ["the", "rapist"] because "the" is very frequent. The model learns from context what it actually means.
- Comparing token counts across languages to judge model "intelligence" — a model isn't smarter in English, it's just cheaper per idea in English due to tokenization efficiency.

---

Say **next** for Topic 3: Vocabulary & Token IDs!