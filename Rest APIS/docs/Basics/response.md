# Phase 1 — Topic 3: HTTP Response

You now know that:

```text
Client ──── Request ────> Server
Client <─── Response ──── Server
```

Let's understand the **response**.

An HTTP response has 3 important parts:

```text
HTTP Response
│
├── Status Code
├── Headers
└── Body
```

---

## 1. Status Code

The **status code tells the client what happened to the request.**

For example:

```http
HTTP/1.1 200 OK
```

`200` means the request was successful.

### Important status codes

#### 2xx — Success

```text
200 OK
```

Request succeeded.

```text
201 Created
```

Something was successfully created.

For example:

```http
POST /users
```

creates a user → `201 Created`

```text
204 No Content
```

Request succeeded, but there is no response body.

Commonly used for:

```http
DELETE /users/10
```

---

#### 4xx — Client Error

These mean **something was wrong with the request/client side**.

```text
400 Bad Request
```

The request is invalid.

Example:

```json
{
    "age": "hello"
}
```

when the API expects an integer.

---

```text
401 Unauthorized
```

Authentication is missing or invalid.

Example:

```text
No valid JWT token
```

---

```text
403 Forbidden
```

You are authenticated, but **you don't have permission**.

Example:

```text
Normal user tries to access admin API
```

---

```text
404 Not Found
```

The requested resource doesn't exist.

Example:

```http
GET /users/99999
```

if user `99999` doesn't exist.

---

```text
422 Unprocessable Entity
```

The request structure/data doesn't satisfy validation rules.

FastAPI commonly returns `422` for validation errors.

---

#### 5xx — Server Error

These mean something went wrong **on the server**.

```text
500 Internal Server Error
```

For example, your Python code crashes:

```python
result = 10 / 0
```

The client may receive:

```text
500 Internal Server Error
```

Other useful ones:

```text
502 Bad Gateway
503 Service Unavailable
504 Gateway Timeout
```

You'll encounter these more when working with distributed systems and production deployments.

---

# 2. Response Headers

The server can also send headers.

Example:

```http
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 45
```

The headers provide information about the response.

The most important one for now:

```http
Content-Type: application/json
```

This tells the client:

> "The response body contains JSON."

---

# 3. Response Body

The body contains the actual data.

For example:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 10,
    "name": "Sumanth"
}
```

The body is:

```json
{
    "id": 10,
    "name": "Sumanth"
}
```

---

# Complete Request + Response

Let's put everything together.

### Client sends:

```http
GET /users/10 HTTP/1.1
Host: example.com
Accept: application/json
```

### Server responds:

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 10,
    "name": "Sumanth"
}
```

Think:

```text
REQUEST
────────────────────────────

Method:  GET
Path:    /users/10
Headers: Accept: application/json
Body:    None


RESPONSE
────────────────────────────

Status:  200 OK
Headers: Content-Type: application/json
Body:    {"id": 10, "name": "Sumanth"}
```

---

# 4. See It in Python

Since you're learning Python REST services, let's connect this to code.

```python
import requests

response = requests.get(
    "https://example.com"
)

print(response.status_code)
print(response.headers)
print(response.text)
```

You might get:

```text
200
{'Content-Type': 'text/html'}
<!doctype html>
<html>
...
```

### `response.status_code`

Gets the status code:

```python
print(response.status_code)
```

Output:

```text
200
```

### `response.headers`

Gets response headers:

```python
print(response.headers)
```

### `response.text`

Gets the response body as text:

```python
print(response.text)
```

If the server returns JSON, you can use:

```python
print(response.json())
```

For example:

```python
data = response.json()

print(data["name"])
```

---

# 5. Very Important Difference

Don't confuse:

```text
401
```

and

```text
403
```

### 401

> "I don't know who you are."

Authentication problem.

### 403

> "I know who you are, but you're not allowed to do this."

Authorization/permission problem.

Example:

```text
                    API
                     │
             ┌───────┴───────┐
             ↓               ↓
          No token       Valid token
             │               │
            401          Admin API?
                             │
                       ┌─────┴─────┐
                       ↓           ↓
                      Yes          No
                     200          403
```

---

# 6. The Most Important Status Codes to Memorize

For now, focus on these:

| Code  | Meaning               | Typical situation      |
| ----- | --------------------- | ---------------------- |
| `200` | OK                    | Successful GET         |
| `201` | Created               | Successful POST        |
| `204` | No Content            | Successful DELETE      |
| `400` | Bad Request           | Invalid request        |
| `401` | Unauthorized          | Authentication problem |
| `403` | Forbidden             | No permission          |
| `404` | Not Found             | Resource doesn't exist |
| `422` | Validation Error      | Invalid input          |
| `500` | Internal Server Error | Server crashed         |

You don't need to memorize every HTTP status code.

---

## Quick test

Suppose your API has:

```http
GET /users/10
```

and user `10` exists.

What status code should the server normally return?

**A)** `200`
**B)** `404`
**C)** `500`

And if user `10` doesn't exist?

**A)** `200`
**B)** `404`
**C)** `401`
