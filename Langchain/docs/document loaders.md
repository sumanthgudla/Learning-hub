# Topic 8: Document Loaders in LangChain

---

## 1. What Is It?

Document Loaders are LangChain abstractions that **ingest raw data from heterogeneous sources** (PDFs, URLs, CSVs, databases, S3, Notion, etc.) and normalize everything into a unified `Document` object — a dict-like structure containing `page_content` (string) + `metadata` (dict).

At senior level, you need to understand **not just how to call them**, but how lazy vs eager loading works, how metadata flows downstream into retrievers and filters, and how to build fault-tolerant multi-source ingestion pipelines that don't silently swallow errors.

---

## 2. Core Concepts Table

| Loader | Source | Key Args | Notes |
|---|---|---|---|
| `PyPDFLoader` | Local PDF | `file_path` | One `Document` per page |
| `PyMuPDFLoader` | Local PDF | `file_path` | Faster, richer metadata |
| `WebBaseLoader` | URL(s) | `web_path` | Uses `bs4` under the hood |
| `CSVLoader` | CSV file | `file_path`, `source_column` | One `Document` per row |
| `DirectoryLoader` | Folder | `path`, `glob`, `loader_cls` | Recurse + filter by extension |
| `UnstructuredLoader` | Mixed formats | `file_path` | Requires `unstructured` lib |
| `TextLoader` | `.txt` file | `file_path`, `encoding` | Simplest loader |
| `JSONLoader` | JSON/JSONL | `jq_schema` | Needs `jq` lib |
| `NotionDBLoader` | Notion API | `integration_token`, `database_id` | Cloud source |
| `S3FileLoader` | AWS S3 | `bucket`, `key` | Needs `boto3` |

---

## 3. Syntax & Code Examples

### 3a. Basic Usage — PDF and Web

```python
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader

# --- PDF Loader ---
loader = PyPDFLoader("data/report.pdf")
docs = loader.load()

print(len(docs))           # → N (one Document per page)
print(type(docs[0]))       # → <class 'langchain_core.documents.base.Document'>
print(docs[0].page_content[:100])  # → first 100 chars of page 1
print(docs[0].metadata)    
# → {'source': 'data/report.pdf', 'page': 0}

# --- Web Loader ---
web_loader = WebBaseLoader("https://python.org/about/")
web_docs = web_loader.load()

print(web_docs[0].metadata)
# → {'source': 'https://python.org/about/', 'title': 'About Python...', ...}
```

### 3b. CSV Loader — One Document Per Row

```python
from langchain_community.document_loaders import CSVLoader

# Each CSV row becomes a Document.
# 'source_column' tells LangChain which column to use as the "source" metadata field.
loader = CSVLoader(
    file_path="data/products.csv",
    source_column="product_id",   # metadata['source'] = value from this column
    encoding="utf-8"
)
docs = loader.load()

print(docs[0].page_content)
# → "product_id: P001\nname: Widget\nprice: 9.99\ncategory: Tools"
# Every key:value pair from the row is concatenated as text.

print(docs[0].metadata)
# → {'source': 'P001', 'row': 0}
```

### 3c. DirectoryLoader — Batch Ingestion with Glob Filtering

```python
from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader, TextLoader

# Load ALL .pdf files recursively from a folder
pdf_dir_loader = DirectoryLoader(
    path="./knowledge_base/",
    glob="**/*.pdf",         # recursive glob
    loader_cls=PyPDFLoader,  # which loader to use per file
    show_progress=True,      # tqdm progress bar
    use_multithreading=True, # parallel loading — BIG win for large dirs
    silent_errors=True       # skip corrupt files instead of crashing
)
docs = pdf_dir_loader.load()
print(f"Loaded {len(docs)} documents from PDFs")

# Load .txt files from same dir
txt_dir_loader = DirectoryLoader(
    path="./knowledge_base/",
    glob="**/*.txt",
    loader_cls=TextLoader,
    loader_kwargs={"encoding": "utf-8"}  # kwargs passed to each TextLoader
)
txt_docs = txt_dir_loader.load()
```

### 3d. Lazy Loading — Senior-Level Pattern

```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("data/massive_book.pdf")  # 500 pages

# .load() pulls everything into memory at once — BAD for large files
# .lazy_load() returns a GENERATOR — one Document at a time
for doc in loader.lazy_load():
    # process page-by-page, never holding 500 pages in RAM
    process_and_embed(doc)

# ASCII memory diagram:
#
# .load()        → [Doc1, Doc2, Doc3 ... Doc500]  ← entire list in RAM
#
# .lazy_load()   →  Doc1 → process → Doc2 → process → ...
#                   Only 1 Document in RAM at a time ✓
```

### 3e. Real-World Pattern — Multi-Source Ingestion Pipeline

