## Embeddings

**Embeddings are numerical representations of data that capture its meaning or semantic relationships.**

In GenAI, we most commonly use **text embeddings**.

### 1. Simple example

Suppose we have:

```text
"How do I reset my password?"
```

An embedding model converts it into a vector:

```text
[0.12, -0.45, 0.78, 0.21, ...]
```

In reality, the vector may contain hundreds or thousands of dimensions.

The important point is:

> **Similar meanings → similar vectors.**

For example:

```text
"How do I reset my password?"
"Where can I change my password?"
```

Their embeddings should be relatively close together.

But:

```text
"How do I cook biryani?"
```

would be much farther away.

---

## 2. Why do we need embeddings?

LLMs and traditional databases don't naturally provide a simple way to search based on **meaning**.

Consider a database containing:

```text
"Customer wants to upgrade their mobile plan."

User asks:

"I want a better phone plan."
```

A keyword search might struggle because:

```text
upgrade ≠ better
mobile plan ≈ phone plan
```

But embeddings capture the semantic relationship.

```text
User question
     ↓
Embedding model
     ↓
[0.21, 0.74, -0.12, ...]
     ↓
Vector database
     ↓
Find similar vectors
     ↓
Relevant documents
```

This is the foundation of **semantic search and RAG**.

---

# 3. Embeddings in RAG

This is particularly important for your AI Engineer interview.

Suppose you have documents:

```text
Document 1 → Password reset procedure
Document 2 → Account cancellation procedure
Document 3 → Mobile plan upgrade procedure
Document 4 → Billing procedure
```

### During indexing

You convert each document into an embedding:

```text
Document 1
    ↓
Embedding
    ↓
Vector 1

Document 2
    ↓
Embedding
    ↓
Vector 2

...
```

Store them in a vector database such as:

* pgvector
* Chroma
* Pinecone
* Azure AI Search
* FAISS

### During a query

User asks:

> "I want to upgrade my phone plan."

You generate an embedding for the question:

```text
Question
   ↓
Embedding
   ↓
Query vector
```

Then compare the query vector against document vectors.

The closest vectors are retrieved.

```text
                 Query
                   ↓
              Query Vector
                   ↓
          ┌────────┴────────┐
          ↓                 ↓
     Vector DB         Similarity
          ↓                 ↓
      Documents       Top-K results
                           ↓
                          LLM
                           ↓
                       Answer
```

That's basically the retrieval part of **RAG**.

---

# 4. How do we determine "similar"?

Usually through a **similarity metric**.

One very common metric is **cosine similarity**.

Conceptually:

```text
Vector A → "How to reset password"
Vector B → "Where can I change my password?"

              ↓

       High similarity
```

Whereas:

```text
Vector A → "How to reset password"
Vector C → "How to cook biryani"

              ↓

       Low similarity
```

Cosine similarity measures the angle between vectors rather than simply comparing the raw numbers.

---

# 5. Embeddings ≠ LLM

This distinction is important.

An **LLM** is primarily used to understand/generate text.

An **embedding model** converts information into vectors that can be compared mathematically.

```text
Embedding model
       ↓
Text → Vector
```

while:

```text
LLM
       ↓
Prompt → Generated text
```

Some model families/providers offer both capabilities, but conceptually they are different tasks.

---

# 6. What can be embedded?

Not only text.

Embeddings can represent:

* Text
* Images
* Audio
* Code
* Documents
* Products
* Users/items in recommendation systems

For example, in your **CDH/RAG use case**, you could represent:

```text
Rule name
Rule description
Rule history
Rule usage
Business context
```

as embeddings and store them in **pgvector**.

Then when someone asks:

> "Which existing rule is most similar to this new requirement?"

you can perform semantic retrieval.

---

# Interview answer

If the interviewer asks:

> **"What are embeddings?"**

A strong answer is:

> **"Embeddings are numerical vector representations of data that capture semantic meaning and relationships. An embedding model converts text or other data into a high-dimensional vector, where semantically similar inputs tend to have vectors that are close to each other. We use embeddings for semantic search, recommendation systems, clustering, and especially RAG. In a RAG system, we embed documents and store those vectors in a vector database. When a user asks a question, we embed the question, perform similarity search against the stored vectors, retrieve the most relevant chunks, and provide them to the LLM as context."**

### Remember this flow

**Text → Embedding → Vector DB → Similarity Search → Relevant Context → LLM → Answer**

That flow is **very important for your TCS AI Engineer interview**.
