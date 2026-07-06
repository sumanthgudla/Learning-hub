# Data Splitting (Chunking)

## Quick Revision Points

* **Chunking** = Breaking large documents into smaller manageable chunks.
* Required because LLMs cannot process very large documents efficiently.
* Three main benefits:

  * Context Window Limitation
  * Lost-in-the-Middle Problem
  * Faster Retrieval/Search
* Chunking usually includes **overlap** to maintain context.
* Process:

  * Split → Merge → Overlap

---

## Why Chunking is Needed?

### 1. Context Window Limitation

* LLMs have a maximum token limit.
* Large documents may exceed this limit.
* Chunking helps fit data into LLM context windows.

**Interview Line:**
"Chunking helps overcome LLM context window limitations."

---

### 2. Lost-in-the-Middle Problem

* LLMs often miss important information located in the middle of long prompts.
* Smaller chunks improve retrieval of relevant information.

**Interview Line:**
"Chunking reduces the lost-in-the-middle problem by retrieving only relevant sections."

---

### 3. Easier Search

* Searching smaller chunks is faster and more accurate than searching entire documents.

**Interview Line:**
"Chunking improves retrieval efficiency and search accuracy."

---

## Chunking Process

1. Split document into smaller units (sentences/paragraphs).
2. Merge units into chunks of desired size.
3. Add overlap between chunks.

**Flow:**
Document → Split → Merge → Overlap → Chunks

---

# Chunking Methods

## 1. Fixed-Size Chunking

* Most common method.
* Predefined chunk size and overlap.
* Simple and easy to implement.

### A. Character-Based Chunking

* Split using characters like:

  * `\n`
  * `.`
  * `*`

**Interview Line:**
"Character chunking splits text based on specific characters and fixed chunk sizes."

---

### B. Recursive Character Chunking

* Uses multiple separators.
* Tries larger separators first, then smaller ones.
* Recommended for generic text.

**Interview Line:**
"Recursive chunking creates better-sized chunks using multiple separators."

---

### C. Token-Based Chunking

* Chunk size measured in tokens instead of characters.
* More aligned with how LLMs process text.

**Interview Line:**
"Token-based chunking uses token counts, making it more suitable for LLMs."

---

## 2. Specialized Chunking (Adaptive Chunking)

* Uses document structure.
* Preserves natural hierarchy.

Examples:

* HTML → Headers & Sections
* Markdown → Headings
* JSON → Objects
* Code → Classes & Functions

Tools:

* HTMLHeaderTextSplitter
* MarkdownHeaderTextSplitter
* RecursiveJsonSplitter

**Interview Line:**
"Specialized chunking leverages document structure to preserve meaningful content."

---

## 3. Semantic Chunking

* Groups content based on meaning.
* Uses embeddings to measure similarity.
* No fixed chunk size.
* Experimental but powerful.

**Interview Line:**
"Semantic chunking creates chunks based on semantic similarity rather than fixed size."

---

## Chunking Comparison

| Method      | Based On            | Best For               |
| ----------- | ------------------- | ---------------------- |
| Character   | Characters          | Simple text            |
| Recursive   | Multiple separators | Generic documents      |
| Token       | Tokens              | LLM applications       |
| Specialized | Document structure  | HTML, JSON, Code       |
| Semantic    | Meaning             | High-quality retrieval |

---

# Choosing a Chunking Strategy

### 1. Nature of Content

* HTML → Specialized Chunking
* Code → Code-aware Chunking
* Reports → Recursive Chunking

### 2. Query Complexity

* Short queries → Smaller chunks
* Complex queries → Larger chunks

### 3. Use Case

* QA Systems → Smaller chunks
* Summarization → Larger chunks

### 4. Embedding Model

* Some embedding models perform better with specific chunk sizes.

---

## 30-Second Interview Answer

"Chunking is the process of splitting large documents into smaller chunks for efficient retrieval and LLM processing. It helps overcome context window limitations, improves retrieval accuracy, and reduces the lost-in-the-middle problem. Common methods include fixed-size chunking, recursive chunking, token-based chunking, specialized chunking, and semantic chunking."

---

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
