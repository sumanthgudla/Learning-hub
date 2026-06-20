# Vector Database Selection Guide (Senior AI Engineer Interview Answer)

## Key Decision Axes

### 1. Scale of Vectors

| Scale | Recommendation | Reason |
|---------|---------------|---------|
| **Under 1M vectors** | Chroma, pgvector | Any DB works. Optimize for operational simplicity rather than performance. |
| **1M – 100M vectors** | Pinecone, Qdrant | Indexing strategy becomes important. HNSW tuning starts to matter. |
| **100M+ vectors** | Milvus, Pinecone | Battle-tested at very large scale. Built for distributed indexing and search. |

---

### 2. Latency Requirement

| Requirement | Recommendation |     |
|------------|---------------|---------|
| **Sub-millisecond** | Redis VSS | Entire index must live in RAM. No disk I/O can be tolerated. |
| **Single-digit milliseconds** | Pinecone, Qdrant | Managed vector databases can achieve this using HNSW at moderate scale. |
| **Batch / Async workloads** | FAISS, Milvus | Latency is less important than throughput and cost optimization. |

---

### 3. Infrastructure Ownership

| Situation | Recommendation | Reason |
|-----------|---------------|---------|
| **No new infrastructure** | pgvector, Redis VSS | Extend existing systems and reduce operational overhead. |
| **Managed SaaS** | Pinecone | Pay for operational simplicity and managed scaling. |
| **Self-hosted OSS** | Qdrant, Milvus, Weaviate | Full control over infrastructure, deployment, and data residency. |

---

### 4. Query Type

| Query Pattern | Recommendation | Reason |
|--------------|---------------|---------|
| **Vector + Metadata Filter** | Qdrant, Pinecone | Efficient pre-filtering support. Filtering strategy impacts recall significantly. |
| **Hybrid SQL + ANN** | pgvector | Useful when relational joins and semantic search must coexist. |
| **Keyword + Semantic Search** | Weaviate | Native BM25 + vector fusion support. |

---

# What Interviewers Actually Probe

## Q1: Why not use pgvector for everything?

**Answer:**

pgvector's HNSW index keeps the graph structure in memory.

At roughly **50M+ vectors**, memory requirements can reach **50–100 GB per node**. Scaling requires manual PostgreSQL sharding, which often breaks relational JOIN semantics.

Dedicated vector databases solve this through partitioning and distributed architectures designed specifically for ANN workloads.

---

## Q2: When would you choose Pinecone over Qdrant?

**Answer:**

Choose **Pinecone** when:

- The team lacks Kubernetes expertise.
- There is no on-call infrastructure team.
- Fast time-to-production is more important than infrastructure control.

Choose **Qdrant** when:

- Data residency requirements exist.
- Custom hardware optimization is needed.
- Avoiding vendor lock-in is important.
- Self-hosting is acceptable.

---

## Q3: What is the risk of using FAISS in production?

**Answer:**

FAISS is an ANN library, not a complete database.

Out of the box it lacks:

- Persistence
- API server
- Authentication
- Authorization
- Observability
- Multi-tenancy

Using FAISS means building the database layer yourself.

It works very well for:

- Offline indexing
- Batch retrieval
- Research systems

It is generally not sufficient alone for production-facing real-time search applications.

---

## Q4: How does Redis VSS handle memory pressure?

**Answer:**

When `maxmemory` is reached, Redis begins evicting keys according to the configured eviction policy (e.g., `allkeys-lru`).

If vector indexes are stored in Redis hashes, portions of the vector data may be evicted, silently reducing recall quality.

Production systems typically:

- Ensure the entire vector index fits in memory.
- Maintain significant memory headroom.
- Use Redis Enterprise tiering when necessary.

---

# Common Interview Traps to Avoid

### 1. Saying "I'd use Pinecone" without constraints

Interviewers want to hear:

- Dataset size
- Query volume
- Latency requirements
- Budget constraints
- Operational ownership

Always explain **why** Pinecone is appropriate.

---

### 2. Treating ANN accuracy as binary

A senior engineer understands ANN tuning tradeoffs.

For HNSW:

- `ef_construction` affects index quality and build time.
- `ef_search` affects recall and query latency.

Higher recall generally means higher latency.

---

### 3. Ignoring embedding migration

When the embedding model changes:

- Existing embeddings become incompatible.
- Re-indexing is required.

A senior answer should include:

- Versioned embeddings
- Dual-index strategy
- Gradual migration plan

---

### 4. Assuming vector databases solve freshness

Vector databases only store embeddings.

You still need:

- CDC pipelines
- Event-driven updates
- Re-embedding workflows
- Synchronization with source systems

In real-world RAG systems, maintaining embedding freshness is often harder than vector search itself.

---

# Quick Senior-Level Rule of Thumb

| Scenario | Pick |
|-----------|------|
| Existing PostgreSQL + <1M vectors | pgvector |
| Managed SaaS | Pinecone |
| Open-source self-hosted | Qdrant |
| Massive scale (100M+) | Milvus |
| Ultra-low latency | Redis VSS |
| Offline retrieval / batch jobs | FAISS |
| Hybrid SQL + Vector Search | pgvector |
| Hybrid Keyword + Semantic Search | Weaviate |

---

## Interview One-Liner

> "I don't choose a vector database based on popularity. I choose based on vector count, latency SLA, filtering requirements, infrastructure ownership, and operational complexity. The database is often the easy part—the harder problem is keeping embeddings fresh and managing embedding migrations at scale."