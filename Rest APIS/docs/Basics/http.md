# Phase 1 — Topic 1: HTTP

Let's start from the absolute basics. You don't need to know REST yet. First understand **HTTP**, because REST APIs are built on top of HTTP.

---

## 1. What is HTTP?

**HTTP = HyperText Transfer Protocol**

It is a set of rules that allows two systems to communicate over a network.

In a REST API, usually:

```text
Client  ───────────HTTP──────────>  Server
        <──────────HTTP───────────
```

For example, when your browser opens:

```text
https://google.com
```

your browser is the **client**, and Google's servers are the **server**.

The client sends an HTTP request, and the server sends an HTTP response.

```text
Browser
   │
   │ HTTP Request
   ↓
Google Server
   │
   │ HTTP Response
   ↓
Browser
```

That's the fundamental idea.

---

# 2. What is a Client?

A **client** is something that makes a request.

Examples:

* Browser
* Mobile application
* React application
* Python program
* Postman
* Another backend service

For example, when you use:

```python
requests.get("https://example.com")
```

your Python program is the **client**.

---

# 3. What is a Server?

A **server** is a system that receives requests and sends responses.

For example:

```text
Python Client
      │
      │ GET /users
      ↓
FastAPI Server
      │
      │ Response
      ↓
Python Client
```

Later, you'll build that FastAPI server yourself.

---

# 4. What is an HTTP Request?

An HTTP request is a message sent by the client to the server.

A simplified request looks like:

```text
GET /users/10 HTTP/1.1
Host: example.com
```

Let's break this down.

### Method

```text
GET
```

This tells the server **what operation the client wants**.

### Path

```text
/users/10
```

This tells the server **which resource** the client wants.

### HTTP version

```text
HTTP/1.1
```

This tells the server which HTTP protocol version is being used.

---

# 5. HTTP Response

The server responds with something like:

```text
HTTP/1.1 200 OK
Content-Type: application/json

{
    "id": 10,
    "name": "Sumanth"
}
```

Again, break it down.

### Status code

```text
200
```

Means the request was successful.

### Status message

```text
OK
```

Human-readable description of the status.

### Content-Type

```text
application/json
```

Tells the client what type of data is being returned.

### Response body

```json
{
    "id": 10,
    "name": "Sumanth"
}
```

This is the actual data.

---

# 6. The Most Important Concept

Memorize this flow:

```text
                 REQUEST
Client ─────────────────────────> Server
       GET /users/10

                 RESPONSE
Client <───────────────────────── Server
       200 OK
       {"id": 10, "name": "Sumanth"}
```

Everything we're going to learn about REST APIs builds on this.

---

# 7. Real Example Using Python

You can make an HTTP request from Python.

```python
import requests

response = requests.get("https://example.com")

print(response.status_code)
print(response.text)
```

Here:

```python
requests.get(...)
```

creates an HTTP **GET request**.

The server sends an HTTP response.

And:

```python
response.status_code
```

gives you the HTTP status code.

For example:

```text
200
```

---

# 8. Request vs Response

This distinction is extremely important.

### Request

**Client → Server**

Contains things like:

```text
Method
URL
Headers
Body
```

### Response

**Server → Client**

Contains:

```text
Status code
Headers
Body
```

So:

```text
REQUEST
├── Method
├── URL
├── Headers
└── Body

RESPONSE
├── Status Code
├── Headers
└── Body
```

---

# 9. One Real-World Example

Imagine an e-commerce application.

You want to see your order:

```text
GET /orders/123
```

The client sends:

```text
Client
  │
  │ GET /orders/123
  ↓
Server
```

The server finds order `123` and returns:

```text
200 OK
```

with:

```json
{
    "order_id": 123,
    "status": "shipped",
    "amount": 2500
}
```

So the complete communication is:

```text
CLIENT
  │
  │ HTTP REQUEST
  │ GET /orders/123
  ↓
SERVER
  │
  │ finds order
  │
  │ HTTP RESPONSE
  │ 200 OK
  │ JSON data
  ↓
CLIENT
```

---

# 10. What You Need to Remember From Topic 1

Don't worry about REST yet.

For now, remember these **5 things**:

| Concept  | Meaning                |
| -------- | ---------------------- |
| Client   | Sends request          |
| Server   | Processes request      |
| HTTP     | Communication protocol |
| Request  | Client → Server        |
| Response | Server → Client        |

And this diagram:

```text
       HTTP Request
CLIENT ───────────────> SERVER
       <───────────────
       HTTP Response
```

### Quick check for you

Suppose you have:

```text
Python program → FastAPI application
```

The Python program sends:

```text
GET /users/5
```

**Question:** Which one is the client, which one is the server, and what is the request?
