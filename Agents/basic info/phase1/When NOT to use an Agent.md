# Phase 1 — Agent Fundamentals

## Topic 10: When NOT to Use an Agent

This is one of the **most important production-level concepts** in agentic AI.

A common beginner mistake is:

> "This is an AI problem → let's build an agent."

A good AI Engineer asks:

> **"Do I actually need an agent here?"**

Often, the answer is **no**.

---

# 1. First: What makes an agent expensive?

An agent typically introduces:

```text
LLM
 ↓
Decision
 ↓
Tool
 ↓
Result
 ↓
LLM
 ↓
Decision
 ↓
Tool
 ↓
...
```

Compared with:

```text
LLM
 ↓
Answer
```

the agent can introduce:

* More LLM calls
* More latency
* Higher token cost
* More failure points
* More difficult debugging
* Less predictable behavior
* Security risks
* Harder testing

So you should use an agent **only when the benefits justify this complexity**.

---

# 2. Don't use an Agent for a simple LLM task

Suppose the user asks:

> "Summarize this document."

You don't need:

```text
Agent
 ↓
Decide
 ↓
Tool
 ↓
Observe
 ↓
Decide
```

Just:

```text
Document
 ↓
LLM
 ↓
Summary
```

An agent adds unnecessary complexity.

---

# 3. Don't use an Agent for deterministic workflows

Suppose your workflow is always:

```text
Receive invoice
 ↓
Extract fields
 ↓
Validate fields
 ↓
Store in database
 ↓
Send confirmation
```

The steps are known.

You can implement this as:

```text
Workflow
 ├── Extract
 ├── Validate
 ├── Store
 └── Notify
```

You don't need an LLM deciding:

> "Hmm, maybe I should validate the invoice first..."

The workflow already knows what to do.

---

# 4. Agent vs Workflow

This distinction is extremely important.

### Workflow

You define the sequence.

```text
A → B → C → D
```

### Agent

The LLM decides the sequence.

```text
A
 ↓
LLM decides:
 ├── B
 ├── C
 ├── D
 └── E
```

If you already know the correct sequence, **prefer a workflow**.

---

# 5. Don't use an Agent for simple RAG

Suppose you have:

> "What is the refund policy?"

Your RAG pipeline is:

```text
Question
 ↓
Retriever
 ↓
Relevant documents
 ↓
LLM
 ↓
Answer
```

That's sufficient.

You don't necessarily need:

```text
Agent
 ↓
Should I search?
 ↓
Search
 ↓
Should I search again?
 ↓
Search again
 ↓
Should I use another retriever?
 ↓
...
```

If retrieval is straightforward, normal RAG is simpler and more predictable.

---

# 6. Don't use an Agent when the next step is known

Suppose:

```text
User input
 ↓
Classify intent
 ↓
Retrieve documents
 ↓
Generate answer
```

There is no reason for the LLM to dynamically choose between those steps.

Implement it directly:

```text
Input
 ↓
Classifier
 ↓
Retriever
 ↓
Generator
```

This is often called a **pipeline** or **workflow**.

---

# 7. Don't use an Agent when latency is critical

Suppose your API has a requirement:

> Response must be under 500 ms.

An agent may perform:

```text
LLM call #1
 ↓
Tool
 ↓
LLM call #2
 ↓
Tool
 ↓
LLM call #3
```

That's difficult to guarantee.

A simpler architecture:

```text
API
 ↓
Retriever
 ↓
LLM
 ↓
Response
```

may be much easier to optimize.

---

# 8. Don't use an Agent when cost is extremely sensitive

Suppose one request normally requires:

```text
1 LLM call
```

An agent might require:

```text
4 LLM calls
+
3 tool calls
```

If you have:

```text
1 million requests/day
```

the difference becomes significant.

You should always ask:

> **Can I solve this with fewer model calls?**

---

# 9. Don't use an Agent for deterministic calculations

Suppose the user asks:

> "What is 157 × 382?"

Don't ask an LLM agent to reason through it.

Use a calculator/program:

```python
157 * 382
```

Similarly:

* Currency conversion → appropriate API
* Database aggregation → SQL
* Sorting → code
* Filtering → code
* Mathematical calculations → calculator/code

Use deterministic systems where deterministic systems are better.

---

# 10. Don't use an Agent when rules are clear

Suppose your business rule is:

```text
if customer_age < 18:
    reject

elif income < 30000:
    reject

else:
    approve
```

You don't need an agent.

Use normal application logic.

Why?

Because business rules need:

* Predictability
* Auditability
* Testing
* Consistency

LLMs are probabilistic.

Your business rule isn't.

---

# 11. Don't let an Agent make high-risk decisions unnecessarily

This is particularly important.

Imagine:

```text
Agent
 ↓
Banking system
 ↓
Transfer ₹10,00,000
```

Giving an autonomous agent unrestricted access to such a tool is dangerous.

A better architecture might be:

```text
Agent
 ↓
Proposes action
 ↓
Validation / policy check
 ↓
Human approval
 ↓
Execute
```

The agent can assist with the decision without having unrestricted authority.

---

# 12. Don't use an Agent when a normal API is enough

Suppose your application needs:

