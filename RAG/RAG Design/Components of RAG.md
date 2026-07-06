# Components of a RAG System

## Quick Interview Revision (Bullet Points)

### Core RAG Components

* A production-ready RAG system consists of multiple components, not just Retriever and LLM.
* Components are divided into:

  * Indexing Pipeline Components
  * Generation Pipeline Components
  * Supporting Components

---

### Indexing Pipeline Components (Offline)

* Data Loader → Connects to sources and extracts data.
* Data Splitter → Breaks documents into chunks.
* Data Conversion → Converts chunks into embeddings.
* Storage → Stores embeddings in vector databases.

---

### Generation Pipeline Components (Online)

* Retriever → Finds relevant chunks from storage.
* Prompt Management → Combines query + retrieved context.
* LLM Setup → Generates final response.

---

### Supporting Components

* Evaluation → Measures quality and accuracy.
* Monitoring → Tracks system performance.
* Caching → Stores previous responses.
* Guardrails → Prevents harmful outputs.
* Security → Protects against attacks.
* Infrastructure → Provides compute and deployment resources.
* Orchestrator → Controls the entire workflow.

---

### Important Interview Points

* Orchestrator is the brain of the RAG system.
* Indexing pipeline is offline.
* Generation pipeline is online.
* Evaluation happens before and after deployment.
* Monitoring helps detect failures in production.
* Security protects against prompt injection and data poisoning.
* Caching improves response speed and reduces cost.

---

# Detailed Explanation

## High-Level Architecture

A production-grade RAG system can be visualized as:

```text
                USER
                  |
                  v
           Orchestrator
                  |
      ------------------------
      |                      |
      v                      v
 Indexing Pipeline     Generation Pipeline
      |                      |
      v                      v
 Knowledge Base       Contextual Response
```

The orchestrator coordinates everything.

---

# 1. Indexing Pipeline Components

These components prepare data before users start asking questions.

---

## A. Data Loading Component

### Purpose

Connects to external sources and extracts information.

### Sources

* PDFs
* Word Documents
* Websites
* APIs
* Databases
* Internal Company Documents

### Responsibilities

* Connect
* Extract
* Parse

### Example

```text
PDF
 ↓
Raw Text
```

### Interview Answer

**The data loading component is responsible for connecting to external data sources and extracting usable textual information.**

---

## B. Data Splitting Component

### Purpose

Breaks large documents into smaller chunks.

### Why?

Embedding models cannot effectively process huge documents.

### Example

```text
100 Page PDF
      ↓
500 Chunks
```

### Benefits

* Better retrieval accuracy
* Faster search
* Better context matching

### Interview Answer

**Data splitting breaks large documents into smaller chunks to improve retrieval quality and embedding efficiency.**

---

## C. Data Conversion Component

### Purpose

Converts text chunks into embeddings.

### Process

```text
Chunk
  ↓
Embedding Model
  ↓
Vector
```

### Example Models

* OpenAI Embeddings
* Sentence Transformers
* BGE Models
* E5 Models

### Interview Answer

**The conversion component transforms text chunks into vector embeddings for semantic search.**

---

## D. Storage Component

### Purpose

Stores embeddings.

### Usually Implemented Using

* Pinecone
* Weaviate
* Milvus
* Chroma
* FAISS

### Interview Answer

**The storage component stores vector embeddings in a searchable knowledge base.**

---

# 2. Generation Pipeline Components

These components work during runtime when a user asks a question.

---

## A. Retriever

### Purpose

Searches the knowledge base.

### Process

```text
User Query
     ↓
Embedding
     ↓
Similarity Search
     ↓
Top K Chunks
```

### Interview Answer

**Retriever finds the most relevant chunks from the vector database using semantic similarity search.**

---

## B. Prompt Management

### Purpose

Augments user query with retrieved context.

### Example

Before:

```text
Who won the World Cup?
```

After:

```text
Question:
Who won the World Cup?

Context:
Australia defeated India...
```

### Interview Answer

**Prompt management combines user queries and retrieved information before sending them to the LLM.**

---

## C. LLM Setup

### Purpose

