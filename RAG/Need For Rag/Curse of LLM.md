## RAG – Quick Bullet Points (Interview Scan)

- **LLMs are next-token prediction models** — trained on massive text data to predict the most probable next word, not to store facts
- **3 core limitations of LLMs:**
  - **Knowledge cutoff** — training is expensive/slow, so data has a fixed end date (e.g., GPT-4.1 cuts off at June 2024)
  - **Hallucinations** — LLMs confidently give wrong answers because they pick high-probability words, not verified facts
  - **Knowledge limitation** — no access to private/internal data (company docs, customer data, etc.)
- **RAG = Retrieval Augmented Generation** — 3 steps: **Retrieve** → **Augment** → **Generate**
- **RAG fixes LLM limitations** by injecting external, up-to-date, or private information into the prompt before the LLM responds
- **RAG market** — ~$1B in 2023, growing at 44.7% annually

---

## Brief Explanation (Go Deeper)

**Why LLMs fail without RAG:**
LLMs don't "look up" facts — they learn statistical patterns from text. So when asked about the 2023 Cricket World Cup, GPT-3.5 either admits it doesn't know or worse, confidently says India won (it was Australia). That confident wrong answer is a **hallucination** — a direct result of the model picking probable-sounding words rather than verified information.

**How RAG solves this:**
RAG is essentially automating what you'd do manually — Google the answer, copy the relevant text, and paste it alongside your question. The LLM then reads that context and answers accurately. In a real system, this is all done programmatically:
1. **Retrieve** — fetch relevant content from an external source (Wikipedia, internal docs, database)
2. **Augment** — attach that content to the user's original query
3. **Generate** — the LLM now has the facts it needs to respond accurately

The key insight: **RAG doesn't retrain the LLM** — it just gives it better context at query time. That's why it's fast, cheap, and scalable compared to retraining.

---

Paste the next chunk whenever you're ready!