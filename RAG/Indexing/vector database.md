# Storage (Vector Databases)

## Quick Revision Points

* Final stage of the **Indexing Pipeline**.
* Stores embeddings for future retrieval.
* Uses **Vector Databases (Vector DBs)**.
* Optimized for:

  * Similarity Search
  * Semantic Search
  * High-dimensional vectors
* Uses metrics like:

  * Cosine Similarity
  * Euclidean Distance

---

## What is a Vector Database?

**Answer:**
A vector database is a specialized database designed to store, index, and retrieve vector embeddings efficiently.

**Interview Line:**
"Vector databases store embeddings and perform fast semantic similarity searches."

---

## Why Vector Databases?

Traditional databases store:

* SQL → Rows & Columns
* NoSQL → Documents
* Graph DB → Nodes & Relationships

Vector DB stores:

* Embeddings (high-dimensional vectors)

**Interview Line:**
"Vector databases are optimized for storing and searching high-dimensional embedding vectors."

---

# Types of Vector Databases

### 1. Vector Index Libraries

* Lightweight
* Search only
* No database features

Examples:

* FAISS
* Annoy
* ScaNN
* NMSLIB

**Interview Line:**
"FAISS is a vector index library focused on efficient similarity search."

---

### 2. Specialized Vector Databases

Examples:

* Pinecone
* Chroma
* Milvus
* Qdrant
* Weaviate

Features:

* Security
* Scalability
* Filtering
* Metadata Support

---

### 3. Search Platforms with Vector Search

Examples:

* Elasticsearch
* OpenSearch
* Apache Solr

---

### 4. SQL Databases with Vector Support

Examples:

* PostgreSQL (pgvector)
* Azure SQL
* Cloud SQL

---

### 5. NoSQL Databases with Vector Support

Examples:

* MongoDB

---

### 6. Graph Databases with Vector Support

Examples:

* Neo4j

---

# Similarity Search

### How Retrieval Works?

```text
User Query
      ↓
Embedding
      ↓
Vector DB
      ↓
Similarity Search
      ↓
Top Matching Chunks
```

**Interview Line:**
"Vector databases retrieve the nearest embeddings using similarity search."

---

# FAISS

### What is FAISS?

* Facebook AI Similarity Search.
* Most popular vector index library.
* Open Source.
* High-performance similarity search.

**Interview Line:**
"FAISS is a lightweight vector indexing library widely used for semantic search and retrieval."

---

# How to Choose a Vector Database?

### 1. Accuracy vs Speed

* Faster search vs better retrieval quality.

### 2. Flexibility vs Performance

* More features may reduce speed.

### 3. Local vs Cloud

* Local → Faster access.
* Cloud → Scalability and security.

### 4. API vs Direct Access

* Managed APIs vs self-hosted control.

### 5. Cost

* Managed solutions cost more.
* Self-hosted solutions require maintenance.

**Interview Line:**
"Vector database selection depends on performance, scalability, flexibility, and cost requirements."

---

## 30-Second Interview Answer

"Vector databases are specialized databases used to store and retrieve embeddings efficiently. They support similarity search using metrics such as cosine similarity and Euclidean distance. Popular options include FAISS, Pinecone, ChromaDB, Milvus, Qdrant, and Weaviate. They form the storage layer of a RAG system and enable fast retrieval of relevant document chunks."

---

# Interview Questions

### Q1. What is a Vector Database?

**Answer:**
A database optimized for storing, indexing, and retrieving embedding vectors.

---

### Q2. Why do we need Vector Databases in RAG?

**Answer:**
To perform fast semantic similarity search on embeddings.

---

### Q3. What is stored inside a Vector Database?

**Answer:**
Embeddings (vector representations of documents/chunks) along with metadata.

---

### Q4. What is Similarity Search?

**Answer:**
Finding vectors closest to the query vector based on similarity metrics.

---

### Q5. Which similarity metrics are commonly used?

**Answer:**

* Cosine Similarity
* Euclidean Distance

---

### Q6. What is FAISS?

**Answer:**
Facebook AI Similarity Search, a popular vector indexing library for nearest-neighbor search.

---

### Q7. Difference between FAISS and Pinecone?

**Answer:**

* FAISS → Local vector index library.
* Pinecone → Managed cloud vector database.

---

### Q8. Name some popular Vector Databases.

**Answer:**

* FAISS
* Pinecone
* ChromaDB
* Milvus
* Qdrant
* Weaviate

---

### Q9. What factors influence Vector DB selection?

**Answer:**

* Accuracy
* Speed
* Scalability
* Cost
* Cloud vs Local deployment

---

### Q10. Where does a Vector Database fit in RAG?

**Answer:**
After embeddings are generated, they are stored in a vector database for retrieval during query processing.

---

## One-Line Summary

**Vector Database = Stores embeddings and performs fast similarity search for RAG retrieval.** 🚀
