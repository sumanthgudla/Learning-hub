# Phase 2 — Topic 7: Authentication vs Authorization

Now we're getting into one of the most important parts of real-world REST APIs: **security**.

The first thing to understand is the difference between:

> **Authentication = Who are you?**
> **Authorization = What are you allowed to do?**

---

# 1. Authentication

Authentication verifies the identity of the client/user.

For example:

```text
Client
  ↓
"Here are my credentials"
  ↓
Server
  ↓
"Yes, you are Sumanth."
```

Common authentication mechanisms include:

* Username/password
* API keys
* JWT tokens
* OAuth 2.0
* Session cookies

---

# 2. Authorization

After authentication, the server determines what that user is allowed to do.

For example:

```text
User: Sumanth
Role: Employee
```

He might be allowed to:

```text
GET /employees/10       ✅
GET /employees          ✅
DELETE /employees/10    ❌
```

So:

```text
Authentication
    ↓
Who are you?

Authorization
    ↓
What can you do?
```

---

# 3. Easy Real-Life Example

Think about an office building.

You show your employee ID card at the entrance.

```text
ID Card
  ↓
Security checks your identity
  ↓
Authentication
```

Now you're allowed into the building.

But maybe you can't enter the server room.

```text
Server room access?
       ↓
Are you authorized?
       ↓
No ❌
```

So:

```text
ID verification → Authentication
Permission check → Authorization
```

---

# 4. REST API Example

Suppose we have:

```http
GET /users/10
```

The client sends:

```http
Authorization: Bearer eyJhbGciOi...
```

The server verifies the token.

If the token is valid:

```text
Authentication ✅
```

Then the server checks whether the user has permission.

For example:

```text
Can this user view user 10?
```

If yes:

```text
Authorization ✅
```

Then:

```http
200 OK
```

---

# 5. What Happens If Authentication Fails?

Suppose the client sends:

```http
GET /users/10
```

without a token.

The server might return:

```http
401 Unauthorized
```

Meaning:

> You haven't successfully authenticated.

Remember:

```text
401 → Authentication problem
```

---

# 6. What Happens If Authorization Fails?

Suppose the user is authenticated:

```text
Authentication ✅
```

but they're not an admin.

They try:

```http
DELETE /users/10
```

The server might return:

```http
403 Forbidden
```

Meaning:

> I know who you are, but you're not allowed to perform this operation.

Remember:

```text
403 → Permission problem
```

---

# 7. API Keys

One simple authentication mechanism is an API key.

The client receives something like:

```text
abc123xyz
```

Then sends:

```http
GET /products
X-API-Key: abc123xyz
```

The server checks:

```text
Is this API key valid?
        ↓
       Yes
        ↓
Process request
```

API keys are commonly used for:

* Service-to-service APIs
* External developer APIs
* Internal applications

---

# 8. JWT Authentication

JWT is extremely common in REST APIs.

JWT means:

> **JSON Web Token**

A simplified flow:

```text
                 Login
Client ─────────────────────> Server
                               │
                               │ Validate credentials
                               ↓
                         Generate JWT
                               │
Client <───────────────────────┘
             JWT
```

The client then uses that JWT for future requests.

```http
GET /users
Authorization: Bearer <JWT>
```

---

# 9. JWT Request Flow

Let's say you log in:

```http
POST /login
```

Body:

```json
{
    "username": "sumanth",
    "password": "password123"
}
```

Server verifies the credentials.

Then returns:

```json
{
    "access_token": "eyJhbGciOiJIUzI1Ni..."
}
```

The client stores the token.

Next request:

```http
GET /users
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

Server:

```text
Receive JWT
    ↓
Validate JWT
    ↓
Extract user information
    ↓
Check permissions
    ↓
Process request
```

---

# 10. Why `Bearer`?

You may have seen:

```http
Authorization: Bearer eyJhbGciOi...
```

`Bearer` basically indicates the authentication scheme being used.

The general structure is:

```text
Authorization: <scheme> <credentials>
```

For JWT bearer authentication:

```text
Authorization: Bearer <JWT>
```

---

# 11. JWT Structure

A JWT generally looks like:

```text
xxxxx.yyyyy.zzzzz
```

It has three parts:

```text
Header.Payload.Signature
```

For example:

```text
eyJhbGciOiJIUzI1NiJ9
.
eyJzdWIiOiIxMjMifQ
.
abc123signature
```

Conceptually:

```text
┌──────────┐
│  Header  │
├──────────┤
│ Payload  │
├──────────┤
│ Signature│
└──────────┘
```

We'll learn each part later.

---

# 12. Important JWT Point

A JWT payload is **not automatically secret**.

It is typically encoded, not encrypted.

So don't put sensitive information such as:

```text
password
credit card number
private secrets
```

inside the JWT payload.

The signature is used to help verify that the token hasn't been tampered with.

---

# 13. Authentication Flow

You should understand this flow:

```text
1. Client sends credentials
          ↓
2. Server validates credentials
          ↓
3. Server generates token
          ↓
4. Client receives token
          ↓
5. Client sends token with requests
          ↓
6. Server validates token
          ↓
7. Server checks permissions
          ↓
8. Server returns response
```

This flow is fundamental to backend development.

---

# 14. Authentication vs Authorization

Memorize this:

```text
Authentication
      ↓
"Who are you?"

Authorization
      ↓
"What are you allowed to do?"
```

And:

```text
401 → Authentication failed
403 → Authorization failed
```

---

# 15. Where This Fits in Our Architecture

Earlier we had:

```text
Client
   ↓
Router
   ↓
Service
   ↓
Repository
   ↓
Database
```

Authentication adds another layer around the request:

```text
Client
   ↓
Authentication
   ↓
Authorization
   ↓
Router
   ↓
Service
   ↓
Repository
   ↓
Database
```

In FastAPI, you'll commonly implement this using **dependencies** and security utilities.

---

## What You Need to Know Right Now

Don't worry about implementing JWT yet.

For now, understand:

```text
API Key
    ↓
Simple credential/token

JWT
    ↓
Signed token containing claims

Authentication
    ↓
Verify identity

Authorization
    ↓
Verify permissions

401
    ↓
Authentication failure

403
    ↓
Authorization failure
```

### Next Topic: JWT in Detail

We'll break down **JWT Header, Payload, Signature, access tokens, expiration, refresh tokens, and the complete login → API request flow**.