```python
from langchain_community.document_loaders import (
    PyPDFLoader, WebBaseLoader, CSVLoader
)
from langchain_core.documents import Document
from typing import List
import logging

logger = logging.getLogger(__name__)

def load_from_source(source_type: str, path: str) -> List[Document]:
    """
    Fault-tolerant loader dispatcher.
    Returns [] on failure — never lets one bad source kill the pipeline.
    """
    loaders = {
        "pdf": PyPDFLoader,
        "web": WebBaseLoader,
        "csv": CSVLoader,
    }
    loader_cls = loaders.get(source_type)
    if not loader_cls:
        raise ValueError(f"Unknown source type: {source_type}")
    
    try:
        loader = loader_cls(path)
        docs = loader.load()
        # Inject a 'source_type' tag into every document's metadata
        for doc in docs:
            doc.metadata["source_type"] = source_type
        logger.info(f"Loaded {len(docs)} docs from {path}")
        return docs
    except Exception as e:
        logger.error(f"Failed to load {path}: {e}")
        return []   # ← don't crash the whole pipeline


def ingest_all(sources: list) -> List[Document]:
    """
    sources = [
        {"type": "pdf", "path": "reports/q3.pdf"},
        {"type": "web", "path": "https://example.com/faq"},
        {"type": "csv", "path": "data/faq.csv"},
    ]
    """
    all_docs = []
    for src in sources:
        docs = load_from_source(src["type"], src["path"])
        all_docs.extend(docs)
    print(f"Total documents ingested: {len(all_docs)}")
    return all_docs


# Usage
sources = [
    {"type": "pdf", "path": "data/manual.pdf"},
    {"type": "web", "path": "https://python.org/about/"},
]
all_docs = ingest_all(sources)
```

### 3f. Senior-Level — Metadata Enrichment Post-Load

```python
from langchain_community.document_loaders import PyPDFLoader
from datetime import datetime

loader = PyPDFLoader("contracts/agreement_v2.pdf")
docs = loader.load()

# Enrich metadata BEFORE passing to vector store.
# This metadata becomes filterable in retrieval later.
for doc in docs:
    doc.metadata.update({
        "doc_type": "contract",
        "department": "legal",
        "ingested_at": datetime.utcnow().isoformat(),
        "version": "v2",
        # Preserve original source but add human-readable label
        "display_name": "Service Agreement V2"
    })

# Later in retrieval:
# vectorstore.similarity_search(query, filter={"department": "legal"})
#                                              ^^^^^^^^^^^^^^^^^^^
#                   This metadata filter is only possible because we set it HERE
```

---

## 4. Internals / How It Works

```
Under the Hood — What .load() does:
─────────────────────────────────────────────────────

PyPDFLoader("report.pdf")
    │
    └─► uses `pypdf` library internally
         ├─ Opens file handle
         ├─ Iterates pages via PdfReader
         └─ For each page:
              page_content = page.extract_text()
              metadata     = {"source": file_path, "page": page_number}
              → wraps in Document(page_content=..., metadata=...)

Document object (Pydantic BaseModel):
┌─────────────────────────────────────────┐
│  Document                               │
│  ├── page_content: str   ← the text     │
│  └── metadata: dict      ← provenance   │
│       ├── source: str                   │
│       ├── page: int  (PDF)              │
│       ├── title: str (Web)             │
│       └── ... any custom fields you add │
└─────────────────────────────────────────┘

WebBaseLoader internals:
  → uses requests + BeautifulSoup4
  → strips HTML tags, extracts visible text
  → metadata includes title, description, language from <meta> tags

DirectoryLoader internals:
  → uses pathlib.Path.glob() to find files
  → spawns a ThreadPoolExecutor when use_multithreading=True
  → instantiates one loader_cls per file path
  → calls .load() on each, collects results
```

**Key design insight:** The `Document` is a thin Pydantic model — it's just a container. All the "intelligence" lives in the loaders. This is intentional: it means any loader output plugs into any downstream component (splitter, embedder, vector store) without modification.

---

## 5. Interview Questions

**Q1: What's the difference between `.load()` and `.lazy_load()`? When would you use each?**

> `.load()` is eager — it reads the entire source and returns a `List[Document]` all at once, holding everything in memory. `.lazy_load()` is a generator that yields one `Document` at a time, making it memory-efficient for large files (multi-hundred-page PDFs, giant CSVs). Use `.load()` for small files or when you need random access. Use `.lazy_load()` inside ingestion pipelines where you're processing millions of tokens and memory is a constraint.

---

**Q2: Why does `PyPDFLoader` split by page but `WebBaseLoader` returns one document? What are the implications for chunking?**

> `PyPDFLoader` naturally splits at page boundaries because PDFs have a page model — each page is a discrete unit in `pypdf`. `WebBaseLoader` fetches the full HTML, strips tags, and returns the entire visible text as a single `Document`. This matters enormously for chunking: PDF pages are already ~500-1000 tokens, a reasonable chunk size. A web page might be 10,000 tokens, so you **must** run a text splitter afterward or you'll exceed context windows and lose retrieval precision.

