# Phase 2 — Topic 1: What Exactly Is REST?

Now we're moving from **HTTP fundamentals** to **REST**.

The most important thing to understand first:

> **REST is not a protocol. HTTP is a protocol. REST is an architectural style for designing APIs.**

---

## 1. HTTP vs REST

You already learned HTTP:

```text
Client
   │
   │ HTTP Request
   ↓
Server
   │
   │ HTTP Response
   ↓
Client
```

REST gives us **guidelines for how we should design those HTTP APIs**.

For example, HTTP allows us to create:

```text
GET /getUserById/10
```

But REST encourages us to think in terms of **resources**:

```text
GET /users/10
```

Both can work technically.

But `/users/10` follows REST principles better.

---

# 2. What is a Resource?

A **resource is a thing that your API manages**.

For example:

```text
Users
Products
Orders
Customers
Payments
Documents
Messages
```

You represent these resources using URLs.

For example:

```text
/users
/products
/orders
/customers
/documents
```

Think:

```text
Resource        URL
---------------------------
Users       →   /users
Products    →   /products
Orders      →   /orders
```

---

# 3. Collection vs Individual Resource

This is important.

### Collection

```text
/users
```

means:

> The collection of users.

### Individual resource

```text
/users/10
```

means:

> User with ID 10.

So:

```text
/users
   ↓
All users

/users/10
   ↓
Specific user
```

Similarly:

```text
/products
/products/100

/orders
/orders/500
```

---

# 4. HTTP Method + Resource

This is where REST becomes interesting.

Instead of putting the action in the URL, REST uses the **HTTP method** to describe the operation.

For example:

```text
GET /users
```

means:

> Retrieve users.

```text
POST /users
```

means:

> Create a user.

```text
GET /users/10
```

means:

> Retrieve user 10.

```text
PUT /users/10
```

means:

> Replace/update user 10.

```text
DELETE /users/10
```

means:

> Delete user 10.

So:

```text
HTTP Method + Resource
        ↓
     Operation
```

---

# 5. Why Not Put Actions in the URL?

You might see APIs like:

```text
/getUser
/createUser
/updateUser
/deleteUser
```

These aren't necessarily invalid APIs, but they're not following the usual REST resource-oriented style.

REST prefers:

```text
GET    /users/10
POST   /users
PUT    /users/10
DELETE /users/10
```

Notice that the URL is always about the **resource**:

```text
/users
```

The HTTP method tells us what we're doing with it.

---

# 6. Think Like a Database

A useful mental model is to think about a database table.

Suppose you have:

```text
USER
-----------------------
id | name | age
-----------------------
1  | Ram  | 25
2  | Ravi | 30
3  | John | 28
```

Your REST API could expose this as:

```text
/users
```

Then:

```text
GET /users
```

returns the collection.

```text
GET /users/2
```

returns:

```json
{
    "id": 2,
    "name": "Ravi",
    "age": 30
}
```

You can think:

```text
Database table
      ↓
REST resource
      ↓
/users
```

This isn't a strict requirement—REST resources don't have to correspond directly to database tables—but it's a useful starting mental model.

---

# 7. Nested Resources

Resources can have relationships.

Suppose:

```text
User
 └── Orders
```

You could have:

```text
/users/10/orders
```

Meaning:

> Orders belonging to user 10.

And:

```text
/users/10/orders/500
```

Meaning:

> Order 500 belonging to user 10.

Another example:

```text
/products/100/reviews
```

Meaning:

> Reviews for product 100.

---

# 8. CRUD and REST

You already learned CRUD.

REST maps nicely to CRUD:

```text
Create → POST
Read   → GET
Update → PUT/PATCH
Delete → DELETE
```

For users:

| Operation      | Method | Endpoint    |
| -------------- | ------ | ----------- |
| Create         | POST   | `/users`    |
| Get all        | GET    | `/users`    |
| Get one        | GET    | `/users/10` |
| Replace        | PUT    | `/users/10` |
| Partial update | PATCH  | `/users/10` |
| Delete         | DELETE | `/users/10` |

This is the basic pattern you'll use when we start building FastAPI applications.

---

# 9. REST Is Stateless

This is one of the most important REST concepts.

**Stateless means the server should not depend on remembering the client's previous request to understand the current request.**

For example:

### Request 1

```http
GET /users/10
Authorization: Bearer abc123
```

### Request 2

```http
GET /orders/50
Authorization: Bearer abc123
```

Each request contains the information the server needs to process it.

The server shouldn't assume:

> "I remember that this client authenticated five minutes ago."

Instead, the request carries the necessary authentication information.

```text
Request 1 → contains required context
Request 2 → contains required context
Request 3 → contains required context
```

We'll explore statelessness more deeply later.

---

# 10. RESTful API Example

Imagine you're building an e-commerce API.

A REST-style API could look like:

```text
GET    /products
GET    /products/100

POST   /products

PUT    /products/100
PATCH  /products/100

DELETE /products/100
```

For orders:

```text
GET    /orders
GET    /orders/500

POST   /orders

PATCH  /orders/500

DELETE /orders/500
```

Notice how clean the URLs are.

---

# 11. A Non-RESTful vs RESTful Example

### Less REST-oriented

```text
GET  /getAllUsers
GET  /getUserById/10
POST /createUser
POST /updateUser
POST /deleteUser
```

### REST-oriented

```text
GET    /users
GET    /users/10
POST   /users
PUT    /users/10
DELETE /users/10
```

The second approach separates:

```text
Resource → URL
Operation → HTTP method
```

That's the key idea.

---

# 12. One Important Caveat

Don't think:

> "REST means you MUST use exactly these URLs."

REST is an architectural style, not a rigid syntax specification.

Real-world APIs sometimes use:

```text
POST /users/10/activate
```

for an action that doesn't map cleanly to CRUD.

So don't become overly strict about URLs.

The goal is to design APIs that are:

* predictable
* resource-oriented
* consistent
* easy to understand

---

# Your Mental Model

Remember this:

```text
                 REST API
                    │
            ┌───────┴───────┐
            ↓               ↓
        Resource         Operation
            ↓               ↓
        /users             GET
        /orders            POST
        /products          PUT
                           PATCH
                           DELETE
```

So when you see:

```text
PATCH /users/10
```

your brain should immediately think:

> **Resource:** user 10
> **Operation:** partially update it

---

## Quick Check

Suppose you have a **books** resource.

What would be the REST-style endpoint and method for:

1. Get all books
2. Get book with ID `25`
3. Create a new book
4. Change only the title of book `25`
5. Delete book `25`

Think about the answers before moving on.

**Next topic: REST Resource Naming & Endpoint Design** — we'll learn how to design good URLs, plural vs singular names, nested resources, and common REST API mistakes.
