# Phase 2 — Topic 3: Statelessness

This is one of the **most important REST concepts**, especially for interviews.

The word sounds complicated, but the basic idea is simple:

> **Each HTTP request should contain all the information the server needs to process it.**

The server should not depend on remembering what happened in a previous request.

---

## 1. Simple Example

Imagine you have:

```text
Client
   │
   │ Request 1
   ↓
Server
```

Then:

```text
Client
   │
   │ Request 2
   ↓
Server
```

In a stateless API, the server treats each request independently.

For example:

### Request 1

```http
GET /users/10
Authorization: Bearer ABC123
```

The server can process it because the request contains the authentication information.

### Request 2

```http
GET /orders/500
Authorization: Bearer ABC123
```

Again, the request contains what the server needs.

The server doesn't need to say:

> "I remember this client from Request 1."

---

# 2. What Would Stateful Mean?

Imagine the server does this:

```text
Request 1:
Login

Server:
"Okay, I'll remember that this client is Sumanth."

Request 2:
Get orders

Server:
"I remember you from Request 1."
```

Now the server is maintaining information about the client's previous interaction.

That's a **stateful** approach.

Conceptually:

```text
Request 1
   ↓
Server stores client state
   ↓
Request 2
   ↓
Server relies on stored state
```

REST encourages stateless communication.

---

# 3. Why Is Statelessness Useful?

Imagine you have 3 servers:

```text
             Load Balancer
             /     |     \
            ↓      ↓      ↓
         Server1 Server2 Server3
```

A client sends:

```text
Request 1 → Server 1
Request 2 → Server 3
Request 3 → Server 2
```

If each request contains everything necessary, **any server can process any request**.

```text
Request 1 → Server 1 ✅
Request 2 → Server 3 ✅
Request 3 → Server 2 ✅
```

This makes horizontal scaling much easier.

---

# 4. Authentication Example

Suppose you log in and receive a JWT:

```text
JWT = abc123
```

Then every request can contain:

```http
Authorization: Bearer abc123
```

For example:

```http
GET /users/10
Authorization: Bearer abc123
```

and:

```http
GET /orders/500
Authorization: Bearer abc123
```

The server validates the token on each request.

Conceptually:

```text
Login
  ↓
JWT
  ↓
Client
  ↓
┌─────────────────────────┐
│ Request + JWT            │
└─────────────────────────┘
  ↓
Server
  ↓
Validate JWT
  ↓
Process request
```

We'll learn JWT properly later.

---

# 5. Stateless Does NOT Mean the Server Stores Nothing

This is a common misunderstanding.

A server can still have:

```text
Database
Cache
Files
Configuration
Application state
```

For example:

```text
Request
   ↓
FastAPI
   ↓
PostgreSQL
```

The server can absolutely store **application data**.

What REST statelessness means is that the server shouldn't need to maintain **client session state between requests** in order to understand the next request.

---

# 6. Example With an E-commerce API

Suppose you have:

```text
POST /login
```

Response:

```json
{
    "access_token": "abc123"
}
```

The client then makes:

```http
GET /orders
Authorization: Bearer abc123
```

The server validates the token and retrieves orders.

Next request:

```http
GET /orders/500
Authorization: Bearer abc123
```

Again, the server validates the token.

The second request doesn't depend on the server remembering the first request.

---

# 7. Stateless vs Stateful

| Stateless                         | Stateful                                    |
| --------------------------------- | ------------------------------------------- |
| Each request is independent       | Requests can depend on previous requests    |
| Request carries necessary context | Server maintains client session state       |
| Easier to scale horizontally      | Scaling can be more complicated             |
| Common REST approach              | Traditional server sessions often use state |

---

# 8. Interview Question

### "Why is REST stateless?"

A good answer:

> REST APIs are stateless because each request contains all the information required by the server to process that request. The server does not rely on stored client session state from previous requests. This makes APIs easier to scale and allows requests to be handled by different servers.

That's a solid interview answer.

---

# 9. One Important Distinction

Don't confuse:

```text
HTTP
```

with:

```text
REST
```

HTTP itself doesn't automatically mean your API is RESTful.

You can build a stateful application over HTTP.

REST is an architectural style that includes **stateless communication** as one of its constraints.

---

## Mental Model

Remember:

```text
STATEFUL

Request 1
   ↓
Server remembers client
   ↓
Request 2
   ↓
Server depends on previous state
```

versus:

```text
STATELESS

Request 1 ──> Server
                 ↓
             Process

Request 2 ──> Server
                 ↓
             Process

Each request contains what is needed.
```

---

### Next Topic: Idempotency

We'll learn why:

```text
GET
PUT
DELETE
```

are generally considered **idempotent**, while:

```text
POST
```

usually isn't—and why this matters when APIs retry failed requests.