Generate final answer.

### Examples

* OpenAI GPT models
* Anthropic Claude
* Google Gemini
* Meta Llama

### Interview Answer

**The LLM component generates the final contextual response using the retrieved information.**

---

# 3. Supporting Components

These are critical in production systems.

---

## A. Evaluation Component

### Purpose

Measure system quality.

### Metrics

* Accuracy
* Relevance
* Faithfulness
* Hallucination Rate
* Context Precision

### Before Deployment

Tests whether the RAG system performs well.

### After Deployment

Ensures quality remains high.

### Interview Answer

**Evaluation measures the effectiveness and reliability of the RAG system using various quality metrics.**

---

## B. Monitoring Component

### Purpose

Observe system health.

### Tracks

* Latency
* Failures
* Retrieval Quality
* Token Usage
* Costs

### Interview Answer

**Monitoring continuously tracks production performance and helps identify system failures.**

---

## C. Caching

### Purpose

Store previous responses.

### Example

If 100 users ask:

```text
What is RAG?
```

The system can reuse the previous answer.

### Benefits

* Lower latency
* Reduced cost
* Better scalability

### Interview Answer

**Caching stores previously retrieved results or generated responses to improve speed and reduce cost.**

---

## D. Guardrails

### Purpose

Ensure safe AI behavior.

### Examples

Prevent:

* Toxic content
* Harmful content
* Policy violations
* Sensitive data leaks

### Interview Answer

**Guardrails enforce business rules and safety policies on LLM outputs.**

---

## E. Security

### Purpose

Protect the RAG system.

### Common Threats

#### Prompt Injection

```text
Ignore previous instructions...
```

#### Data Poisoning

Malicious data inserted into knowledge base.

#### Unauthorized Access

Sensitive information leakage.

### Interview Answer

**Security protects the RAG system from attacks such as prompt injection, data poisoning, and unauthorized access.**

---

## F. Infrastructure

### Purpose

Provides underlying resources.

### Includes

* Cloud Services
* GPUs
* Databases
* APIs
* Networking

### Examples

* Amazon Web Services
* Microsoft Azure
* Google Cloud

### Interview Answer

**Infrastructure provides the compute, storage, and networking resources required to run the RAG system.**

---

# Orchestrator (Most Important Interview Topic)

## What is an Orchestrator?

The orchestrator is the central controller of the entire RAG system.

### Responsibilities

* Manage workflow
* Control execution order
* Connect all components
* Handle failures
* Route requests

### Example Flow

```text
User Query
     ↓
Retriever
     ↓
Prompt Builder
     ↓
LLM
     ↓
Guardrails
     ↓
Response
```

The orchestrator coordinates every step.

### Examples

* LangChain
* LangGraph
* LlamaIndex Workflows
* Custom Python Pipelines

### Interview Answer

**The orchestrator acts as the brain of the RAG system, coordinating interactions between retrieval, prompting, generation, evaluation, and monitoring components.**

---

# Frequently Asked Interview Questions

### Q1. What are the major components of a production-ready RAG system?

**Answer:**

* Data Loading
* Data Splitting
* Data Conversion
* Storage
* Retriever
* Prompt Management
* LLM
* Evaluation
* Monitoring
* Guardrails
* Security
* Infrastructure
* Orchestrator

---

### Q2. Which components belong to the Indexing Pipeline?

**Answer:**

* Data Loader
* Data Splitter
* Data Conversion
* Storage

---

### Q3. Which components belong to the Generation Pipeline?

**Answer:**

* Retriever
* Prompt Management
* LLM

---

### Q4. Why is the orchestrator important?

**Answer:**
It coordinates all RAG components and ensures the workflow executes correctly.

---

### Q5. Why do production RAG systems need monitoring?

**Answer:**
To track latency, failures, retrieval quality, costs, and overall system health.

---

# One-Line Interview Answer

**A production-ready RAG system consists of indexing components (loading, chunking, embedding, storage), generation components (retriever, prompt manager, LLM), and supporting components such as orchestration, evaluation, monitoring, caching, guardrails, security, and infrastructure.**
