Correct. 👍

But there's an important nuance.

If the system is simply:

```text
User
 ↓
LLM
 ↓
Weather Tool
 ↓
LLM
 ↓
Answer
```

and the tool is **always called according to a fixed workflow**, you can describe it as **an LLM with a tool**.

If the LLM can dynamically decide:

```text
User
 ↓
LLM
 ↓
Should I call weather tool?
 ├── No → Answer
 └── Yes
       ↓
   Weather Tool
       ↓
   Result
       ↓
   LLM
       ↓
   Need another action?
```

then you're moving into **agent behavior**.

### Key distinction

| System     | Decision-making                                       |
| ---------- | ----------------------------------------------------- |
| LLM        | Generates response                                    |
| LLM + tool | Can use a tool                                        |
| Agent      | **Decides what actions to take and can iterate**      |
| RAG        | Retrieves knowledge before/while generating an answer |

So don't define an agent simply as **"LLM + tools."**

The stronger definition is:

> **Agent = LLM + tools + autonomous decision-making + control loop toward a goal.**

### Next topic: Agent Loop

This is the foundation you'll need before we get into LangGraph.

We'll learn:

**Observe → Think/Decide → Act → Observe → Repeat**

and then implement a **very small agent in Python without LangChain/LangGraph first**.
