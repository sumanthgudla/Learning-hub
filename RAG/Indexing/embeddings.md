# Data Conversion (Embeddings)

## Quick Revision Points

* Computers work with numbers, not text.
* **Embeddings** convert text into numerical vectors.
* Similar words/sentences have vectors closer together.
* Embeddings capture **semantic meaning**, not just keywords.
* Used heavily in RAG for retrieval/search.
* Popular embedding models:

  * Word2Vec
  * GloVe
  * FastText
  * ELMo
  * BERT

---

## What are Embeddings?

* Embeddings are **vector representations of data**.
* Text is converted into **n-dimensional vectors**.
* Similar meanings → Similar vectors.

### Example

```
Dog  → [5,7,1,...]
Bark → [6,7,2,...]

Close vectors = Similar meaning
```

**Interview Line:**
"Embeddings are numerical vector representations that capture the semantic meaning of text."

---

## Why Embeddings are Needed in RAG?

* Keyword search misses meaning.
* Embeddings enable **semantic search**.
* Retrieve documents based on meaning rather than exact words.

**Interview Line:**
"Embeddings help retrieve semantically relevant documents even when keywords don't exactly match."

---

# Embedding Models

### Word2Vec

* Developed by Google.
* One of the earliest embedding models.

### GloVe

* Developed by Stanford.
* Uses word co-occurrence statistics.

### FastText

* Developed by Facebook.
* Handles rare and misspelled words better.

### ELMo

* Context-aware embeddings.
* Improves NLP tasks like QA and sentiment analysis.

### BERT

* Transformer-based model.
* Generates contextual embeddings.
* Considers both left and right context.

**Interview Question:**
Which embedding model introduced contextual embeddings?

**Answer:**
BERT and ELMo.

---

# Popular Pretrained Embedding Models

### OpenAI

* text-embedding-ada-002 (1536 dimensions)
* text-embedding-3-small (1536 dimensions)
* text-embedding-3-large (3072 dimensions)

### Google

* Gemini text-embedding-004
* Up to 768 dimensions

### Voyage AI

* voyage-large-2
* voyage-large-2-instruct
* voyage-code-2
* voyage-law-2

### Mistral

* mistral-embed
* 1024 dimensions

### Cohere

* embed-english-v3.0
* embed-multilingual-v3.0

**Interview Line:**
"OpenAI, Google, Voyage AI, Cohere, and Mistral provide widely used pretrained embedding models."

---

# Similarity Search

## Cosine Similarity

Most common similarity metric.

### Range

* +1 → Very Similar
* 0 → Unrelated
* -1 → Opposite Meaning

**Interview Line:**
"Cosine similarity measures the angle between vectors and is the most common similarity metric in RAG."

---

## Euclidean Distance

* Measures actual distance between vectors.
* Smaller distance = More Similar.

**Interview Line:**
"Euclidean distance measures similarity based on the distance between embeddings."

---

# Embedding Use Cases

### Text Search

* Core use case in RAG.
* Find relevant document chunks.

### Clustering

* Group similar documents.

### Machine Learning

* Convert text into numerical features.

### Recommendation Systems

* Recommend similar products/content.

**Interview Line:**
"Embeddings are used for retrieval, clustering, recommendations, and machine learning tasks."

---

# Choosing an Embedding Model

### 1. Use Case

* Retrieval
* Classification
* Clustering
* Summarization

### 2. Performance

* Check MTEB Leaderboard.

### 3. Cost

* Proprietary models may incur API costs.
* Open-source models are usually free.

**Interview Line:**
"Embedding model selection depends on retrieval performance, use case, and cost."

---

## RAG Flow

```
Chunks
   ↓
Embedding Model
   ↓
Vector Embeddings
   ↓
Vector Database
```

---

## 30-Second Interview Answer

"Embeddings are numerical vector representations of text that capture semantic meaning. In RAG systems, document chunks and user queries are converted into embeddings, and similarity metrics like cosine similarity are used to retrieve the most relevant chunks. Popular embedding models include Word2Vec, BERT, OpenAI embeddings, Voyage AI, Cohere, and Mistral."

---

# Interview Questions

### Q1. What are Embeddings?

**Answer:**
Embeddings are dense vector representations of text that capture semantic meaning.

---

### Q2. Why are Embeddings used in RAG?

**Answer:**
To perform semantic search and retrieve relevant documents based on meaning rather than keywords.

---

### Q3. What is Cosine Similarity?

**Answer:**
A similarity metric that measures the angle between two vectors, ranging from -1 to 1.

---

### Q4. Difference between Keyword Search and Embedding Search?

**Answer:**
Keyword search relies on exact word matches, while embedding search uses semantic similarity.

---

### Q5. What are some popular embedding models?

**Answer:**

* Word2Vec
* GloVe
* FastText
* ELMo
* BERT
* OpenAI Embeddings
* Voyage AI
* Cohere Embeddings
* Mistral Embeddings

---

### Q6. What is the role of embeddings in RAG?

**Answer:**
They convert chunks and queries into vectors for similarity-based retrieval.

---

### Q7. What is the most commonly used similarity metric?

**Answer:**
Cosine Similarity.

---

### Q8. How do you choose an embedding model?

**Answer:**
Based on use case, retrieval performance, benchmark scores, and cost.

---

## One-Line Summary

**Embeddings convert text into vectors, enabling semantic search and retrieval in RAG systems.** 🚀
