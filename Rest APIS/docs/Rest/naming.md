# Phase 2 — Topic 2: REST Resource Naming & Endpoint Design

Now let's learn how to **design good REST URLs**.

The main idea is simple:

> **URLs should represent resources, while HTTP methods represent actions.**

---

## 1. Use Nouns, Not Verbs

❌ Avoid:

```text
/getUsers
/createUser
/updateUser
/deleteUser
```

✅ Prefer:

```text
GET    /users
POST   /users
PUT    /users/10
DELETE /users/10
```

Why?

Because:

```text
/users
```

represents the **resource**.

And:

```text
GET / POST / PUT / DELETE
```

tells us what we're doing.

---

# 2. Prefer Plural Resource Names

Usually use:

```text
/users
/products
/orders
/customers
/documents
```

rather than:

```text
/user
/product
/order
/customer
```

Why?

Because `/users` represents a **collection**.

```text
/users
   │
   ├── User 1
   ├── User 2
   ├── User 3
   └── User 4
```

Then:

```text
/users/10
```

represents one specific user.

So:

```text
/users       → collection
/users/10    → individual resource
```

This convention makes APIs easier to understand.

---

# 3. Resource Hierarchy

Suppose a user has orders.

You could represent the relationship as:

```text
/users/10/orders
```

Meaning:

> Orders belonging to user 10.

Then:

```text
/users/10/orders/500
```

means:

> Order 500 belonging to user 10.

The structure is:

```text
/users
   │
   └── /10
        │
        └── /orders
              │
              └── /500
```

---

# 4. Don't Make URLs Too Deep

Although nested resources are useful, don't go crazy.

You might see something like:

```text
/users/10/orders/500/products/20/reviews/5
```

This becomes difficult to understand and maintain.

Usually, keep nesting relatively shallow.

Instead, you might have:

```text
/users/10/orders/500
```

and separately:

```text
/products/20/reviews
```

The exact design depends on the relationship and use case.

---

# 5. Filtering Should Usually Use Query Parameters

Suppose you want users from India.

Don't create:

```text
/users/fromIndia
```

Prefer:

```text
GET /users?country=India
```

For products:

```text
GET /products?category=laptop
```

Multiple filters:

```text
GET /products?category=laptop&brand=dell
```

This keeps the URL resource-oriented.

---

# 6. Searching

Use query parameters for searches.

For example:

```text
GET /users?search=sumanth
```

or:

```text
GET /products?search=iphone
```

The exact parameter name can vary.

The important concept is:

```text
/users?...
       ↑
   query/filter
```

---

# 7. Sorting

You can use query parameters:

```text
GET /products?sort=price
```

or:

```text
GET /products?sort=price&order=desc
```

Meaning:

> Get products sorted by price in descending order.

---

# 8. Pagination

For large collections:

```text
GET /users?page=2&limit=20
```

or:

```text
GET /users?offset=20&limit=20
```

This avoids returning thousands or millions of records at once.

For example:

```text
GET /users?page=1&limit=10
```

might return users 1–10.

```text
GET /users?page=2&limit=10
```

might return users 11–20.

---

# 9. Don't Put Every Action in the URL

Suppose you want to activate a user.

You might see:

```text
POST /activateUser/10
```

That's not resource-oriented.

Sometimes an action endpoint is reasonable:

```text
POST /users/10/activate
```

because `activate` represents a state-changing operation that doesn't map cleanly to standard CRUD.

But don't use action-style endpoints for ordinary CRUD operations.

For example:

❌

```text
POST /createUser
POST /deleteUser
POST /updateUser
```

✅

```text
POST   /users
DELETE /users/10
PATCH  /users/10
```

---

# 10. Case and Naming

Use consistent naming.

A common convention is lowercase plural nouns:

```text
/users
/products
/order-items
```

Avoid mixing styles:

```text
/users
/Products
/customerDetails
/ORDER_ITEMS
```

Consistency matters more than the exact convention.

---

# 11. API Versioning

As your API evolves, you may need different versions.

For example:

```text
/api/v1/users
/api/v2/users
```

This allows you to change the API without immediately breaking existing clients.

For example:

```text
GET /api/v1/users/10
```

vs:

```text
GET /api/v2/users/10
```

You'll learn API versioning in more detail later.

---

# 12. A Complete Example

Imagine you're building an employee management API.

Good resource design:

```text
GET    /employees
GET    /employees/10

POST   /employees

PUT    /employees/10
PATCH  /employees/10

DELETE /employees/10
```

Filtering:

```text
GET /employees?department=engineering
```

Pagination:

```text
GET /employees?page=2&limit=20
```

Employee's projects:

```text
GET /employees/10/projects
```

Specific project:

```text
GET /employees/10/projects/50
```

This is a clean, predictable API.

---

# 13. The Rule I Want You to Remember

When designing a REST endpoint, ask:

### Question 1

**What is the resource?**

```text
users
orders
products
employees
```

### Question 2

**Am I working with the collection or one resource?**

```text
/users
/users/10
```

### Question 3

**What operation am I performing?**

Use:

```text
GET
POST
PUT
PATCH
DELETE
```

### Question 4

**Am I filtering/searching/sorting?**

Use query parameters:

```text
/users?department=engineering
```

---

## Example

Suppose you need:

> Get all orders for customer 25 that are currently shipped.

A good endpoint could be:

```text
GET /customers/25/orders?status=shipped
```

Break it down:

```text
/customers/25
      ↓
specific customer

/orders
      ↓
their orders

?status=shipped
      ↓
filter
```

That's the REST mindset.

---

### Next Topic: REST Statelessness

We'll go deeper into one of the **most important REST principles**: what "stateless" actually means, why APIs use tokens, and how the server handles multiple requests from the same client.
