# Phase 2 — Topic 4: Idempotency

**Idempotency** is an important REST concept and a common interview topic.

The simple definition is:

> **If you perform the same request multiple times, the intended final state of the server is the same as if you performed it once.**

Let's make that concrete.

---

## 1. Simple Example

Suppose:

```http
DELETE /users/10
```

You send it once:

```text
User 10 → deleted
```

You send the exact same request again:

```http
DELETE /users/10
```

User 10 is still:

```text
User 10 → deleted
```

The final state didn't change.

Therefore, DELETE is generally considered **idempotent**.

```text
DELETE × 1 → deleted
DELETE × 2 → deleted
DELETE × 10 → deleted
```

---

# 2. GET Is Idempotent

Suppose:

```http
GET /users/10
```

You call it:

```text
1 time
10 times
100 times
```

You're just retrieving the user.

You're not changing the resource.

So GET is considered idempotent.

```text
GET
 ↓
Read
 ↓
No state change
```

---

# 3. PUT Is Idempotent

Suppose user 10 is:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

You send:

```http
PUT /users/10
```

with:

```json
{
    "name": "Rahul",
    "age": 30
}
```

After the first request:

```text
User 10:
name = Rahul
age = 30
```

Send the exact same request again:

```http
PUT /users/10
```

Same body:

```json
{
    "name": "Rahul",
    "age": 30
}
```

The final state remains:

```text
name = Rahul
age = 30
```

Therefore PUT is idempotent.

---

# 4. POST Is Usually NOT Idempotent

This is the interesting one.

Suppose:

```http
POST /users
```

with:

```json
{
    "name": "Sumanth"
}
```

You send it once:

```text
User 101 created
```

Send it again:

```text
User 102 created
```

Send it again:

```text
User 103 created
```

Now you have multiple users.

```text
POST × 1 → 1 user created
POST × 2 → 2 users created
POST × 3 → 3 users created
```

Therefore POST is generally **not idempotent**.

---

# 5. PUT vs POST

This is one reason the distinction between PUT and POST matters.

### POST

Usually means:

> Create a new resource; the server determines the resource ID.

```http
POST /users
```

Server:

```text
Creates user 101
```

Another request:

```text
POST /users
```

Server:

```text
Creates user 102
```

---

### PUT

Usually means:

> Set/replace a resource at a specific URI.

```http
PUT /users/101
```

You are saying:

> Make user 101 have this representation.

Repeated requests produce the same intended final state.

---

# 6. Why Does Idempotency Matter?

Imagine you're making a payment API.

Suppose you send:

```http
POST /payments
```

and your network connection fails.

You don't know whether the server processed it.

Your application might retry:

```text
Request 1
   ↓
Server processes payment
   ↓
Network failure
   X

Client doesn't know what happened

Retry
   ↓
Server processes payment again
```

Potentially:

```text
₹10,000 charged
+
₹10,000 charged again
```

That's a serious problem.

---

# 7. Idempotency Keys

Payment APIs often solve this using an **idempotency key**.

For example:

```http
POST /payments
Idempotency-Key: abc123
```

Body:

```json
{
    "amount": 10000,
    "currency": "INR"
}
```

If the client retries:

```http
POST /payments
Idempotency-Key: abc123
```

the server recognizes:

> "I've already processed request `abc123`."

So it doesn't create another payment.

Conceptually:

```text
Request
   │
   │ Idempotency-Key: abc123
   ↓
Server
   │
   ├── First time?
   │      ↓
   │    Process
   │
   └── Already processed?
          ↓
       Return previous result
```

This is extremely useful in real production systems.

---

# 8. Which HTTP Methods Are Idempotent?

For your current level, remember:

| Method | Generally Idempotent?        |
| ------ | ---------------------------- |
| GET    | ✅ Yes                        |
| PUT    | ✅ Yes                        |
| DELETE | ✅ Yes                        |
| PATCH  | ⚠️ Depends on implementation |
| POST   | ❌ Generally no               |

**Important:** Idempotency is about the **effect of repeated identical requests**, not whether the response itself is identical every time.

Also, "idempotent" does **not** mean "the request can only be sent once."

It means repeated identical requests have the same intended effect on server state.

---

# 9. Simple Interview Answer

If an interviewer asks:

> **What is idempotency in REST?**

You can say:

> Idempotency means making the same request multiple times has the same intended effect on the server as making it once. GET, PUT, and DELETE are generally idempotent, while POST is generally not. It is especially important when retrying requests over unreliable networks.

That's a good answer.

---

## Remember This

```text
GET
→ Read
→ Idempotent

PUT
→ Set/replace
→ Idempotent

DELETE
→ Remove
→ Idempotent

POST
→ Create/process
→ Usually not idempotent
```

### Next Topic: REST API Response Design

We'll learn how a good REST API should structure its responses, including **status codes + JSON response body + error responses**, and then we'll start moving toward actually building your first FastAPI REST service.
