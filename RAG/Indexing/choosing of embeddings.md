Depends on a few tradeoffs: cost, latency, domain fit, and whether you need multilingual or long-context support. Quick breakdown:

**By use case**

- **General-purpose semantic search / RAG (English, cost-sensitive)** → OpenAI `text-embedding-3-small` or `3-large`, Azure OpenAI equivalents (since you're already on Azure OpenAI), or Cohere `embed-v3`. `3-small` is cheap and good enough for most retrieval; `3-large` when recall quality matters more than cost.
- **Open-source / self-hosted, no API cost** → `BAAI/bge-large-en-v1.5`, `intfloat/e5-large-v2`, or `nomic-embed-text`. Good MTEB scores, run on your own infra, no per-call cost — worth it if you're doing high-volume embedding and want to avoid vendor lock-in.
- **Multilingual content** → `multilingual-e5-large`, Cohere `embed-multilingual-v3`, or OpenAI `3-large` (which handles multilingual decently too).
- **Domain-specific (legal, medical, code)** → fine-tuned or specialized models: `voyage-code-2` for code, `voyage-law-2` for legal, etc. Voyage AI models consistently rank well on MTEB for domain retrieval.
- **Long documents / long context chunks** → check max token limits — OpenAI's are 8191 tokens, `e5`/`bge` variants are often 512, Voyage models go higher. If you're not chunking aggressively, this matters.

**Practical decision order**
1. Do you need it self-hosted (data residency, cost at scale)? → open-source (bge/e5).
2. Otherwise, already on Azure OpenAI → just use `text-embedding-3-large` for best quality, `3-small` if cost/latency-sensitive, since you avoid adding another vendor.
3. Check MTEB leaderboard for your specific task type (retrieval vs. clustering vs. classification) — models rank differently per task, not just overall.
4. Always benchmark on your own eval set (few hundred query-doc pairs) rather than trusting leaderboard numbers blindly — domain gap is real, especially for Pega's kind of structured/enterprise content.

One thing that trips people up: embedding model and vector DB dimension must match, and once you pick one, changing it means re-embedding your entire corpus — so it's worth spending a day benchmarking upfront rather than swapping later.

Is this for something specific — a new RAG pipeline, or evaluating an existing one?