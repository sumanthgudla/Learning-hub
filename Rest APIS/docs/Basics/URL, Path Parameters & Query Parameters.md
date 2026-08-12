# Phase 1 — Topic 5: URL, Path Parameters & Query Parameters

These are very important because you'll use them constantly when building FastAPI APIs.

Let's start with this URL:

```text
https://example.com/users/10?active=true&limit=20
```

It contains different parts:

```text
https://example.com/users/10?active=true&limit=20
│       │           │       │
│       │           │       └── Query parameters
│       │           └────────── Path
│       └────────────────────── Host
└────────────────────────────── Protocol
```

---

# 1. Path Parameters

A **path parameter identifies a specific resource**.

Example:

```text
/users/10
```

Here:

```text
/users/{user_id}
```

`10` is the `user_id`.

So:

```text
/users/10
/users/20
/users/50
```

represent different users.

### FastAPI example

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }
```

When the client calls:

```text
GET /users/10
```

FastAPI passes:

```python
user_id = 10
```

to your function.

---

# 2. Why use Path Parameters?

Use them when you're identifying **which specific resource** you're talking about.

For example:

```text
/users/10
/products/25
/orders/1001
```

Think:

```text
/users/10
       ↑
   specific user
```

---

# 3. Query Parameters

Query parameters come **after `?`**.

Example:

```text
/users?age=27
```

Here:

```text
age=27
```

is a query parameter.

You can have multiple:

```text
/users?age=27&city=Vizag
```

Here:

```text
age=27
city=Vizag
```

are query parameters.

---

# 4. What are Query Parameters Used For?

Usually for:

* filtering
* searching
* sorting
* pagination
* optional parameters

For example:

```text
/users?city=Vizag
```

means:

> Give me users from Vizag.

Another:

```text
/products?category=laptop
```

means:

> Give me laptops.

Another:

```text
/products?category=laptop&sort=price
```

means:

> Give me laptops sorted by price.

---

# 5. FastAPI Query Parameter

```python
@app.get("/users")
def get_users(city: str | None = None):
    return {
        "city": city
    }
```

Request:

```text
GET /users?city=Vizag
```

FastAPI gives:

```python
city = "Vizag"
```

---

# 6. Path vs Query Parameter

This is one of the most important distinctions.

### Path parameter

```text
/users/10
```

Means:

> I want **user 10**.

### Query parameter

```text
/users?city=Vizag
```

Means:

> I want users **filtered by city**.

So:

```text
Path
 ↓
Identifies a resource

Query
 ↓
Filters/modifies how you retrieve resources
```

---

# 7. Combining Them

You can use both.

```text
/users/10/orders?status=completed
```

Here:

```text
/users/10/orders
```

is the path.

```text
status=completed
```

is the query parameter.

Meaning:

> Give me completed orders for user 10.

FastAPI:

```python
@app.get("/users/{user_id}/orders")
def get_orders(
    user_id: int,
    status: str | None = None
):
    return {
        "user_id": user_id,
        "status": status
    }
```

Request:

```text
GET /users/10/orders?status=completed
```

Result:

```python
user_id = 10
status = "completed"
```

---

# 8. Pagination

Query parameters are very commonly used for pagination.

Imagine you have 1 million users.

You don't want:

```text
GET /users
```

to return all 1 million.

Instead:

```text
GET /users?page=2&limit=20
```

means:

> Give me page 2, with 20 users.

Another common style:

```text
GET /users?offset=20&limit=20
```

We'll build this later.

---

# 9. Search

For example:

```text
GET /products?search=laptop
```

The API can search products matching `"laptop"`.

---

# 10. Sorting

For example:

```text
GET /products?sort=price&order=asc
```

Meaning:

```text
sort by → price
order   → ascending
```

---

# 11. Important Rule

A simple mental rule:

### Path parameter

```text
/users/10
```

**Which resource?**

### Query parameter

```text
/users?city=Vizag
```

**How should I filter/search/sort the resources?**

---

# Example

Suppose your API has:

```text
GET /products/500?currency=INR
```

Identify each:

```text
/products/500
      ↑
   Path parameter

currency=INR
      ↑
   Query parameter
```

So:

```text
Product ID → 500
Currency   → INR
```

---

## Quick Test

What is the difference between these?

### A

```text
GET /users/10
```

### B

```text
GET /users?id=10
```

They can sometimes produce the same result, but conceptually:

**A uses a path parameter** to identify a specific user.

**B uses a query parameter** to filter/search the users collection.

For REST API design, you'll commonly see:

```text
GET /users/10
```

for a specific user.

---

### Next: HTTP Headers

We'll learn **`Content-Type`, `Accept`, `Authorization`, custom headers**, and how to send them from Python using `requests`.
