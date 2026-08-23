# Topic 5 — Pydantic Schemas for LangChain Tools

Pydantic schemas are used to define **exactly what arguments a tool accepts** and how those arguments should be structured.

This becomes especially important in production agents.

---

## 1. Why do we need Pydantic?

Suppose we have:

```python
@tool
def search_customer(
    name: str,
    age: int
):
    ...
```

This gives us basic type information:

```text
name → string
age  → integer
```

But what if we want more control?

For example:

* Which fields are required?
* What does each field mean?
* What values are allowed?
* What should happen if the input is invalid?
* Should `age` be greater than 0?
* Should `status` only be `"active"` or `"inactive"`?

That's where **Pydantic** helps.

---

# 2. Basic Pydantic schema

First define a model:

```python
from pydantic import BaseModel, Field


class CustomerSearchInput(BaseModel):
    name: str = Field(description="Customer's full name")
    age: int = Field(description="Customer's age")
```

Now we have a structured schema:

```text
CustomerSearchInput
│
├── name: str
└── age: int
```

---

# 3. Using it with `@tool`

LangChain allows us to provide this schema using `args_schema`.

```python
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CustomerSearchInput(BaseModel):
    name: str = Field(description="Customer's full name")
    age: int = Field(description="Customer's age")


@tool(args_schema=CustomerSearchInput)
def search_customer(name: str, age: int):
    """Search for a customer using their name and age."""
    return f"Searching for {name}, age {age}"
```

Now the tool has an explicit input schema.

---

# 4. What does the LLM see?

Conceptually, LangChain can expose something like:

```text
Tool:
search_customer

Description:
Search for a customer using their name and age.

Arguments:

name:
  type: string
  description: Customer's full name

age:
  type: integer
  description: Customer's age
```

This gives the LLM much more structured information.

---

# 5. Why `Field(description=...)` matters

Consider:

```python
name: str
```

versus:

```python
name: str = Field(
    description="Customer's full legal name"
)
```

The second version provides additional information to the model.

Same with:

```python
age: int = Field(
    description="Customer's age in years"
)
```

Descriptions help the LLM understand **what each argument represents**.

---

# 6. Required fields

Consider:

```python
class CustomerSearchInput(BaseModel):
    name: str
    age: int
```

Both fields are required.

Conceptually:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

This is valid.

But:

```json
{
    "name": "Sumanth"
}
```

is missing:

```text
age
```

Pydantic can detect that.

---

# 7. Optional fields

You can explicitly make a field optional:

```python
from typing import Optional


class CustomerSearchInput(BaseModel):
    name: str
    age: Optional[int] = None
```

Now:

```text
name → required
age  → optional
```

This is valid:

```json
{
    "name": "Sumanth"
}
```

And this is also valid:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

---

# 8. Constraints

Pydantic can also enforce constraints.

For example:

```python
from pydantic import BaseModel, Field


class CustomerInput(BaseModel):
    name: str
    age: int = Field(gt=0, lt=120)
```

Now:

```text
age > 0
age < 120
```

is expected.

So:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

is valid.

But:

```json
{
    "name": "Sumanth",
    "age": -5
}
```

fails validation.

---

# 9. Enum-like values

Suppose your tool accepts a customer status.

You don't want:

```text
status = "xyz"
```

You only want:

```text
active
inactive
blocked
```

You can use an Enum:

```python
from enum import Enum
from pydantic import BaseModel


class CustomerStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    BLOCKED = "blocked"


class CustomerInput(BaseModel):
    customer_id: int
    status: CustomerStatus
```

Now the schema tells the model that the allowed values are restricted.

---

# 10. Nested schemas

Pydantic also allows complex structures.

For example:

```python
class Address(BaseModel):
    city: str
    country: str


class CustomerInput(BaseModel):
    name: str
    address: Address
```

The expected structure becomes:

```json
{
    "name": "Sumanth",
    "address": {
        "city": "Visakhapatnam",
        "country": "India"
    }
}
```

This is very useful for tools that require complex inputs.

---

# 11. Why this matters for Agents

Imagine an agent with a tool:

```python
@tool
def create_order(...):
    ...
```

Creating an order might require:

```text
customer_id
product_id
quantity
shipping_address
payment_method
```

Instead of loosely handling everything:

```python
def create_order(
    customer_id,
    product_id,
    quantity,
    ...
):
```

you can define a clear schema:

```python
class CreateOrderInput(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    shipping_address: str
    payment_method: str
```

Now you have a formal contract:

```text
LLM
 ↓
Generate structured arguments
 ↓
Pydantic schema
 ↓
Validate
 ↓
Tool
```

---

# 12. Tool schema = contract

This is an important production concept.

Think of the Pydantic schema as a **contract between the LLM and your tool**.

```text
             Contract
                ↓
LLM ────────────────→ Tool
       arguments
```

The contract says:

> "If you want to call this tool, provide these fields in this structure."

For example:

```text
search_customer
       │
       ↓
CustomerSearchInput
       │
       ├── name: string
       ├── age: integer
       └── status: enum
```

---

# 13. Direct invocation

You can also invoke a tool with the schema:

```python
search_customer.invoke({
    "name": "Sumanth",
    "age": 27
})
```

LangChain/Pydantic can validate the input against the defined schema.

---

# 14. Basic Python types vs Pydantic

### Simple tool

```python
@tool
def get_customer(customer_id: int):
    ...
```

Good for simple cases.

### Structured tool

```python
class CustomerInput(BaseModel):
    customer_id: int = Field(
        description="Unique customer ID"
    )


@tool(args_schema=CustomerInput)
def get_customer(customer_id: int):
    ...
```

Better when your tool has:

* Multiple arguments
* Complex inputs
* Constraints
* Detailed descriptions
* Nested objects
* Validation requirements

---

# 15. The architecture you should remember

```text
User
  ↓
LLM
  ↓
Tool selection
  ↓
Generate arguments
  ↓
Pydantic Schema
  ↓
Validation
  ↓
Tool execution
  ↓
Tool result
  ↓
LLM
  ↓
Final answer
```

This is much closer to how a production agent works.

---

# 16. Interview question

### Why use Pydantic schemas for LangChain tools?

A strong answer:

> "Pydantic schemas allow us to define structured and validated inputs for tools. They specify field names, types, descriptions, optional or required fields, and constraints. LangChain can expose this schema to the LLM so it can generate structured tool arguments, while validation helps prevent invalid inputs from reaching the tool."

---

## Key takeaway

Don't think of Pydantic as just a validation library.

For agent systems, think:

```text
Pydantic Schema
      ↓
Tool input contract
      ↓
LLM knows expected structure
      ↓
Arguments are structured
      ↓
Arguments can be validated
      ↓
Tool executes safely
```

### Next topic: **Binding Tools to an LLM**

We'll take the tools we've created and actually connect them to an LLM using `bind_tools()`. That's where the **LLM + tools** relationship starts becoming concrete.
