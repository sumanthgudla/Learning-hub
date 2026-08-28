## Vector Databases

A **vector database is a database designed to store, index, and search vector embeddings efficiently based on similarity.**

Since you just learned embeddings, think of it this way:

> **Embeddings create the vectors. Vector databases store and search those vectors.**

### 1. Why do we need a vector database?

Suppose you have 1 million documents.

You convert them into embeddings:

```text
Document 1 → [0.12, 0.45, 0.78, ...]
Document 2 → [0.91, 0.13, 0.22, ...]
Document 3 → [0.14, 0.44, 0.76, ...]
...
Document 1,000,000 → [...]
```

Now a user asks:

> "How can I reset my password?"

You convert the question into an embedding:

```text
Query → [0.13, 0.43, 0.77, ...]
```

The vector database searches for vectors that are **most similar to the query vector**.

```text
                   User Question
                         ↓
                    Embedding
                         ↓
                    Query Vector
                         ↓
                 ┌──────────────┐
                 │ Vector DB    │
                 │              │
                 │ 1M vectors   │
                 └──────┬───────┘
                        ↓
                Similarity Search
                        ↓
                 Top 5 documents
                        ↓
                       LLM
                        ↓
                     Answer
```

---

## 2. What does a vector database actually store?

Usually, you don't store just the vector.

You store something like:

```text
ID: 123

Vector:
[0.12, 0.45, 0.78, ...]

Metadata:
{
    "document": "password_guide.pdf",
    "page": 12,
    "department": "support"
}

Text:
"To reset your password, go to..."
```

So the vector helps with **similarity search**, while metadata helps you **filter and retrieve the original content**.

---

## 3. How does similarity search work?

The database compares the query vector with stored vectors using a similarity/distance metric.

Common ones are:

### Cosine similarity

Measures the similarity based on the angle between vectors.

### Euclidean distance

Measures the straight-line distance between vectors.

### Dot product

Measures the product of corresponding vector dimensions.

The choice depends on the embedding model and database/index configuration.

---

## 4. Why can't we just use SQL?

Traditional SQL is excellent for exact/structured queries:

```sql
SELECT *
FROM customers
WHERE age > 30;
```

But semantic queries are different.

User asks:

> "I want to change my password."

The database may contain:

> "Password reset instructions"

There isn't necessarily an exact keyword match.

Vector search can identify that these pieces of text are **semantically related**.

So:

**SQL → structured/exact filtering**

**Vector search → semantic similarity**

And in real systems, you often use **both**.

---

## 5. What is RAG's relationship with vector databases?

This is one of the most important interview concepts.

### Indexing phase

```text
Documents
    ↓
Chunking
    ↓
Embedding model
    ↓
Vectors
    ↓
Vector database
```

### Query phase

```text
User question
      ↓
Embedding model
      ↓
Query vector
      ↓
Vector database
      ↓
Similarity search
      ↓
Top-K relevant chunks
      ↓
Prompt + retrieved context
      ↓
LLM
      ↓
Answer
```

This is the core of **RAG**.

---

# 6. Examples of vector databases

Some commonly used technologies are:

* **Pinecone**
* **Weaviate**
* **Milvus**
* **Qdrant**
* **Chroma**
* **FAISS** — technically a vector similarity-search library rather than a full traditional database
* **pgvector** — vector extension for PostgreSQL
* **Azure AI Search** — supports vector and hybrid search

Since you've worked with **pgvector**, an interview-friendly explanation is:

> "I've used PostgreSQL with pgvector when I wanted vector search alongside relational data."

That's actually a strong practical answer because you can explain why you chose it.

---

# 7. Vector DB vs normal DB

| Traditional DB                    | Vector DB                              |
| --------------------------------- | -------------------------------------- |
| Stores structured data            | Stores embeddings/vectors + metadata   |
| Exact/range queries               | Similarity queries                     |
| `WHERE age > 30`                  | "Find documents similar to this query" |
| B-tree/hash indexes commonly used | Vector indexes such as HNSW/IVF        |
| SQL-centric                       | Vector/similarity search-centric       |

But don't say **"vector databases replace SQL databases."**

In production, they often work together.

---

# 8. Important concept: HNSW

If the interviewer goes deeper, they may ask:

> **"How does a vector database search millions of vectors efficiently?"**

One important technique is **HNSW — Hierarchical Navigable Small World**.

Instead of comparing the query against every single vector:

```text
1 million vectors
       ↓
compare with every vector
       ↓
very expensive
```

HNSW builds a graph structure that allows the search to navigate toward likely nearest neighbors much faster.

You don't need to explain the mathematical details unless asked.

---

# Interview answer

If asked **"What is a vector database?"**, give this:

> **"A vector database is a database optimized for storing and searching high-dimensional vector embeddings. We generate embeddings from documents using an embedding model and store them along with metadata and the original content or a reference to it. When a user sends a query, we generate an embedding for that query and perform similarity search to retrieve the most relevant documents. This is commonly used in RAG systems. Examples include Pinecone, Qdrant, Milvus, Chroma, and PostgreSQL with pgvector."**

### Remember this chain

**Embedding model → Vector → Vector DB → Similarity Search → Top-K → RAG → LLM**

The next concept you should learn is **chunking**—because in a real RAG system, *how you split documents before creating embeddings* has a huge impact on retrieval quality.
