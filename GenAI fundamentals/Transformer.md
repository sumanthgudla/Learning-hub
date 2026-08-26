## 3. What is the Transformer architecture and why is it important?

This is one of the **most important LLM interview questions**. You don't need to explain the mathematics deeply for most AI Engineer interviews, but you should be able to explain the architecture clearly.

The Transformer was introduced in the 2017 paper **"Attention Is All You Need."** Its key idea was to build sequence models around **attention rather than recurrence**. This made training much more parallelizable and enabled the scaling that led to modern LLMs. ([arXiv][1])

---

# 1. First: What problem did Transformers solve?

Before Transformers, NLP commonly used **RNNs/LSTMs**.

Suppose we have:

> "The customer who purchased the phone yesterday wants a refund."

An RNN processes the sequence roughly like:

```text
The → customer → who → purchased → the → phone → yesterday → ...
```

One token depends on the previous step.

This creates two problems:

1. **Sequential processing** makes training difficult to parallelize.
2. It's harder to capture relationships between tokens that are far apart.

Transformers introduced **self-attention**, allowing tokens to directly interact with other tokens in the sequence. ([Google Research][2])

---

# 2. What is a Transformer?

At a high level:

```text
Text
 ↓
Tokenization
 ↓
Token Embeddings
 ↓
Positional Information
 ↓
Transformer Blocks
 ↓
Output
```

Each Transformer block contains components such as:

```text
Input
  ↓
Self-Attention
  ↓
Feed-Forward Network
  ↓
Output
```

There are also **residual connections and layer normalization** around these components. ([attentionisallyouneed.uk][3])

---

# 3. The most important part: Self-Attention

This is what you should understand really well.

Consider:

> "The bank approved the loan because **it** had sufficient funds."

What does **"it"** refer to?

The model needs to understand relationships between words.

Self-attention allows each token to look at other tokens and determine:

> **Which other tokens are important for understanding me?**

Conceptually:

```text
"The bank approved the loan because it had sufficient funds"

                           ↓
                    "it" attends to
                           ↓
                         "bank"
```

The model calculates attention weights between tokens.

So instead of processing tokens independently, the model builds contextual representations based on relationships between tokens.

---

# 4. Query, Key and Value

This is a common interview follow-up.

Self-attention uses three representations:

```text
Query (Q)
Key   (K)
Value (V)
```

A simple way to explain them:

* **Query:** What information am I looking for?
* **Key:** What information do I contain / what can I be matched on?
* **Value:** What information should actually be passed forward?

For example, when processing:

> "The animal didn't cross the street because **it** was tired."

The token **"it"** produces a query.

The model compares that query against keys from other tokens to determine which tokens are relevant.

Then the corresponding values are weighted and combined.

The standard attention equation is:

```text
Attention(Q,K,V)
    = softmax(QKᵀ / √dₖ)V
```

You **do not need to derive this** in most AI Engineer interviews. But know what it means:

```text
Q × K
 ↓
Similarity
 ↓
Softmax
 ↓
Attention weights
 ↓
Weighted combination of V
```

The original Transformer paper defines this as scaled dot-product attention. ([attentionisallyouneed.uk][3])

---

# 5. Why "Multi-Head" Attention?

Instead of having one attention mechanism, Transformers use multiple attention heads.

Think of it as multiple perspectives.

One head might learn relationships related to:

```text
Subject ↔ Verb
```

Another might focus on:

```text
Pronoun ↔ Noun
```

Another might capture:

```text
Semantic relationships
```

Another might capture:

```text
Long-range relationships
```

The exact interpretation of individual heads isn't something you should claim as fixed, but the important point is:

> **Multi-head attention allows the model to attend to information from different representation subspaces and relationships in parallel.** ([attentionisallyouneed.uk][3])

---

# 6. Why do we need positional information?

Attention itself doesn't inherently process tokens sequentially.

For example:

```text
"Dog bites man"
```

and

```text
"Man bites dog"
```

contain the same words but have completely different meanings.

The model therefore needs information about **where tokens occur in the sequence**.

The original Transformer used **positional encodings** added to token representations. ([attentionisallyouneed.uk][3])

So conceptually:

```text
Token embedding
      +
Position information
      ↓
Transformer
```

Modern architectures can use different positional mechanisms, so don't say every modern LLM necessarily uses the original sinusoidal positional encoding.

---

# 7. Feed-Forward Network

After attention, the representation goes through a feed-forward neural network.

Simplified:

```text
Attention output
      ↓
Linear layer
      ↓
Activation
      ↓
Linear layer
      ↓
Output
```

