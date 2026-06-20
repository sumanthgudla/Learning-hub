# Indexing Pipeline (Interview Notes)

## Quick Bullet Points (Revision Before Interview)

* Indexing Pipeline is an **offline/asynchronous process** in RAG.
* It builds and updates the **knowledge base** before users ask questions.
* Not executed during real-time query processing.
* Consists of **4 main components**:

  1. Data Loading
  2. Data Splitting (Chunking)
  3. Data Conversion (Embeddings)
  4. Data Storage (Vector Database)
* Data Loading extracts data from multiple sources like PDFs, Docs, JSON, HTML, CMS, Data Lakes, etc.
* Data Splitting breaks large documents into smaller chunks.
* Data Conversion transforms text into numerical vectors called embeddings.
* Data Storage stores embeddings in Vector Databases for efficient retrieval.
* Metadata management, data cleaning, preprocessing, and masking confidential information happen during data loading.

---

# Detailed Interview Explanation

## What is the Indexing Pipeline in RAG?

The **Indexing Pipeline** is responsible for creating the knowledge base used by the retrieval system.

Since processing huge amounts of data every time a user asks a question would be slow and expensive, RAG systems prepare the data in advance through the indexing pipeline.

It is called an **offline (or asynchronous) pipeline** because it runs separately from the user query flow and updates the knowledge base periodically.

---

## 1. Data Loading

### Purpose

To collect and prepare data from various external sources.

### Responsibilities

* Connect to external systems.
* Read files from different locations.
* Extract text from documents.
* Parse content into a usable format.
* Clean and preprocess data.

### Common Data Sources

* File Systems
* Data Lakes
* Content Management Systems (CMS)
* Databases
* Cloud Storage

### Supported File Types

* PDF
* DOC/DOCX
* JSON
* HTML
* Text Files

### Additional Tasks

* Remove irrelevant content.
* Ensure data consistency.
* Mask confidential or sensitive information.
* Extract and store metadata.

### Interview Answer

> The Data Loading component connects to external data sources, extracts information from different file formats, preprocesses the data, removes noise, handles metadata, and prepares the content for further processing.

---

## 2. Data Splitting (Chunking)

### Purpose

Large documents cannot be efficiently searched or embedded as a whole.

Therefore, documents are divided into smaller pieces called **chunks**.

### Why Chunking is Needed

* Improves retrieval accuracy.
* Reduces embedding size.
* Helps retrieve only relevant portions of documents.
* Fits within LLM context limits.

### Example

Original Document:

```
100-page company policy document
```

After Chunking:

```
Chunk 1
Chunk 2
Chunk 3
...
Chunk N
```

### Interview Answer

> Data Splitting, also known as chunking, breaks large documents into smaller manageable chunks, improving retrieval quality and enabling efficient embedding generation.

---

## 3. Data Conversion (Embeddings)

### Purpose

Computers cannot directly perform semantic search on text.

Text must first be converted into numerical representations called **embeddings**.

### What are Embeddings?

Embeddings are dense vector representations that capture the meaning of text.

Example:

```
"Artificial Intelligence"
      ↓
[0.12, -0.45, 0.87, ...]
```

### Benefits

* Semantic similarity search.
* Better retrieval than keyword matching.
* Captures context and meaning.

### Interview Answer

> The Data Conversion component transforms text chunks into embeddings, which are numerical vectors that represent semantic meaning and enable efficient similarity search.

---

## 4. Data Storage

### Purpose

Store embeddings permanently for future retrieval.

### Where are Embeddings Stored?

Specialized databases called **Vector Databases**.

### Popular Vector Databases

* Pinecone
* Weaviate
* Milvus
* Chroma
* FAISS

### Why Vector DBs?

They are optimized for:

* Similarity Search
* Nearest Neighbor Search
* Fast Retrieval
* Scalability

### Interview Answer

> The Data Storage component stores embeddings in vector databases, which are optimized for fast similarity search and retrieval during the generation phase.

---

# End-to-End Flow (Very Important Interview Question)

### How does the Indexing Pipeline work?

```
Raw Documents
      ↓
Data Loading
      ↓
Data Splitting (Chunking)
      ↓
Embedding Generation
      ↓
Vector Database Storage
      ↓
Knowledge Base Ready
```

### 30-Second Interview Answer

> The Indexing Pipeline is an offline process that prepares the knowledge base for a RAG system. It first loads data from various sources, then splits large documents into smaller chunks, converts those chunks into embeddings, and finally stores the embeddings in a vector database. This prepared knowledge base is later used by the retrieval system to fetch relevant information during user queries.

---

## Interview Questions

### Q1: Why is the indexing pipeline offline?

**Answer:**
Because processing documents every time a user asks a question would be slow and expensive. Therefore, data is preprocessed and stored beforehand.

---

### Q2: What are the four components of the indexing pipeline?

**Answer:**

1. Data Loading
2. Data Splitting (Chunking)
3. Data Conversion (Embeddings)
4. Data Storage (Vector DB)

---

### Q3: Why do we perform chunking?

**Answer:**
Chunking improves retrieval accuracy, reduces embedding size, and helps fit information within LLM context windows.

---

### Q4: Why are embeddings required?

**Answer:**
Embeddings convert text into numerical vectors, enabling semantic similarity search and retrieval.

---

### Q5: Why do we use vector databases?

**Answer:**
Vector databases are optimized for storing embeddings and performing fast similarity searches required in RAG systems.

---

### One-Line Summary

**Indexing Pipeline = Load Data → Chunk Data → Generate Embeddings → Store in Vector DB → Create Knowledge Base.** 🚀
