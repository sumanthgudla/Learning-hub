# What Does a RAG System Look Like?

## Quick Interview Revision (Bullet Points)

### RAG Generation Pipeline (Online / Real-Time Flow)

* RAG = Retrieval + Augmentation + Generation.
* User asks a question.
* Retriever searches for relevant information.
* Relevant information is retrieved from the knowledge base.
* Retrieved context is added to the user's query (augmentation).
* Augmented prompt is sent to the LLM.
* LLM generates a context-aware response.
* Retriever uses **non-parametric memory** (external knowledge).
* LLM uses **parametric memory** (knowledge learned during training).
* Generation pipeline works in real time.

### RAG Indexing Pipeline (Offline Flow)

* Indexing pipeline creates the knowledge base.
* Connect to data sources.
* Extract and parse documents.
* Split large documents into chunks.
* Convert chunks into embeddings/vector format.
* Store embeddings in a vector database.
* Runs before the generation pipeline.
* Keeps the knowledge base updated.

### Important Interview Points

* RAG consists of **two pipelines**:

  * Indexing Pipeline (offline)
  * Generation Pipeline (online)
* Without indexing, retrieval is impossible.
* Knowledge base improves scalability and retrieval speed.
* Data from multiple sources should be centralized.
* Chunking improves retrieval accuracy.
* Embeddings enable semantic search.
* Vector databases store searchable embeddings.

---

# Detailed Explanation

## 1. Generation Pipeline (Runtime Flow)

Suppose a user asks:

**"Who won the 2023 Cricket World Cup?"**

The generation pipeline performs the following steps:

### Step 1: User Query

User asks a question.

```text
Who won the 2023 Cricket World Cup?
```

### Step 2: Retrieval

Retriever searches the knowledge base for relevant information.

```text
Search → Cricket World Cup 2023 winner
```

### Step 3: Fetch Relevant Information

Relevant chunk retrieved:

```text
Australia defeated India in the final and won the 2023 Cricket World Cup.
```

### Step 4: Augmentation

Original query + retrieved information are combined.

```text
Question:
Who won the 2023 Cricket World Cup?

Context:
Australia defeated India in the final and won the 2023 Cricket World Cup.
```

### Step 5: Generation

The augmented prompt is sent to the LLM.

Response:

```text
Australia won the 2023 Cricket World Cup.
```

---

## Interview Definition of Generation Pipeline

**Generation Pipeline is the online component of RAG that retrieves relevant information from the knowledge base, augments the user query with that information, and sends it to the LLM to generate a contextual response.**

---

# Parametric vs Non-Parametric Memory

### Parametric Memory

Knowledge stored inside the LLM weights.

Examples:

* GPT's trained knowledge
* Model parameters

Advantages:

* Fast
* No retrieval needed

Disadvantages:

* Cannot be updated easily
* Can become outdated

---

### Non-Parametric Memory

External knowledge source.

Examples:

* PDFs
* Websites
* Company documents
* Vector databases

Advantages:

* Easy to update
* Supports real-time information

Disadvantages:

* Requires retrieval step

---

### Interview Answer

**LLM knowledge stored in model weights is called Parametric Memory, while external knowledge retrieved during runtime is called Non-Parametric Memory. RAG combines both to generate accurate responses.**

---

# Why Not Search Directly From Source Every Time?

Imagine searching:

* PDFs
* Word files
* APIs
* Databases
* Websites

for every user question.

Problems:

* Slow
* Expensive
* Difficult to scale
* Different formats
* Duplicate information
* Inconsistent answers

Therefore we create a centralized knowledge base.

---

# Indexing Pipeline (Offline Process)

Before retrieval can happen, data must be prepared.

This preparation process is called the **Indexing Pipeline**.

---

## Step 1: Connect to Sources

Sources may include:

* Internet
* PDFs
* Word Documents
* Databases
* APIs
* Internal company documents

---

## Step 2: Extract and Parse

Extract meaningful text.

Example:

```text
PDF → Raw Text
API → JSON Data
Word File → Text
```

---

## Step 3: Split Documents

Large documents are broken into smaller chunks.

Example:

```text
100-page PDF
      ↓
500 chunks
```

Reason:

* Better retrieval accuracy
* Fits embedding model limits

---

## Step 4: Convert Into Suitable Format

Each chunk is converted into an embedding vector.

Example:

```text
Chunk
   ↓
Embedding Model
   ↓
Vector Representation
```

This enables semantic search.

---

## Step 5: Store

Store vectors in:

* Vector DB
* Vector Index

Examples:

* Pinecone
* Weaviate
* Milvus
* Chroma
* FAISS

Now the knowledge base is ready.

---

# Complete RAG Flow

```text
                INDEXING PIPELINE (Offline)

Data Sources
     ↓
Connect
     ↓
Extract
     ↓
Chunk
     ↓
Embedding
     ↓
Vector DB
     ↓
Knowledge Base


             GENERATION PIPELINE (Online)

User Query
     ↓
Retriever
     ↓
Retrieve Chunks
     ↓
Augment Prompt
     ↓
LLM
     ↓
Final Answer
```

---

# Common Interview Questions

### Basic Questions

**1. What are the main components of a RAG system?**

Answer:

* Indexing Pipeline
* Generation Pipeline
* Knowledge Base
* Retriever
* LLM

---

**2. What is the purpose of the generation pipeline?**

Answer:
To retrieve relevant information and generate context-aware responses using an LLM.

---

**3. What is the purpose of the indexing pipeline?**

Answer:
To prepare and organize external data into a searchable knowledge base.

---

### Intermediate Questions

**4. Why do we need a knowledge base in RAG?**

Answer:
A centralized knowledge base enables faster, scalable, and accurate retrieval compared to searching multiple sources in real time.

---

**5. Why is chunking important?**

Answer:
Chunking improves retrieval quality and allows embedding models to process large documents effectively.

---

**6. What is augmentation in RAG?**

Answer:
Adding retrieved context to the user's query before sending it to the LLM.

---

### Advanced Questions

**7. Why can't we directly query PDFs and databases every time?**

Answer:
It is slow, expensive, difficult to scale, and may lead to inconsistent results. Indexing solves these issues.

---

**8. Why does indexing happen before generation?**

Answer:
Because retrieval requires a searchable knowledge base. Without indexing, there is nothing to retrieve.

---

# One-Line Interview Answer

**A RAG system consists of an offline Indexing Pipeline that creates a searchable knowledge base and an online Generation Pipeline that retrieves relevant context, augments the user query, and uses an LLM to generate accurate responses.**