```text
GET /customer/123
```

You don't need:

```text
User
 ↓
Agent
 ↓
Decide whether to call customer API
 ↓
Call API
 ↓
LLM
 ↓
Answer
```

If the application already knows it needs customer `123`:

```text
Application
 ↓
GET /customer/123
 ↓
Response
```

is better.

---

# 13. Don't use an Agent just because you're using tools

This is a subtle but important point.

Having tools doesn't automatically mean you need an agent.

For example:

```text
User
 ↓
Application
 ↓
Weather API
 ↓
LLM
 ↓
Answer
```

You are using a tool/API, but the workflow can still be deterministic.

An agent is useful when the model needs to **decide dynamically which tool/action to use and potentially repeat actions**.

---

# 14. A very useful decision framework

When designing an AI system, ask these questions:

### Question 1

**Is the workflow deterministic?**

If yes:

```text
→ Prefer workflow
```

### Question 2

**Can one LLM call solve it?**

If yes:

```text
→ Use simple LLM call
```

### Question 3

**Is retrieval the only external operation?**

If yes:

```text
→ Consider RAG
```

### Question 4

**Does the system need multiple tools?**

Maybe:

```text
→ Agent
```

### Question 5

**Does the next action depend on the previous result?**

If yes:

```text
→ Agent becomes more appropriate
```

### Question 6

**Can the task be solved deterministically with code/API/SQL?**

If yes:

```text
→ Prefer deterministic implementation
```

---

# 15. Simple comparison

| Problem                           | Best starting approach |
| --------------------------------- | ---------------------- |
| Summarize text                    | LLM                    |
| Translate text                    | LLM                    |
| Classify support ticket           | LLM                    |
| Question over documents           | RAG                    |
| Fixed multi-step process          | Workflow               |
| SQL aggregation                   | SQL                    |
| Mathematical calculation          | Code/calculator        |
| Simple API call                   | Normal API             |
| Dynamic multi-tool task           | Agent                  |
| Tool selection depends on results | Agent                  |
| Iterative troubleshooting         | Agent                  |
| Autonomous research               | Agent                  |

The key phrase is:

> **Start with the simplest architecture that solves the problem.**

---

# 16. Example: Customer Support

Suppose you are building a customer-support application.

### Approach A — Agent everywhere

```text
User
 ↓
Agent
 ↓
Decide
 ↓
Search KB
 ↓
Agent
 ↓
Check customer
 ↓
Agent
 ↓
Create ticket
 ↓
Agent
 ↓
Answer
```

Looks impressive.

But it may be unnecessary.

---

### Approach B — Workflow

```text
User
 ↓
Intent classifier
 ↓
 ┌──────────────┬──────────────┐
 ↓              ↓              ↓
Billing       Technical      Account
 ↓              ↓              ↓
Specific       RAG            API
workflow
```

Much more predictable.

---

### Approach C — Agent only where needed

Maybe technical troubleshooting is genuinely dynamic:

```text
User
 ↓
Intent Router
 ↓
Technical issue
 ↓
Agent
 ↓
Check logs
 ↓
Search KB
 ↓
Run diagnostic
 ↓
Check result
 ↓
Try another diagnostic
 ↓
Final answer
```

This is often a better architecture.

**Use agents for the parts that actually require agentic behavior.**

---

# 17. This is an important production principle

Don't think:

```text
LLM → Agent
```

Think:

```text
Problem
  ↓
What is the simplest architecture?
  ↓
 ┌─────────────┬────────────┬─────────────┐
 ↓             ↓            ↓
LLM            RAG        Workflow
                              │
                              ↓
                           Agent
                    (only if necessary)
```

Agents should be **earned by complexity**, not added by default.

---

# 18. Interview question

### "When would you not use an agent?"

A strong answer:

> **I would avoid an agent when the workflow is deterministic, the next steps are known in advance, or the task can be solved with a single LLM call, standard RAG, SQL, code, or an API. Agents introduce additional latency, cost, complexity, and failure modes. I would use an agent when the task requires dynamic decision-making, multiple tools, iterative execution, or the next action depends on previous results.**

That's a very good Senior AI Engineer answer.

---

# 19. Complete Phase 1 mental model

You've now completed the entire **Agent Fundamentals** phase.

```text
                    AI AGENT
                       │
       ┌───────────────┼────────────────┐
       ↓               ↓                ↓
      LLM            Tools            State
       │               │                │
       └───────────────┼────────────────┘
                       ↓
                    Loop
                       ↓
              Reason → Act → Observe
                       ↓
                    Repeat
                       ↓
                  Finish
```

And the most important architectural decision:

```text
Simple problem
     ↓
Use simple solution

Complex dynamic problem
     ↓
Consider Agent
```

### Phase 1 is now complete. 🎯

You have covered:

1. What is an AI Agent?
2. LLM vs Agent vs RAG
3. Agent Loop
4. Tools & Tool Calling
5. Function Calling
6. Structured Outputs
7. Agent State
8. Why Agents Need Loops
9. ReAct Pattern
10. When NOT to Use an Agent

**Next phase should move from concepts to implementation:** building a simple agent with **Python + an LLM + tools**, then gradually adding state, loops, and error handling.
