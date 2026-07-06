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


Q1. What is the Generation Pipeline?
Answer:
The generation pipeline is the real-time component of RAG that retrieves relevant information and generates responses for user queries.
Q2. What are the components of the Generation Pipeline?
Answer:
Retriever
Prompt Management
LLM
Q3. Which is the most critical component in a RAG system?
Answer:
The Retriever, because retrieval quality directly affects response quality.
Q4. What is Augmentation in RAG?
Answer:
Augmentation is the process of combining retrieved context with the user's query before sending it to the LLM.
Q5. Why is Prompt Management important?
Answer:
Because the quality and structure of the prompt significantly influence the quality of the generated response.
Q6. What role does the LLM play in RAG?
Answer:
The LLM generates the final answer using the user query and retrieved context.
Q7. Can a RAG system use multiple LLMs?
Answer:
Yes. Different LLMs can be used for different tasks such as generation, summarization, classification, or reranking.
Q8. What causes latency in the Generation Pipeline?
Answer:
Retrieval operations and LLM inference are the primary contributors to latency.
One-Line Summary
Generation Pipeline = Retrieve Relevant Data → Augment Prompt → Generate Response using LLM. 🚀


Q1. Why do we need evaluation in RAG?
Answer:
To measure retrieval quality, detect hallucinations, and assess overall system performance.
Q2. What are the three components of the RAG Evaluation Triad?
Answer:
Context Relevance
Groundedness
Answer Relevance
Q3. What is Context Relevance?
Answer:
It measures whether the retrieved documents are relevant to the user's query.
Q4. What is Groundedness?
Answer:
It measures whether the generated answer is supported by the retrieved context and not hallucinated.
Q5. What is Answer Relevance?
Answer:
It measures how well the generated answer addresses the user's original question.
Q6. What is a Ground Truth Dataset?
Answer:
A benchmark dataset containing correct answers used to evaluate system accuracy.
Q7. How can hallucinations be detected in RAG?
Answer:
By measuring Groundedness and checking whether responses are supported by retrieved context.
One-Line Summary
RAG Evaluation = Context Relevance + Groundedness + Answer Relevance. 🚀



Q1. What is Semantic Caching?
Answer:
Semantic caching stores LLM responses and returns them for semantically similar queries instead of running the entire RAG pipeline again.
Q2. How does caching help RAG systems?
Answer:
It reduces latency, inference cost, and load on the LLM.
Q3. What are Guardrails?
Answer:
Guardrails are predefined rules that restrict model outputs to comply with business, regulatory, and ethical requirements.
Q4. Why are Guardrails important?
Answer:
They prevent harmful, unsafe, or policy-violating responses.
Q5. What are common security threats in RAG systems?
Answer:
Prompt Injection
Data Poisoning
Sensitive Information Disclosure
Unauthorized Access
Q6. What is Prompt Injection?
Answer:
An attack where malicious instructions are inserted into prompts to manipulate the model's behavior.
Q7. What is Data Poisoning?
Answer:
Injecting malicious or incorrect data into the knowledge base to influence model outputs.
Q8. What is RAGOps?
Answer:
RAGOps is the operational framework for managing, monitoring, evaluating, and maintaining production RAG systems.
Q9. What are key RAGOps components?
Answer:
Logging
Tracing
Monitoring
Evaluation
Model Versioning
Feedback Systems
One-Line Summary
Production RAG = Caching + Guardrails + Security + RAGOps for performance, safety, and maintainability. 🚀











