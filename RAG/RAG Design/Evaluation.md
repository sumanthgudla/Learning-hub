
# Evaluation and Monitoring

## Quick Revision Points

* Evaluation measures the quality of a RAG system.
* Helps determine if the system is accurate and reducing hallucinations.
* Used before deployment and for continuous monitoring.
* Common metrics:

  * Relevance
  * Precision
  * Recall
* TruEra proposes a **RAG Evaluation Triad**:

  * Context Relevance
  * Groundedness
  * Answer Relevance
* Ground Truth datasets are used as benchmarks for evaluation.
* Continuous monitoring helps identify weak areas and improve performance.

---

## RAG Evaluation Triad

### 1. Context Relevance

**Question:**
Is the retrieved context relevant to the user's query?

**Why Important?**

* Poor retrieval leads to poor answers.
* Even the best LLM cannot generate a good response from irrelevant context.

**Interview Line:**
"Context relevance measures whether the retriever fetched the right information for the user query."

---

### 2. Groundedness

**Question:**
Is the generated answer faithful to the retrieved context?

**Why Important?**

* Detects hallucinations.
* Ensures answers are based on retrieved information.

**Interview Line:**
"Groundedness measures whether the LLM's response is supported by the retrieved context."

---

### 3. Answer Relevance

**Question:**
Is the final answer relevant to the user's original query?

**Why Important?**

* Ensures the response actually addresses the user's question.

**Interview Line:**
"Answer relevance measures how well the generated response answers the user's query."

---

## Ground Truth Dataset

* A manually curated dataset containing correct answers.
* Used as a benchmark for evaluating RAG performance.
* Helps compare generated responses against expected outputs.

**Interview Line:**
"Ground truth datasets provide reference answers for measuring RAG system accuracy."

---

## Continuous Monitoring

* Monitor system performance in production.
* Track metrics over time.
* Collect user feedback.
* Identify queries where the system struggles.
* Improve retrieval and prompting strategies.

**Interview Line:**
"Continuous monitoring helps detect performance issues and improve the RAG system over time."

---

## Important Flow

**User Query → Retrieved Context → Generated Answer**

Evaluation Checks:

1. Query ↔ Context → Context Relevance
2. Context ↔ Answer → Groundedness
3. Query ↔ Answer → Answer Relevance

---

## 30-Second Interview Answer

"Evaluation and monitoring help measure the effectiveness of a RAG system. The TruEra RAG Evaluation Triad evaluates three aspects: Context Relevance (retrieval quality), Groundedness (whether answers are based on retrieved context), and Answer Relevance (whether the answer addresses the user's query). Continuous monitoring and user feedback help improve system performance over time."

---

# Interview Questions

### Q1. Why do we need evaluation in RAG?

**Answer:**
To measure retrieval quality, detect hallucinations, and assess overall system performance.

---

### Q2. What are the three components of the RAG Evaluation Triad?

**Answer:**

1. Context Relevance
2. Groundedness
3. Answer Relevance

---

### Q3. What is Context Relevance?

**Answer:**
It measures whether the retrieved documents are relevant to the user's query.

---

### Q4. What is Groundedness?

**Answer:**
It measures whether the generated answer is supported by the retrieved context and not hallucinated.

---

### Q5. What is Answer Relevance?

**Answer:**
It measures how well the generated answer addresses the user's original question.

---

### Q6. What is a Ground Truth Dataset?

**Answer:**
A benchmark dataset containing correct answers used to evaluate system accuracy.

---

### Q7. How can hallucinations be detected in RAG?

**Answer:**
By measuring Groundedness and checking whether responses are supported by retrieved context.

---

## One-Line Summary

**RAG Evaluation = Context Relevance + Groundedness + Answer Relevance.** 🚀
