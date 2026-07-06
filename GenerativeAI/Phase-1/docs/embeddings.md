# Phase 1 — Topic 6: Embeddings — What?

## What is it?
An embedding is a way of representing something — a word, a sentence, an image, a user, a product — as a list of numbers (a vector). The key idea is that these numbers are not random: things that are semantically similar end up with vectors that are close together in space. Embeddings are how we translate human concepts like "meaning" and "similarity" into math that a computer can compute on. They are the backbone of almost every modern AI system.

---

## 1. The core idea — meaning as a point in space

```python
# Forget code for a second. Conceptually:

# Old way — one-hot encoding
# Each word gets a vector with a single 1 and everything else 0
# Vocabulary of 50,000 words → 50,000-dimensional vector

vocab = ["cat", "dog", "king", "queen", "Paris", "France"]

one_hot = {
    "cat":    [1, 0, 0, 0, 0, 0],
    "dog":    [0, 1, 0, 0, 0, 0],
    "king":   [0, 0, 1, 0, 0, 0],
    "queen":  [0, 0, 0, 1, 0, 0],
    "Paris":  [0, 0, 0, 0, 1, 0],
    "France": [0, 0, 0, 0, 0, 1],
}

# Problems with one-hot:
# 1. "cat" and "dog" are equally distant from each other
#    as "cat" and "France" — no sense of similarity
# 2. 50,000 dimensions for 50,000 words — huge and sparse
# 3. Adding a new word means extending every vector

# New way — dense embeddings
# Each word gets a short, dense vector (e.g. 300 or 1536 numbers)
# Similar words have similar vectors

embeddings = {
    "cat":    [0.2,  0.9,  0.1,  0.3],
    "dog":    [0.2,  0.8,  0.1,  0.4],   # close to cat!
    "king":   [0.7,  0.1,  0.9,  0.2],
    "queen":  [0.7,  0.1,  0.8,  0.6],   # close to king!
    "Paris":  [0.3,  0.2,  0.1,  0.9],
    "France": [0.3,  0.3,  0.1,  0.8],   # close to Paris!
}
# cat ↔ dog: similar animals → similar vectors
# king ↔ queen: similar royalty → similar vectors
# Paris ↔ France: capital ↔ country → similar vectors
```

---

## 2. Embeddings in practice — generating them

```python
# pip install openai sentence-transformers

# ── Option 1: OpenAI embeddings API ───────────────────────────
from openai import OpenAI

client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="The cat sat on the mat"
)

embedding = response.data[0].embedding
print(type(embedding))    # list
print(len(embedding))     # 1536  ← 1536-dimensional vector
print(embedding[:5])      # [0.0023, -0.0147, 0.0312, ...]


# Embed multiple texts at once (more efficient)
texts = [
    "I love machine learning",
    "Deep learning is amazing",
    "Pizza is delicious",
]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

embeddings = [item.embedding for item in response.data]
print(len(embeddings))      # 3  — one embedding per text
print(len(embeddings[0]))   # 1536


# ── Option 2: sentence-transformers (free, local) ─────────────
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

texts = [
    "I love machine learning",
    "Deep learning is amazing",
    "Pizza is delicious",
]

embeddings = model.encode(texts)
print(embeddings.shape)    # (3, 384)  ← 3 texts, 384 dimensions each
print(type(embeddings))    # numpy.ndarray
```

---

## 3. Measuring similarity between embeddings

```python
import numpy as np
from openai import OpenAI

client = OpenAI()

def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return np.array(response.data[0].embedding)

def cosine_similarity(a, b):
    """How similar are two vectors? Returns -1 to 1. Higher = more similar."""
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Compare sentences
sentences = [
    "I love dogs",
    "I adore puppies",        # should be VERY similar to above
    "Machine learning is fun", # should be different
    "The stock market crashed", # should be very different
]

embeddings = {s: get_embedding(s) for s in sentences}

base = "I love dogs"
for sentence in sentences[1:]:
    sim = cosine_similarity(embeddings[base], embeddings[sentence])
    print(f"'{base}' ↔ '{sentence}'")
    print(f"  similarity: {sim:.4f}\n")

# Output (approximate):
# 'I love dogs' ↔ 'I adore puppies'         → 0.91  ← very similar
# 'I love dogs' ↔ 'Machine learning is fun' → 0.21  ← different
# 'I love dogs' ↔ 'The stock market crashed'→ 0.05  ← very different
```

---

## 4. Embeddings are not just for words

```python
# Embeddings work for ANY kind of content — not just words

# ── Sentence / paragraph embeddings ───────────────────────────
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

# Whole sentences → single vector
sentence = "The transformer architecture revolutionised NLP"
embedding = model.encode(sentence)
print(embedding.shape)    # (384,)  — one vector for the whole sentence


# ── Document embeddings ────────────────────────────────────────
document = """
    Retrieval-Augmented Generation (RAG) combines a retrieval system
    with a generative model. The retriever finds relevant documents,
    and the generator uses them to produce grounded answers.
"""
doc_embedding = model.encode(document)
# One 384-dim vector representing the whole document's meaning


# ── Code embeddings ────────────────────────────────────────────
code = """
def binary_search(arr, target):
    left, right = 0, len(arr) - 1
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1
"""
# Models like "codellama" or "text-embedding-3-small" can embed code too


# ── Multimodal embeddings ──────────────────────────────────────
# CLIP (OpenAI) embeds BOTH images and text into the SAME space
# "a photo of a dog" → [0.2, 0.5, ...]
# [actual dog image] → [0.2, 0.4, ...]  ← similar vector!
# This is how image search works: embed query text, find similar image embeddings
```