---

**Q3: How do you handle a directory with mixed file types — PDFs, TXTs, and CSVs — in one pipeline?**

> Use multiple `DirectoryLoader` instances with different `glob` patterns and `loader_cls` settings, then merge the results. Alternatively, use `UnstructuredLoader` which auto-detects file type but adds a heavyweight dependency. The merge approach is more predictable in production and lets you control encoding, metadata enrichment, and error handling per type independently.

---

**Q4: A loader silently fails and returns no documents. How would you debug this in production?**

> Set `silent_errors=False` on `DirectoryLoader` during development so errors surface immediately. In production, wrap each `.load()` call in try/except and log the exception with the source path. Also validate the output: if `len(docs) == 0` for a non-empty source, raise an alert. Add a metadata field like `ingested_at` so you can audit which documents actually made it into the vector store vs. what was attempted.

---

**Q5: Why is metadata enrichment after loading critical for production RAG systems?**

> Loaders inject minimal metadata — just source path and maybe a page number. But in production you need filters like "only retrieve from the legal department's docs", "only docs ingested after 2024-01-01", or "only version 2 contracts." These filters happen at the vector store retrieval layer — but the filter keys must already be **in the metadata at index time**. If you forget to enrich metadata before embedding, you can't add those filters later without re-indexing everything.

---

## 6. Practice Problems

### Beginner — Load and Inspect

**File:** `docloaders_prac01_load_and_inspect.py`

```
Task:
Load a PDF from disk using PyPDFLoader.
Print:
  1. Total number of pages/documents loaded
  2. The metadata of the first document
  3. First 200 characters of the last page's content
  
Expected output (example):
  Total docs: 12
  First doc metadata: {'source': 'data/sample.pdf', 'page': 0}
  Last page preview: "...conclusion text here..."
```

### Senior — Fault-Tolerant Multi-Source Ingestion with Metadata Enrichment

**File:** `docloaders_prac02_multisource_pipeline.py`

```
Task:
Build an ingestion function that accepts a list of source configs:
  [
    {"type": "pdf",  "path": "...", "department": "engineering"},
    {"type": "web",  "path": "...", "department": "marketing"},
    {"type": "csv",  "path": "...", "department": "sales"},
  ]

Requirements:
  1. Dispatch to the correct loader per type
  2. Enrich each document's metadata with: department, source_type, 
     ingested_at (ISO timestamp), doc_index (int, sequential across all docs)
  3. If a source fails, log the error and continue (don't crash)
  4. Return a summary dict:
     {"total": 42, "by_source_type": {"pdf": 20, "web": 10, "csv": 12},
      "failed_sources": ["bad_url.com"]}

Test it with at least 2 valid sources and 1 intentionally broken path.
```

---

## 7. Common Mistakes & Senior Traps

- **Calling `.load()` on massive files in a loop** — each call loads everything into memory. Use `.lazy_load()` or process in batches.

- **Ignoring `silent_errors=True` in production** — `DirectoryLoader` will silently skip unreadable files. You won't know unless you explicitly count expected vs. actual docs loaded.

- **Treating metadata as immutable** — Juniors assume the loader metadata is "done." Seniors know metadata is just a starting dict — you must enrich it before indexing or your retrieval filters won't work.

- **Wrong `source_column` in CSVLoader:**
```python
# WRONG — if column doesn't exist, crashes or uses row index
loader = CSVLoader("data.csv", source_column="id")  # but column is 'ID'

# RIGHT — inspect columns first
import pandas as pd
df = pd.read_csv("data.csv")
print(df.columns.tolist())  # → ['ID', 'name', 'content']
loader = CSVLoader("data.csv", source_column="ID")
```

- **WebBaseLoader returns garbage text** — it extracts all visible text including navbars, footers, cookie banners. Fix with `bs_kwargs`:
```python
# RIGHT — restrict to specific HTML tags
from bs4 import SoupStrainer
loader = WebBaseLoader(
    web_path="https://example.com/docs",
    bs_kwargs={"parse_only": SoupStrainer("article")}  # only parse <article> tags
)
```

- **Assuming one loader = one document** — `PyPDFLoader` gives N docs (one per page), `CSVLoader` gives N docs (one per row), `WebBaseLoader` gives 1 doc. If you design your chunking assuming one-doc-in, you'll get wildly different chunk counts across sources.

- **Not deduplicating on re-ingestion** — if you re-run ingestion after updating one PDF, you'll insert duplicate documents into the vector store. Track document hashes or source+page keys to detect duplicates before upsert.

---

Say **"next"** when you're ready for **Topic 9: Text Splitters & Chunking** 🚀