So a simplified Transformer block is:

```text
                 ┌───────────────┐
                 │ Self-Attention│
                 └───────┬───────┘
                         ↓
                    Add + Norm
                         ↓
                 ┌───────────────┐
                 │ Feed Forward  │
                 └───────┬───────┘
                         ↓
                    Add + Norm
                         ↓
                       Output
```

The original Transformer architecture uses stacked layers containing multi-head attention and position-wise feed-forward networks, with residual connections and normalization. ([attentionisallyouneed.uk][3])

---

# 8. Encoder vs Decoder

This is another important interview point.

The **original Transformer** had:

```text
Encoder → Decoder
```

The encoder processes the input, while the decoder generates the output.

But modern models use different Transformer variants.

### BERT

Primarily:

```text
Encoder-only
```

Good for understanding/representation tasks.

### GPT-style models

Primarily:

```text
Decoder-only
```

Good for autoregressive text generation.

### Original Transformer

```text
Encoder + Decoder
```

Designed for sequence-to-sequence tasks such as machine translation.

So if an interviewer asks:

> "Is a Transformer always encoder-decoder?"

Answer:

> **No. The original Transformer was encoder-decoder, but modern models can use encoder-only, decoder-only, or encoder-decoder architectures depending on the task.**

---

# 9. Why was the Transformer so important?

This is probably the **most important part of your answer**.

The Transformer removed the need for recurrence in the core architecture and made it possible to process tokens much more **in parallel during training**. The original paper demonstrated better parallelization and reduced training time compared with the recurrent approaches of the time. ([arXiv][1])

This became extremely important because large models need enormous amounts of training data and computation.

Conceptually:

```text
RNN

Token 1
   ↓
Token 2
   ↓
Token 3
   ↓
Token 4

Sequential dependency
```

versus:

```text
Transformer

Token 1 ─┐
Token 2 ─┤
Token 3 ─┼──→ Self-Attention
Token 4 ─┤
Token 5 ─┘

More parallelizable during training
```

That ability to scale training efficiently was a major reason Transformers became foundational to modern LLMs. ([Google Research][2])

---

# 10. Interview-ready answer

If the interviewer asks:

> **"What is the Transformer architecture and why is it important?"**

I would recommend you say:

> **"A Transformer is a neural network architecture introduced in the 'Attention Is All You Need' paper. Its main innovation was using self-attention instead of recurrent processing to model relationships between tokens.**
>
> **In self-attention, each token can attend to other tokens in the sequence and determine which ones are relevant to its representation. The mechanism uses Query, Key and Value vectors to calculate attention scores. Multiple attention heads allow the model to capture different relationships, and the output is passed through feed-forward layers, with residual connections and normalization. Positional information is also added so the model can understand token order.**
>
> **The original Transformer had an encoder-decoder architecture, while modern models can be encoder-only, decoder-only, or encoder-decoder. For example, GPT-style LLMs use decoder-only Transformers.**
>
> **The architecture was important because it removed the sequential bottleneck of RNNs and made training much more parallelizable. That made it much easier to scale models to huge datasets and model sizes, which ultimately enabled modern LLMs."**

### If they ask for the 10-second version:

> **"The Transformer is an architecture based primarily on self-attention. Self-attention lets every token determine which other tokens are relevant to it, while multi-head attention captures different relationships. Unlike RNNs, Transformers can process tokens much more parallelly during training, making them highly scalable. That's why Transformers became the foundation of modern LLMs."**

### Remember this flow

```text
Text
 ↓
Tokens
 ↓
Embeddings + Position
 ↓
┌────────────────────────┐
│ Transformer Block      │
│                        │
│ Self-Attention         │
│       ↓                │
│ Feed-Forward Network   │
│       ↓                │
│ Residual + Normalization│
└────────────────────────┘
 ↓
Repeated many times
 ↓
Output
```

**For your TCS AI Engineer interview, this is enough depth initially.** The next thing you should master is **"What exactly happens inside self-attention — Q, K, V with a simple example?"** That's the natural follow-up and is much more likely to be asked than deriving the entire Transformer mathematically.

[1]: https://arxiv.org/abs/1706.03762?utm_source=chatgpt.com "Attention Is All You Need"
[2]: https://research.google/pubs/attention-is-all-you-need/?utm_source=chatgpt.com "Attention is All You Need"
[3]: https://attentionisallyouneed.uk/?utm_source=chatgpt.com "Attention Is All You Need — Vaswani et al., 2017"
