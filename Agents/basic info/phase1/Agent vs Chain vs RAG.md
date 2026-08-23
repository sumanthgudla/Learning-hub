# Phase 1 — Topic 3: Agent vs Chain vs RAG

Before moving into tool calling, you should be very clear on this distinction. It's one of the most common areas where people loosely use the word **agent**.

---

## 1. Chain

A **chain** follows a predefined sequence.

Example:

```text
User Question
     ↓
Retrieve Documents
     ↓
LLM
     ↓
Answer
```

The developer decides the workflow beforehand.

For example:

```python
documents = retriever.search(question)
answer = llm(question, documents)
```

The LLM doesn't decide whether retrieval should happen.

### Think:

> **Chain = developer controls the flow**

---

# 2. RAG

RAG is primarily a **knowledge retrieval architecture**.

Typical RAG:

```text
Question
   ↓
Embedding
   ↓
Vector DB
   ↓
Relevant Documents
   ↓
LLM
   ↓
Answer
```

The purpose is:

> Give the LLM external knowledge that wasn't necessarily in its context/model knowledge.

You've already learned this.

---

# 3. Agent

An agent is about **decision-making and actions**.

Imagine you give an agent these tools:

```text
Search
Calculator
Database
Weather API
Email
```

User asks:

> "Find our customer's recent orders and tell me whether their total exceeds ₹50,000."

The agent might decide:

```text
User
 ↓
Agent
 ↓
Need customer data
 ↓
Database Tool
 ↓
Orders returned
 ↓
Need total
 ↓
Calculator
 ↓
Total calculated
 ↓
Need to answer
 ↓
Final response
```

The important thing:

**The agent chose the actions.**

---

# 4. Chain vs Agent

Consider this workflow:

```text
Question
 ↓
Search
 ↓
Database
 ↓
LLM
 ↓
Answer
```

If you always execute:

```python
search()
database()
llm()
```

that's essentially a **chain/workflow**.

But suppose the LLM can decide:

```text
Question
 ↓
Agent
 ↓
Do I need search?
 ├── No
 │    ↓
 │   Answer
 │
 └── Yes
      ↓
    Search
      ↓
    Need database?
     ├── No → Answer
     └── Yes
          ↓
       Database
          ↓
        Answer
```

Now you have an **agentic workflow**.

---

# 5. Agent + RAG

This is where things become particularly interesting for you.

You can make your RAG system itself a **tool**.

```text
                 Agent
                   ↓
             Need information?
              /            \
            No              Yes
            ↓                ↓
         Answer          RAG Tool
                            ↓
                       Vector DB
                            ↓
                       Documents
                            ↓
                          Agent
                            ↓
                          Answer
```

The agent decides whether retrieval is necessary.

For example:

> "What is the refund policy?"

Agent:

```text
Need company knowledge
        ↓
Use RAG
```

But:

> "What is 15 × 20?"

Agent:

```text
No need for RAG
        ↓
Calculator
```

This is called **agentic RAG** when agents dynamically control retrieval and related reasoning.

---

# 6. Agent vs Chatbot

Another important distinction.

A chatbot can simply do:

```text
User
 ↓
LLM
 ↓
Response
```

An agent can do:

```text
User
 ↓
Agent
 ↓
Plan
 ↓
Tool
 ↓
Result
 ↓
Tool
 ↓
Result
 ↓
Final response
```

So:

> **Every agent can provide conversational interaction, but a chatbot isn't necessarily an agent.**

---

# 7. Agent vs Workflow

This is a more advanced distinction you'll need for production systems.

### Workflow

You explicitly define:

```text
A → B → C → D
```

### Agent

You give the model options:

```text
A
 ↓
LLM decides:
 ├── B
 ├── C
 ├── D
 └── Finish
```

### Production reality

You often combine both.

For example:

```text
                    Agent
                      ↓
              Determine intent
                      ↓
             ┌────────┴────────┐
             ↓                 ↓
        Support Flow       Sales Flow
             ↓                 ↓
       Fixed workflow     Agentic workflow
```

You **don't want everything to be autonomous**.

This is an important production principle:

> Use deterministic workflows where the process is known; use agents where dynamic decision-making provides value.

---

# 8. Example from your Pega experience

Imagine a **Post-Update Checker**.

You could build it as a fixed workflow:

```text
Get rules
 ↓
Compare versions
 ↓
Run validations
 ↓
Generate report
```

That's a workflow.

But suppose the system needs to determine:

```text
Rule changed?
     ↓
Yes
 ↓
What type of change?
 ├── Database → inspect DB dependencies
 ├── API → inspect API dependencies
 ├── Decision logic → inspect related rules
 └── UI → inspect UI dependencies
```

Now an agent can decide which investigation path to take.

That is where agent architecture becomes useful.

---

# 9. The mental model you should keep

Remember these four:

```text
LLM
↓
Generates/understands language

RAG
↓
Provides external knowledge

Tool
↓
Allows the model/system to perform an action

Agent
↓
Decides which actions to take and can iterate
```

Together:

```text
                 ┌─────────────┐
                 │    Agent    │
                 └──────┬──────┘
                        ↓
              ┌───────────────────┐
              │   Decide Action   │
              └─────────┬─────────┘
                        ↓
          ┌─────────────┼─────────────┐
          ↓             ↓             ↓
        RAG          Database       API
          ↓             ↓             ↓
          └─────────────┼─────────────┘
                        ↓
                       LLM
                        ↓
                Continue / Finish
```

## Interview-ready answer

If an interviewer asks:

**"What is the difference between RAG and an agent?"**

A good answer is:

> "RAG is primarily a technique for retrieving external knowledge and providing it to an LLM. An agent is a system where an LLM can dynamically decide what actions to take, such as retrieving information, calling APIs, querying databases, or using other tools, and can iterate based on the results."

---

### Next topic: **Tool Calling**

This is where agents become practical.

We'll learn exactly how an LLM goes from:

```text
"I need weather information"
```

to:

```python
weather(city="Hyderabad")
```

and how the tool result gets sent back to the LLM.
