# Phase 2 — Topic 6: REST API Architecture

Now we're moving from **REST concepts** to how a real Python REST service is structured.

A beginner might write everything in one file:

```python
@app.get("/users")
def get_users():
    # database code
    # business logic
    # validation
    # response
```

That works for a small project, but production applications usually separate responsibilities.

---

# 1. The Basic Architecture

A common architecture looks like:

```text
Client
  │
  │ HTTP Request
  ↓
Router / Controller
  │
  ↓
Service
  │
  ↓
Repository / DAO
  │
  ↓
Database
```

And the response comes back:

```text
Database
   ↑
Repository
   ↑
Service
   ↑
Router
   ↑
Client
```

Let's understand each layer.

---

# 2. Router

The **router** determines which piece of code should handle the request.

For example:

```http
GET /users/10
```

FastAPI might have:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    ...
```

The router essentially says:

```text
GET /users/10
       ↓
get_user()
```

Think of the router as the **entry point**.

---

# 3. Controller

In some architectures, the router itself acts as the controller.

Its responsibility should primarily be:

```text
Receive request
      ↓
Validate/parse input
      ↓
Call service
      ↓
Return response
```

For example:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):

    user = user_service.get_user(user_id)

    return user
```

The controller shouldn't contain a lot of business logic.

---

# 4. Service Layer

The **service layer contains business logic**.

For example:

```python
def get_user(user_id):
    user = user_repository.find_by_id(user_id)

    if user is None:
        raise UserNotFoundException()

    return user
```

The service decides:

> What should the application actually do?

For example, creating an order might involve:

```text
Create order
 ↓
Check customer exists
 ↓
Check product exists
 ↓
Check inventory
 ↓
Calculate price
 ↓
Apply discount
 ↓
Save order
```

That is business logic.

It belongs in the service layer rather than inside the API route.

---

# 5. Repository Layer

The repository handles **database interaction**.

For example:

```python
def find_by_id(user_id):
    return db.query(User).filter(
        User.id == user_id
    ).first()
```

The repository's job is basically:

> Get data from or save data to the database.

You don't want your API route directly writing lots of SQL/database logic.

---

# 6. Complete Example

Imagine:

```http
GET /users/10
```

The request flows like this:

```text
Client
  │
  │ GET /users/10
  ↓
FastAPI Router
  │
  │ user_service.get_user(10)
  ↓
Service
  │
  │ user_repository.find_by_id(10)
  ↓
Repository
  │
  │ SQL query
  ↓
PostgreSQL
```

Database returns:

```json
{
    "id": 10,
    "name": "Sumanth"
}
```

Then:

```text
PostgreSQL
   ↑
Repository
   ↑
Service
   ↑
Router
   ↑
Client
```

The client receives:

```json
{
    "id": 10,
    "name": "Sumanth"
}
```

---

# 7. Why Separate These Layers?

Imagine you put everything inside:

```python
@app.post("/orders")
def create_order():
    # validate request
    # check customer
    # check inventory
    # calculate price
    # apply discount
    # SQL query
    # save order
    # send notification
    # create response
```

This quickly becomes difficult to maintain.

Instead:

```text
Router
 ↓
OrderService
 ↓
OrderRepository
 ↓
Database
```

Now each component has a clear responsibility.

---

# 8. Separation of Responsibilities

Remember this table:

| Layer             | Responsibility               |
| ----------------- | ---------------------------- |
| Router/Controller | Handle HTTP request/response |
| Service           | Business logic               |
| Repository        | Database operations          |
| Database          | Store data                   |

A useful rule:

> **Router knows HTTP. Service knows business logic. Repository knows the database.**

---

# 9. Example Project Structure

A FastAPI project could eventually look like:

```text
app/
│
├── main.py
│
├── routers/
│   ├── users.py
│   └── orders.py
│
├── services/
│   ├── user_service.py
│   └── order_service.py
│
├── repositories/
│   ├── user_repository.py
│   └── order_repository.py
│
├── models/
│   ├── user.py
│   └── order.py
│
├── schemas/
│   ├── user.py
│   └── order.py
│
└── database/
    └── connection.py
```

Don't worry about creating all these folders yet.

We'll build them gradually.

---

# 10. Where Does Pydantic Fit?

Pydantic is generally used for **request/response schemas and validation**.

For example:

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int
```

The request:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

gets validated before your business logic runs.

Conceptually:

```text
HTTP Request
     ↓
Pydantic
     ↓
Validated Python object
     ↓
Service
```

---

# 11. Why This Matters for AI Engineer Roles

This architecture is especially useful when you're building AI services.

For example:

```text
POST /chat
     ↓
Router
     ↓
ChatService
     ↓
RAGService
     ↓
Retriever
     ↓
Vector Database
     ↓
LLM
```

You might eventually have:

```text
FastAPI
   ↓
Chat Router
   ↓
Chat Service
   ↓
LangGraph
   ↓
Retriever
   ↓
pgvector
   ↓
Azure OpenAI
```

So REST isn't just about CRUD applications.

You can expose your **AI/RAG/LLM workflows as REST APIs**.

---

# 12. Don't Over-Engineer

One warning:

You don't need 15 layers for a tiny application.

For a simple learning project:

```text
main.py
```

is perfectly fine.

As complexity grows:

```text
main.py
 ↓
routers
 ↓
services
 ↓
repositories
```

becomes useful.

The goal is **separation of responsibility**, not creating folders just for the sake of it.

---

# The Big Picture

At this point, you should visualize a REST service like this:

```text
                 HTTP
                  │
                  ↓
             ┌─────────┐
             │  Client │
             └────┬────┘
                  │
             HTTP Request
                  │
                  ↓
             ┌─────────┐
             │ Router  │
             └────┬────┘
                  │
                  ↓
             ┌─────────┐
             │ Service │
             └────┬────┘
                  │
                  ↓
           ┌──────────────┐
           │  Repository  │
           └──────┬───────┘
                  │
                  ↓
             ┌─────────┐
             │   DB    │
             └─────────┘
```

Then the result travels back up and becomes an HTTP response.

---

## Phase 2 Progress

You've now learned:

```text
1. REST
2. Resources
3. Endpoint design
4. Statelessness
5. Idempotency
6. Response design
7. REST architecture
```

### Next: Phase 2 — Topic 7: REST API Authentication

We'll learn the difference between **authentication and authorization**, then understand the basic **JWT flow** before eventually implementing it in FastAPI.
