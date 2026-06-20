## RAG Novelty & Memory – Quick Bullet Points

- **3 goals RAG achieves** that retraining/fine-tuning also can but expensively:
  - Up-to-date information
  - Factually accurate responses
  - Awareness of proprietary/private data

- **RAG vs Fine-tuning vs Retraining** — RAG is cheaper, faster, and dynamically updatable; the other two need huge data + compute + regular costly updates

- **Origin** — 2020 paper by Patrick Lewis et al.: *"Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"*

- **Parametric memory** = what the LLM learned during training (stored in model weights/parameters). It's **fixed and limited**

- **Non-parametric memory** = external knowledge provided at query time (docs, databases, internet). It's **flexible and unlimited**

- **RAG = Parametric + Non-parametric memory** working together

- **3 advantages of RAG:**
  - **Deep contextual awareness** — responses grounded in your specific data source
  - **Source citation** — users can verify where the answer came from
  - **Lesser hallucination** — more context = fewer confident wrong answers

---

## Brief Explanation

**Why not just retrain or fine-tune?**
Both approaches bake new knowledge into the model's weights permanently. That sounds good, but it's extremely expensive and slow — and the moment new information comes in, you'd have to do it all over again. RAG sidesteps this entirely by keeping the model as-is and feeding it fresh information at query time.

**Parametric vs Non-parametric — the core idea:**
Think of **parametric memory** as the LLM's long-term brain — everything it learned during training, encoded into billions of numerical weights. It's powerful but frozen after training.

**Non-parametric memory** is like giving the LLM a reference book to read before answering. It's not inside the model — it lives outside (a database, your company docs, the web) and gets fetched on demand. The beauty is this "reference library" can be updated anytime without touching the model.

**The expanded RAG definition (good to quote in interviews):**
> RAG enhances the parametric memory of an LLM by creating access to an explicit non-parametric memory, from which a retriever fetches relevant info, augments it to the prompt, and enables the LLM to generate contextual, reliable, and factually accurate responses.

Paste the next chunk when ready!