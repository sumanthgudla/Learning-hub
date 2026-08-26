**Tokens are the small pieces of text that an LLM processes instead of reading text directly as whole words or sentences.**

### 1. What is a token?

A token can be:

* A whole word → `hello`
* Part of a word → `unbelievable` might become `un`, `believ`, `able`
* Punctuation → `,` `.` `?`
* Sometimes spaces or other character sequences

For example:

> **"I love artificial intelligence."**

could be broken roughly into:

`I` | ` love` | ` artificial` | ` intelligence` | `.`

The exact tokenization depends on the model/tokenizer.

---

### 2. Why do we need tokens?

Computers don't naturally understand text as **meaningful words**.

An LLM ultimately operates on **numbers**.

So the process is roughly:

**Text → Tokens → Token IDs → Embeddings/vectors → Neural network → Output tokens → Text**

For example:

```text
"I love AI"

      ↓ tokenizer

["I", " love", " AI"]

      ↓ convert to IDs

[40, 1287, 5621]

      ↓

Transformer processes these numbers
```

The model learns relationships between these token representations.

---

### 3. Why not just use words?

Because language is complicated.

Consider:

```text
playing
played
player
playful
```

A tokenizer can potentially break these into shared pieces such as:

```text
play + ing
play + ed
play + er
play + ful
```

This allows the model to learn relationships between related words and also handle words it hasn't encountered exactly before.

It also helps with things like:

```text
unhappiness
internationalization
ChatGPT
```

rather than requiring every possible word to exist as a separate vocabulary entry.

---

### 4. Tokens are important because of the context window

This is **very important for interviews**.

An LLM has a maximum number of tokens it can process in one request.

For example, conceptually:

```text
Context window = 128K tokens
```

That means the model can process roughly up to 128,000 tokens of:

* your prompt
* conversation history
* documents
* retrieved RAG chunks
* tool results
* etc.

If you put too much information into the context, you can exceed the context window.

---

### 5. Tokens also affect cost

LLM APIs commonly charge based on tokens.

For example:

```text
Input:
10,000 tokens

Output:
2,000 tokens
```

You are charged based on those input and output tokens according to the provider's pricing.

So when building a production GenAI application, **reducing unnecessary tokens can reduce cost and latency.**

---

### 6. Tokens also affect RAG

This connects directly to what you've been learning.

Suppose you have a 100-page document.

You generally don't send the entire document to the LLM.

Instead:

```text
Document
   ↓
Split into chunks
   ↓
Create embeddings
   ↓
Store in vector DB
   ↓
User asks question
   ↓
Retrieve relevant chunks
   ↓
Put retrieved chunks into prompt
   ↓
LLM
```

The retrieved chunks consume **context-window tokens**.

So chunk size and the number of retrieved chunks (`top-k`) matter.

---

### Interview answer

If an interviewer asks **"What are tokens and why do we need them?"**, you can say:

> **"Tokens are the basic units of text that an LLM processes. They can represent a complete word, part of a word, punctuation, or other text sequences. We tokenize text because neural networks operate on numerical representations rather than raw text. The tokenizer converts text into token IDs, which the transformer processes to understand patterns and generate the next tokens. Tokens are also important because they determine the model's context-window usage, API cost, and latency."**

That's a **strong 45–60 second interview answer**.

One important distinction to remember:

**Token ≠ word.**
A word can be one token, multiple tokens, and sometimes tokenization can include punctuation/spacing.
