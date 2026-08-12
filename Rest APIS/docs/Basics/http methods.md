Almost. 👍

* User exists → **`200 OK`** ✅
* User doesn't exist → **`404 Not Found`**, not `401`

`401` is for an **authentication problem**.

Example:

```text
GET /users/10
Authorization: <missing/invalid token>
                ↓
              401
```

Now let's continue.

# Phase 1 — Topic 4: HTTP Methods

HTTP methods tell the server **what operation you want to perform on a resource**.

The main ones you need are:

```text
GET
POST
PUT
PATCH
DELETE
```

Think about a `users` resource.

---

## 1. GET — Read

Used to retrieve data.

```http
GET /users
```

Means:

> Give me the users.

Or:

```http
GET /users/10
```

Means:

> Give me user 10.

Normally, GET doesn't modify data.

```text
GET
 ↓
Read data
```

---

## 2. POST — Create

Used to create a new resource.

```http
POST /users
```

Body:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

Server might respond:

```http
201 Created
```

with:

```json
{
    "id": 101,
    "name": "Sumanth",
    "age": 27
}
```

Think:

```text
POST
 ↓
Create new resource
```

---

## 3. PUT — Replace

Suppose user 10 currently has:

```json
{
    "id": 10,
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

You're essentially saying:

> Replace the representation of user 10 with this new data.

Think:

```text
PUT
 ↓
Replace/update the resource
```

---

## 4. PATCH — Partial Update

This is where PATCH differs from PUT.

Suppose the user is:

```json
{
    "id": 10,
    "name": "Sumanth",
    "age": 27,
    "city": "Vizag"
}
```

You only want to change the city.

Send:

```http
PATCH /users/10
```

```json
{
    "city": "Hyderabad"
}
```

Only the city needs to be changed.

Think:

```text
PATCH
 ↓
Partially update
```

### Simple way to remember

```text
PUT   → Replace
PATCH → Modify part
```

---

# 5. DELETE — Delete

```http
DELETE /users/10
```

Means:

> Delete user 10.

Server might return:

```http
204 No Content
```

Think:

```text
DELETE
   ↓
Remove resource
```

---

# CRUD Mapping

This is extremely important.

```text
CRUD
│
├── Create → POST
├── Read   → GET
├── Update → PUT / PATCH
└── Delete → DELETE
```

So a typical REST API looks like:

```text
POST   /users       → Create user
GET    /users       → Get users
GET    /users/10    → Get user 10
PUT    /users/10    → Replace user 10
PATCH  /users/10    → Modify user 10
DELETE /users/10    → Delete user 10
```

Notice something important:

**The URL stays resource-oriented.**

We don't normally create URLs like:

```text
/getUser
/createUser
/updateUser
/deleteUser
```

Instead, the **HTTP method tells us the operation**:

```text
GET    /users/10
POST   /users
PUT    /users/10
DELETE /users/10
```

That's an important part of REST thinking.

---

## One more important concept: Safe vs Idempotent

Don't worry about mastering this yet, but know the basic idea.

### GET is safe

A GET should not modify the resource.

```text
GET /users/10
```

You can call it repeatedly without changing the user.

### DELETE is idempotent

If you delete user 10 once:

```text
DELETE /users/10
```

user 10 is gone.

Calling the same DELETE again should not cause additional deletion.

We'll come back to **idempotency** when we study REST principles.

---

## Your turn

Consider this API:

```text
/users
```

What HTTP method would you use for each?

1. Get all users
2. Create a new user
3. Get user with ID 5
4. Change only the user's email
5. Delete user 5
6. Replace all details of user 5

Answer like:

```text
1 → GET
2 → ...
```

Then we'll move to **Topic 5: URL, Path Parameters, and Query Parameters**.
