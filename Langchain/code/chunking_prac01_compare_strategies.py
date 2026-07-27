'''
Task:
Take the same text (load any .txt or PDF you have).
Split it three ways:
  1. RecursiveCharacterTextSplitter — chunk_size=500, overlap=50
  2. CharacterTextSplitter         — chunk_size=500, overlap=50
  3. TokenTextSplitter             — chunk_size=128, overlap=16

Print for each strategy:
  - Number of chunks produced
  - Average chunk length (characters)
  - Shortest and longest chunk (characters)
  - First chunk content (first 100 chars)

Expected insight: all three produce different counts even with "same" size params.
'''

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_text_splitters import CharacterTextSplitter
from langchain_text_splitters import TokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader

Rag_pdf=PyPDFLoader('Learning docs/RAG Learning.pdf')
docs=Rag_pdf.load()

rcts=RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)

cts=CharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=50
)
chunks=rcts.split_documents(docs)
cts_chunks=cts.split_documents(docs)
print(len(chunks))
print(len(cts_chunks))
