'''
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

Test it with at least 2 valid sources and 1 intentionally broken path.'''

from langchain_community.document_loaders import DocumentLoader, PyPDFLoader,