## Phase 1 — Topic 6: Structured Outputs

Since you've completed the first few topics, let's continue with **Structured Outputs**.

### 1. What problem does structured output solve?

Normally, an LLM returns **free-form text**.

For example, you ask:

> Extract the customer's name, age, and city.

The model might return:

```text
The customer is Rahul, he is 28 years old and lives in Hyderabad.
```

That's useful for humans, but difficult for a program to reliably consume.

You want something like:

```json
{
  "name": "Rahul",
  "age": 28,
  "city": "Hyderabad"
}
```

Now your Python application can directly use:

```python
result["name"]
result["age"]
result["city"]
```

So:

> **Structured output = forcing the LLM response into a predefined schema.**

---

# 2. Structured Output vs Tool Calling

These two are related but different.

### Structured output

The LLM produces data following your schema.

```text
User
 ↓
LLM
 ↓
Structured JSON
```

Example:

```json
{
  "intent": "refund",
  "priority": "high",
  "reason": "duplicate charge"
}
```

### Tool calling

The LLM decides to invoke a function/tool.

```text
User
 ↓
LLM
 ↓
Tool call
 ↓
Your Python function
 ↓
Tool result
 ↓
LLM
```

Example:

```python
get_order_status(order_id="123")
```

The important distinction:

**Structured output answers:**

> "What should the model's response look like?"

**Tool calling answers:**

> "What external action/function should the model invoke?"

---

# 3. Why agents need structured outputs

This becomes extremely important for agents.

Imagine your agent has three tools:

```python
search_customer()
get_order()
send_email()
```

The LLM shouldn't randomly generate something like:

```text
I think we should probably search for the customer first...
```

Your application needs a predictable decision.

For example:

```json
{
  "action": "search_customer",
  "arguments": {
    "customer_id": "C123"
  }
}
```

Your program can then execute it.

This is one of the foundations of reliable agents.

---

# 4. Structured output with Pydantic

Since you're using Python, **Pydantic** is especially important.

Example:

```python
from pydantic import BaseModel


class Customer(BaseModel):
    name: str
    age: int
    city: str
```

You can tell the LLM that the expected response is a `Customer`.

Conceptually:

```text
LLM
 ↓
Generate response
 ↓
Validate against Customer schema
 ↓
Customer object
```

The result becomes something like:

```python
Customer(
    name="Rahul",
    age=28,
    city="Hyderabad"
)
```

Then:

```python
customer.name
```

returns:

```text
Rahul
```

---

# 5. Why schema validation matters

Suppose the model returns:

```json
{
    "name": "Rahul",
    "age": "twenty eight",
    "city": "Hyderabad"
}
```

Your schema says:

```python
age: int
```

The application can detect that the output doesn't conform to the expected structure.

This is much safer than doing:

```python
json.loads(llm_response)
```

and blindly trusting the result.

---

# 6. Structured output in an Agent

This is where it connects to what you're learning.

Suppose the user asks:

> "Find the weather in Hyderabad."

Your agent might have an internal decision schema:

```python
class AgentDecision(BaseModel):
    action: str
    reasoning: str
    arguments: dict
```

The LLM produces:

```json
{
    "action": "get_weather",
    "reasoning": "The user is asking for current weather.",
    "arguments": {
        "city": "Hyderabad"
    }
}
```

Your agent code can then do:

```python
if decision.action == "get_weather":
    result = get_weather(**decision.arguments)
```

So structured output provides a **contract between the LLM and your application**.

---

# 7. Three levels you should understand

Think of LLM outputs as three levels:

### Level 1 — Plain text

```text
The customer wants a refund.
```

Good for humans.

---

### Level 2 — Structured data

```json
{
    "intent": "refund",
    "priority": "high"
}
```

Good when your application needs predictable data.

---

### Level 3 — Tool call

```json
{
    "tool": "process_refund",
    "arguments": {
        "order_id": "123"
    }
}
```

Good when the agent needs to **perform an action**.

---

# 8. Where structured outputs are commonly used

As an AI Engineer, you'll encounter this everywhere:

**Information extraction**

```text
Email → name, company, phone, job title
```

**Classification**

```text
Customer message → intent + sentiment + priority
```

**Routing**

```text
Question → billing / technical / sales
```

**Agent decisions**

```text
User request → next action + arguments
```

**RAG**

```text
Retrieved documents → answer + citations
```

**API generation**

```text
Natural language → API parameters
```

---

# 9. Important interview point

If an interviewer asks:

> **Why not just ask the LLM to return JSON?**

Don't say simply:

> "Because JSON might be invalid."

The deeper answer is:

> **LLMs generate probabilistic text. Structured output provides a schema/contract that makes the response predictable and machine-consumable, with validation against the expected structure.**

That's the production-level understanding.

---

# 10. One important distinction

Don't confuse:

```text
JSON
```

with:

```text
Structured Output
```

An LLM can produce JSON-looking text without actually guaranteeing that it conforms to your required schema.

Structured output means your application/model interface is explicitly enforcing a **defined structure**.

---

## Mental model

Keep this in your head:

```text
LLM
 │
 ├── Plain text
 │
 ├── Structured output
 │      └── predictable data
 │
 └── Tool calling
        └── predictable action
```

And for agents:

```text
User
  ↓
Agent / LLM
  ↓
Structured decision
  ↓
Tool
  ↓
Tool result
  ↓
Agent / LLM
  ↓
Structured decision
  ↓
...
```

### Your next topic

You've now covered **Structured Outputs**.

Next in your Phase 1 roadmap is:

**7. Agent State**

This is particularly important because once you understand **state**, the LangGraph concepts you've already worked with will become much clearer.
