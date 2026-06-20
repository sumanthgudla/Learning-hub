# Data Loading

## Quick Revision Points

* First stage of the **Indexing Pipeline**.
* Responsible for collecting data from its original source.
* Sources can be:

  * PDFs
  * Word Documents
  * CSV Files
  * HTML Pages
  * Databases
  * Cloud Storage
  * Websites
* Frameworks like LangChain provide ready-made loaders.
* Metadata plays an important role in retrieval.
* Data cleaning removes noise, duplicates, and sensitive information.

---

## 4 Sub-Steps of Data Loading

### 1. Source Connection

* Connect to data sources.
* Examples:

  * AWS S3
  * SQL/NoSQL Databases
  * Google Drive
  * GitHub
  * Websites

**Interview Line:**
"Source connectors establish connections with external data repositories."

---

### 2. Data Extraction & Parsing

* Read documents.
* Extract text from different formats.
* Parse content into a usable format.

**Interview Line:**
"Extractors and parsers convert documents into machine-readable text."

---

### 3. Metadata Management

* Add and update metadata.
* Metadata includes:

  * Source
  * Author
  * Title
  * Language
  * Creation Date

**Why Important?**

* Improves retrieval accuracy.
* Helps resolve conflicting information.

**Interview Line:**
"Metadata provides additional context about documents and improves retrieval quality."

---

### 4. Data Cleaning & Transformation

* Remove HTML tags.
* Remove special characters.
* Remove duplicates.
* Mask PII and sensitive information.
* Standardize document format.

**Interview Line:**
"Data transformation cleans and standardizes documents before further processing."

---

## LangChain in Data Loading

### What is LangChain?

* Open-source framework for LLM applications.
* Supports:

  * RAG
  * Chatbots
  * Summarization
  * Synthetic Data Generation

### Benefits

* Prebuilt document loaders.
* Integrates with:

  * OpenAI
  * Anthropic
  * Hugging Face
  * AWS
  * Google Cloud
  * Vector Databases

**Interview Line:**
"LangChain provides document loaders, transformers, and integrations that simplify RAG development."

---

## Important Components Used

### AsyncHtmlLoader

* Loads webpage content.
* Extracts HTML data from URLs.

### Html2TextTransformer

* Removes HTML tags.
* Converts webpage content into clean text.

**Interview Question:**
What is the purpose of Html2TextTransformer?

**Answer:**
It converts raw HTML into clean readable text by removing HTML tags.

---

## Flow

**Connect Source → Extract Data → Add Metadata → Clean/Transform Data**

---

## 30-Second Interview Answer

"Data Loading is the first stage of the indexing pipeline. It connects to data sources, extracts and parses documents, enriches them with metadata, and performs cleaning or transformation. Frameworks like LangChain provide loaders and transformers that simplify this process."

---

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
