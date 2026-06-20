# Interview Questions

### Q1. What is Data Loading in RAG?

**Answer:**
Data Loading is the process of collecting, extracting, and preparing data from various sources to build the knowledge base.

---

### Q2. What are the four sub-steps of Data Loading?

**Answer:**

1. Source Connection
2. Data Extraction & Parsing
3. Metadata Management
4. Data Cleaning & Transformation

---

### Q3. What is Metadata?

**Answer:**
Metadata is information about data such as source, author, title, language, and creation date.

---

### Q4. Why is Metadata important in RAG?

**Answer:**
It improves retrieval quality and provides additional context for filtering and ranking documents.

---

### Q5. What is the role of AsyncHtmlLoader?

**Answer:**
It loads webpage content from URLs.

---

### Q6. Why do we clean data before chunking?

**Answer:**
To remove noise, duplicates, HTML tags, and sensitive information that can negatively affect retrieval quality.

---

### Q7. What types of sources can Data Loaders connect to?

**Answer:**
Websites, cloud storage, databases, GitHub, Google Drive, AWS S3, PDFs, and document repositories.

---

## One-Line Summary

**Data Loading = Connect → Extract → Add Metadata → Clean Data before Chunking.** 🚀


# Interview Questions

### Q1. What is Chunking?

**Answer:**
Chunking is the process of breaking large documents into smaller manageable pieces for retrieval and LLM processing.

---

### Q2. Why is Chunking required in RAG?

**Answer:**

* Context window limitations
* Better retrieval accuracy
* Faster search
* Reduces lost-in-the-middle problem

---

### Q3. What is Chunk Overlap?

**Answer:**
Chunk overlap is the repeated content between adjacent chunks to preserve context continuity.

---

### Q4. What is the Lost-in-the-Middle Problem?

**Answer:**
LLMs may fail to attend to important information located in the middle of long contexts.

---

### Q5. What is Recursive Chunking?

**Answer:**
A chunking method that uses multiple separators recursively to create appropriately sized chunks.

---

### Q6. What is Token-Based Chunking?

**Answer:**
Chunking where chunk size and overlap are measured using tokens instead of characters.

---

### Q7. What is Specialized Chunking?

**Answer:**
Chunking based on document structure such as HTML headers, JSON objects, Markdown sections, or code functions.

---

### Q8. What is Semantic Chunking?

**Answer:**
A chunking method that groups text based on semantic similarity using embeddings.

---

### Q9. Which chunking strategy is best?

**Answer:**
There is no universal best method. The choice depends on data type, query complexity, use case, and embedding model.

---

## One-Line Summary

**Chunking = Split large documents into meaningful chunks with overlap for efficient retrieval and better LLM performance.** 🚀



Interview Questions
Q1. What are Embeddings?
Answer:
Embeddings are dense vector representations of text that capture semantic meaning.
Q2. Why are Embeddings used in RAG?
Answer:
To perform semantic search and retrieve relevant documents based on meaning rather than keywords.
Q3. What is Cosine Similarity?
Answer:
A similarity metric that measures the angle between two vectors, ranging from -1 to 1.
Q4. Difference between Keyword Search and Embedding Search?
Answer:
Keyword search relies on exact word matches, while embedding search uses semantic similarity.
Q5. What are some popular embedding models?
Answer:
Word2Vec
GloVe
FastText
ELMo
BERT
OpenAI Embeddings
Voyage AI
Cohere Embeddings
Mistral Embeddings
Q6. What is the role of embeddings in RAG?
Answer:
They convert chunks and queries into vectors for similarity-based retrieval.
Q7. What is the most commonly used similarity metric?
Answer:
Cosine Similarity.
Q8. How do you choose an embedding model?
Answer:
Based on use case, retrieval performance, benchmark scores, and cost.
One-Line Summary
Embeddings convert text into vectors, enabling semantic search and retrieval in RAG systems. 🚀