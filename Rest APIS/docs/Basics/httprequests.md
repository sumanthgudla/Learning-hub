Correct. ✅

* **Python program** → Client
* **FastAPI application** → Server
* `GET /users/5` → HTTP request

# Phase 1 — Topic 2: HTTP Request

Now let's understand the **HTTP request** in detail. This is very important before we move to REST.

An HTTP request has 4 main parts:

```text
HTTP Request
│
├── Method
├── URL
├── Headers
└── Body
```

---

## 1. Method

The method tells the server **what you want to do**.

Common methods:

```text
GET       → Retrieve data
POST      → Create data
PUT       → Replace/update data
PATCH     → Partially update data
DELETE    → Delete data
```

For example:

```http
GET /users/10
```

means:

> "Server, give me user 10."

---

## 2. URL

Suppose you have:

```text
https://example.com/users/10
```

Break it down:

```text
https://       example.com       /users/10
   │                │                 │
protocol          host              path
```

### Protocol

```text
https://
```

We're using HTTPS.

### Host

```text
example.com
```

This identifies the server.

### Path

```text
/users/10
```

This identifies the resource we're interested in.

---

## 3. Headers

Headers provide **additional information** about the request.

For example:

```http
GET /users/10 HTTP/1.1
Host: example.com
Accept: application/json
Authorization: Bearer abc123
```

Here:

```text
Host
Accept
Authorization
```

are headers.

### `Accept`

```http
Accept: application/json
```

means:

> "I would like the response in JSON format."

### `Authorization`

```http
Authorization: Bearer abc123
```

means:

> "Here is my authentication token."

We'll learn authentication later.

---

# 4. Request Body

The body contains **data that you're sending to the server**.

This is especially common with `POST`, `PUT`, and `PATCH`.

For example:

```http
POST /users
Content-Type: application/json

{
    "name": "Sumanth",
    "age": 27
}
```

Here:

```text
POST
```

is the method.

```text
/users
```

is the path.

```text
Content-Type: application/json
```

is a header.

And:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

is the body.

---

# Put Everything Together

A complete HTTP request might look like:

```http
POST /users HTTP/1.1
Host: example.com
Content-Type: application/json
Authorization: Bearer abc123

{
    "name": "Sumanth",
    "age": 27
}
```

Think of it as:

```text
REQUEST
│
├── Method
│     POST
│
├── URL
│     /users
│
├── Headers
│     Content-Type
│     Authorization
│
└── Body
      {
          "name": "Sumanth",
          "age": 27
      }
```

---

# GET vs POST

This is something you'll use constantly.

### GET

Usually used to **retrieve** data.

```http
GET /users/10
```

Usually:

```text
GET
  ↓
Server
  ↓
Returns user
```

### POST

Usually used to **send/create** data.

```http
POST /users
```

with:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

Flow:

```text
Client
   │
   │ POST /users
   │
   │ {"name": "Sumanth"}
   ↓
Server
   │
   │ creates user
   ↓
Response
```

---

# Important Interview Concept

You might be asked:

> **Where do we send data in an HTTP request?**

There are multiple possibilities:

### Path parameter

```text
/users/10
```

### Query parameter

```text
/users?id=10
```

### Header

```http
Authorization: Bearer abc123
```

### Body

```json
{
    "name": "Sumanth"
}
```

We'll learn each of these properly.

---

## Your mental model

Whenever you see an API request, ask yourself:

```text
1. What HTTP method?
2. What URL/path?
3. What headers?
4. Is there a request body?
```

For example:

```http
POST /orders/1001
Content-Type: application/json
Authorization: Bearer xyz

{
    "product_id": 50,
    "quantity": 2
}
```

You should be able to identify:

```text
Method  → POST
Path    → /orders/1001
Headers → Content-Type, Authorization
Body    → product_id, quantity
```

**Next topic: HTTP Response** — status codes, response headers, response body, and why `200`, `201`, `400`, `401`, `404`, and `500` are different.