---

## 5. Embedding dimensions and models

```python
# Different models produce different sized embeddings

models = {
    # OpenAI
    "text-embedding-3-small":  1536,   # fast, cheap, good quality
    "text-embedding-3-large":  3072,   # slower, pricier, better quality
    "text-embedding-ada-002":  1536,   # older, still widely used

    # Open source (sentence-transformers)
    "all-MiniLM-L6-v2":        384,    # tiny and fast, surprisingly good
    "all-mpnet-base-v2":       768,    # bigger, better quality
    "BAAI/bge-large-en-v1.5":  1024,  # strong open-source model

    # Specialized
    "text-embedding-3-small (reduced)": 512,  # can reduce dimensions
}

# Higher dimensions = more nuance captured, but:
# - More storage needed (each float = 4 bytes)
# - Slower similarity search
# - 1 million 1536-dim embeddings = ~6 GB

# You can reduce dimensions with OpenAI's newer models:
from openai import OpenAI
client = OpenAI()

response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world",
    dimensions=512    # reduce from 1536 → 512 with minimal quality loss
)
print(len(response.data[0].embedding))    # 512
```

---

## How it works under the hood

Imagine a giant map of meaning. Every concept — every word, sentence, idea — gets placed somewhere on this map. Things that mean similar things end up geographically close to each other. "Dog" and "cat" are neighbours. "King" and "queen" are neighbours. "Paris" and "France" are neighbours. But "dog" and "stock market" are miles apart. An embedding is simply the GPS coordinates of a concept on this map. The coordinates are just numbers — 384 or 1536 of them — each one a dimension of meaning we don't fully understand but the model learned through training. When you ask "is this sentence similar to that one?", you're really asking "are these two GPS coordinates close together on the meaning map?"

---

## Interview Questions They Actually Ask

**Q1: What is an embedding and why is it used instead of one-hot encoding?**
> An embedding is a dense, low-dimensional vector that represents an item's meaning. One-hot encoding gives every word an equally distant representation — "cat" and "dog" are no closer than "cat" and "aeroplane". Embeddings capture semantic relationships: similar meanings produce similar vectors. They're also far more compact — 384 numbers instead of 50,000 — making them practical for computation.

**Q2: What does it mean for two embeddings to be "similar"?**
> Similarity is measured by cosine similarity — the angle between two vectors. A cosine similarity of 1.0 means the vectors point in the same direction (identical meaning). 0 means perpendicular (unrelated). -1 means opposite. In practice, genuinely similar sentences score 0.85+, loosely related ones 0.5–0.7, and unrelated ones below 0.3. Dot product is also commonly used when vectors are normalised.

**Q3: What is the difference between word embeddings and sentence embeddings?**
> Word embeddings (like Word2Vec, GloVe) produce one vector per word — "bank" gets the same vector whether you mean a river bank or a financial bank. Sentence embeddings (like those from `sentence-transformers` or OpenAI's API) produce one vector for the entire input — they capture full context, so "I went to the bank to deposit money" and "I sat by the river bank" produce different vectors. For most modern GenAI tasks you want sentence/paragraph embeddings.

**Q4: Can the same embedding model be used for both queries and documents in a search system?**
> Yes — and this is important. In semantic search, you embed the user's query and the documents using the same model, then find documents whose embeddings are closest to the query embedding. If you use different models for queries vs documents, the vectors live in different spaces and similarity scores are meaningless. Some specialised models (like BAAI/bge) even have separate query and document modes that produce vectors in the same space but optimised for their respective roles.

**Q5: What happens to embeddings when you update your embedding model?**
> All existing embeddings must be regenerated. Embeddings from different model versions live in incompatible spaces — you cannot compare a vector from `text-embedding-ada-002` to one from `text-embedding-3-small`. This is a real production concern: if you switch models, you need to re-embed every document in your database and rebuild your vector index. This is called "embedding drift" and it's covered in Phase 4.

---

## Common mistakes & traps

- Using the wrong model for the task — an embedding model trained on general text may perform poorly on code, medical text, or multilingual content. Always check if a domain-specific model exists.
- Comparing embeddings from different models — vectors from different models live in completely different spaces. Cosine similarity between them is meaningless.
- Assuming longer embeddings are always better — a 384-dim model fine-tuned on your domain will outperform a 3072-dim general model. Dimension count is not the only quality signal.
- Not normalising vectors before dot product — cosine similarity handles magnitude differences automatically. Raw dot product does not. If you're using dot product for speed, normalise your vectors first.
- Embedding entire long documents as one vector — a single embedding averages out meaning across the whole document. Key details in specific sections get diluted. In RAG systems, you chunk documents first, then embed each chunk separately.
- Forgetting that embeddings are static snapshots — once generated, an embedding doesn't update when the world changes. If your documents change, their embeddings go stale.

---

Say **next** for Topic 7: Embeddings — How!