## Semantic Search

**Semantic search means searching based on the meaning or intent of the query rather than just matching exact keywords.**

This is one of the core concepts behind **RAG**.

### 1. Keyword search vs Semantic search

Suppose your database contains:

> **"Customers can change their password from the account settings page."**

User asks:

> **"Where can I update my login credentials?"**

### Keyword search

It looks for matching words:

```text
update ❌
login ❌
credentials ❌
password ❌
```

It may fail because the exact words aren't present.

### Semantic search

It converts both pieces of text into embeddings:

```text
Document
   ↓
Embedding → [0.21, 0.73, 0.15, ...]

Query
   ↓
Embedding → [0.19, 0.71, 0.18, ...]
```

The vectors are close because the **meaning is similar**.

Therefore:

```text
Query
  ↓
Embedding
  ↓
Vector similarity search
  ↓
Relevant document
```

---

## 2. How semantic search works

The basic flow is:

```text
Documents
    ↓
Chunk documents
    ↓
Embedding model
    ↓
Vectors
    ↓
Vector database
```

Then when the user searches:

```text
User Query
    ↓
Embedding model
    ↓
Query vector
    ↓
Vector DB
    ↓
Similarity search
    ↓
Top-K relevant chunks
```

For example:

```text
Query:
"I want to upgrade my mobile plan"

        ↓

Semantic search

        ↓

Result:
"Customers interested in premium plans can
upgrade through the My Account section."
```

Even though **"upgrade"** and **"premium plans"** may not exactly match the user's wording, the system understands the semantic relationship through embeddings.

---

## 3. Semantic search is not the same as the LLM

This distinction is important.

The **embedding model** converts text into vectors.

The **vector database** searches those vectors.

The **LLM** generates the final response.

```text
                 User Question
                      ↓
               Embedding Model
                      ↓
                 Query Vector
                      ↓
                Vector Database
                      ↓
                Semantic Search
                      ↓
             Relevant Documents
                      ↓
                     LLM
                      ↓
                   Answer
```

---

## 4. Semantic search in RAG

Imagine you have 100,000 company documents.

The user asks:

> "What is our refund policy for damaged products?"

You don't want to send all 100,000 documents to the LLM.

Semantic search finds the relevant pieces:

```text
100,000 documents
        ↓
Semantic search
        ↓
Top 5 relevant chunks
        ↓
LLM
        ↓
Answer
```

This is why semantic search is so important for **RAG**.

---

## 5. Hybrid search

In real production systems, you often combine:

**Keyword search + semantic search**

This is called **hybrid search**.

For example:

> "What is the policy for product ID ABC123?"

Keyword search is very good at finding the exact identifier:

```text
ABC123
```

Semantic search is good at understanding:

```text
policy
product
requirements
```

Combining both can give better retrieval.

---

# Interview answer

If asked **"What is semantic search?"**, say:

> **"Semantic search retrieves information based on the meaning and intent of the query rather than relying only on exact keyword matches. Typically, we generate embeddings for both the query and documents, store the document embeddings in a vector database, and then perform similarity search to retrieve the most relevant chunks. Semantic search is commonly used in RAG systems. In production, we can also combine semantic search with keyword search using hybrid search to improve retrieval accuracy."**

### Remember the difference

**Keyword search:**

> "Do these words match?"

**Semantic search:**

> "Do these meanings match?"

**Hybrid search:**

> "Can I use both?"
