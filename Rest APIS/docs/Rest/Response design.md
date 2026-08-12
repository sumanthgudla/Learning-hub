# Phase 2 — Topic 5: REST API Response Design

Now let's learn how a **well-designed REST API responds to the client**.

You already know that an HTTP response has:

```text
Response
├── Status Code
├── Headers
└── Body
```

For REST APIs, we want these pieces to be **consistent and meaningful**.

---

## 1. Successful Response

Suppose we have:

```http
GET /users/10
```

If the user exists, return:

```http
200 OK
Content-Type: application/json
```

```json
{
    "id": 10,
    "name": "Sumanth",
    "age": 27
}
```

The client can understand:

```text
200 → request succeeded
JSON → here is the user
```

---

# 2. Creating a Resource

Suppose:

```http
POST /users
```

Request body:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

If the server creates the user successfully, a good response is:

```http
201 Created
Content-Type: application/json
```

```json
{
    "id": 101,
    "name": "Sumanth",
    "age": 27
}
```

Why `201` instead of `200`?

Because you're communicating:

> A new resource was successfully created.

---

# 3. Delete Response

Suppose:

```http
DELETE /users/101
```

The server successfully deletes it.

You can return:

```http
204 No Content
```

There is no response body.

```text
204
 ↓
Successful operation
 ↓
No response body
```

You could also return `200` with a JSON response, depending on the API design, but `204` is common when there is nothing useful to return.

---

# 4. Error Responses

A good REST API should also return meaningful errors.

Suppose:

```http
GET /users/999
```

and user `999` doesn't exist.

Return:

```http
404 Not Found
Content-Type: application/json
```

For example:

```json
{
    "detail": "User not found"
}
```

The client now knows:

```text
404
 ↓
The requested resource doesn't exist
```

---

# 5. Validation Error

Suppose the API expects:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

But the client sends:

```json
{
    "name": "Sumanth",
    "age": "hello"
}
```

The API can return a validation error.

FastAPI commonly uses:

```text
422 Unprocessable Entity
```

with details describing what failed.

Conceptually:

```json
{
    "detail": [
        {
            "field": "age",
            "message": "Input should be a valid integer"
        }
    ]
}
```

The exact FastAPI response structure can vary by version/configuration, but the important concept is:

> The server tells the client which input failed validation.

---

# 6. Authentication Error

Suppose the API requires a token:

```http
GET /users
```

but the client doesn't provide valid authentication.

Return:

```http
401 Unauthorized
```

For example:

```json
{
    "detail": "Authentication required"
}
```

Remember:

```text
401
→ Authentication problem
```

---

# 7. Authorization Error

Suppose the client is authenticated, but doesn't have permission.

```http
DELETE /users/10
```

The user is logged in but isn't an administrator.

Return:

```http
403 Forbidden
```

For example:

```json
{
    "detail": "You do not have permission to delete users"
}
```

Remember:

```text
401 → Who are you?
403 → I know who you are, but you're not allowed.
```

---

# 8. Don't Always Return 200

A common beginner mistake is:

```http
200 OK
```

for everything.

For example:

```json
{
    "success": false,
    "message": "User not found"
}
```

with:

```text
200 OK
```

This is usually poor API design.

Instead:

```http
404 Not Found
```

```json
{
    "detail": "User not found"
}
```

Why?

Because clients, monitoring systems, API gateways, and developers can use the HTTP status code directly.

---

# 9. Consistent Response Structure

Suppose you build an API with:

```text
GET /users
GET /products
GET /orders
```

Try to keep response formats predictable.

For example:

```json
{
    "id": 10,
    "name": "Sumanth"
}
```

rather than having completely different structures for every endpoint without a reason.

For lists, you might use:

```json
{
    "items": [
        {
            "id": 1,
            "name": "Sumanth"
        },
        {
            "id": 2,
            "name": "Rahul"
        }
    ],
    "page": 1,
    "limit": 20,
    "total": 100
}
```

This becomes useful when implementing pagination.

---

# 10. REST API Error Design

A production API should give the client enough information to understand the problem, without exposing sensitive internal details.

Good:

```json
{
    "detail": "User not found"
}
```

Bad:

```json
{
    "error": "PostgreSQL connection failed at 10.0.0.15",
    "sql": "SELECT * FROM users WHERE id=999",
    "password": "..."
}
```

Never expose things like:

* database credentials
* internal stack traces
* passwords
* secret keys
* internal infrastructure details

---

# 11. HTTP Status Code + JSON

Think of them as working together.

### Successful GET

```http
200 OK
```

```json
{
    "id": 10,
    "name": "Sumanth"
}
```

### Successful POST

```http
201 Created
```

```json
{
    "id": 101,
    "name": "Sumanth"
}
```

### Not found

```http
404 Not Found
```

```json
{
    "detail": "User not found"
}
```

### Authentication failure

```http
401 Unauthorized
```

```json
{
    "detail": "Invalid token"
}
```

### Server error

```http
500 Internal Server Error
```

```json
{
    "detail": "Internal server error"
}
```

Notice that the **status code communicates the category of result**, while the body provides additional details.

---

# 12. How FastAPI Makes This Easy

Later you'll write something like:

```python
from fastapi import FastAPI, HTTPException

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):

    user = find_user(user_id)

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user
```

FastAPI will turn that into an HTTP response:

```text
404 Not Found
```

with a JSON error body.

So the flow becomes:

```text
Client
   │
   │ GET /users/999
   ↓
FastAPI
   │
   │ user doesn't exist
   ↓
HTTPException(404)
   │
   ↓
404 + JSON response
   │
   ↓
Client
```

---

# 13. What You Should Remember

For now, focus on this table:

| Situation                     | Status |
| ----------------------------- | -----: |
| Successful GET                |  `200` |
| Resource created              |  `201` |
| Successful operation, no body |  `204` |
| Invalid request               |  `400` |
| Authentication failed         |  `401` |
| No permission                 |  `403` |
| Resource doesn't exist        |  `404` |
| Validation failure            |  `422` |
| Unexpected server failure     |  `500` |

And remember:

```text
Status code
    +
Response headers
    +
Response body
    ↓
Complete HTTP response
```

---

## Phase 2 Progress

You've now covered:

```text
✅ What is REST?
✅ Resources
✅ REST endpoint design
✅ Path vs query parameters
✅ Statelessness
✅ Idempotency
✅ REST response design
```

The next important topic is **REST API architecture**: how a request moves through an actual backend:

```text
Client
  ↓
Router
  ↓
Controller
  ↓
Service
  ↓
Repository
  ↓
Database
```

Understanding this will make the transition to **building REST APIs with FastAPI** much easier.
