# Phase 1 — Topic 7: JSON, Serialization & Deserialization

This is an important topic because **REST APIs commonly exchange data as JSON**.

You will use JSON constantly with FastAPI.

---

## 1. What is JSON?

**JSON = JavaScript Object Notation**

It is a standard text format used to exchange data between systems.

Example:

```json
{
    "name": "Sumanth",
    "age": 27,
    "skills": ["Python", "SQL", "FastAPI"]
}
```

It looks similar to a Python dictionary, but **JSON is not a Python dictionary**.

### Python

```python
user = {
    "name": "Sumanth",
    "age": 27
}
```

### JSON

```json
{
    "name": "Sumanth",
    "age": 27
}
```

The Python object exists inside your Python program.

JSON is **text/data representation** used for communication.

---

# 2. Why APIs use JSON

Imagine your Python client wants to create a user.

Python object:

```python
user = {
    "name": "Sumanth",
    "age": 27
}
```

It sends that information to a server as JSON:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

The server receives it and converts it into something it can work with.

So:

```text
Python Object
     ↓
   JSON
     ↓
HTTP Request
     ↓
   Server
     ↓
   JSON
     ↓
Python Object
```

---

# 3. Serialization

**Serialization means converting a Python object into a format that can be transmitted/stored.**

For JSON:

```text
Python object → JSON
```

Example:

```python
user = {
    "name": "Sumanth",
    "age": 27
}
```

Convert to JSON:

```python
import json

json_data = json.dumps(user)

print(json_data)
```

Output:

```text
{"name": "Sumanth", "age": 27}
```

`json.dumps()` converts a Python object into a JSON string.

---

# 4. Deserialization

The reverse process is:

```text
JSON → Python object
```

Example:

```python
import json

json_data = '{"name": "Sumanth", "age": 27}'

user = json.loads(json_data)

print(user)
```

Now:

```python
print(type(user))
```

gives:

```text
<class 'dict'>
```

So:

```text
Serialization:
Python → JSON

Deserialization:
JSON → Python
```

Remember this:

```text
dump  → Python → JSON
load  → JSON → Python
```

---

# 5. JSON Data Types

JSON supports:

### String

```json
{
    "name": "Sumanth"
}
```

### Number

```json
{
    "age": 27
}
```

### Boolean

```json
{
    "active": true
}
```

### Null

```json
{
    "email": null
}
```

### Array

```json
{
    "skills": ["Python", "SQL", "FastAPI"]
}
```

### Object

```json
{
    "user": {
        "name": "Sumanth",
        "age": 27
    }
}
```

---

# 6. Python vs JSON

There are some differences.

| Python  | JSON    |
| ------- | ------- |
| `dict`  | object  |
| `list`  | array   |
| `str`   | string  |
| `int`   | number  |
| `float` | number  |
| `True`  | `true`  |
| `False` | `false` |
| `None`  | `null`  |

Notice:

Python:

```python
True
False
None
```

JSON:

```json
true
false
null
```

---

# 7. JSON in REST APIs

Now let's connect everything we've learned.

Suppose the client wants to create a user.

### Request

```http
POST /users
Content-Type: application/json
```

Body:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

The server processes the JSON.

Then it sends:

### Response

```http
HTTP/1.1 201 Created
Content-Type: application/json
```

Body:

```json
{
    "id": 101,
    "name": "Sumanth",
    "age": 27
}
```

So the communication is:

```text
             HTTP REQUEST

Python
  │
  │ POST /users
  │ Content-Type: application/json
  │
  │ {"name": "Sumanth", "age": 27}
  ↓
FastAPI
  │
  │ Process data
  ↓
             HTTP RESPONSE

Python
  ↑
  │ 201 Created
  │ Content-Type: application/json
  │
  │ {"id": 101, "name": "Sumanth", "age": 27}
  │
FastAPI
```

---

# 8. JSON with `requests`

This is something you'll use when practicing APIs.

```python
import requests

data = {
    "name": "Sumanth",
    "age": 27
}

response = requests.post(
    "https://example.com/users",
    json=data
)
```

The `requests` library converts the Python dictionary into JSON for the HTTP request.

Then you can read a JSON response:

```python
data = response.json()

print(data)
```

So you don't always need to manually call:

```python
json.dumps()
```

when using `requests`.

---

# 9. Why This Matters for FastAPI

FastAPI makes this even easier.

You can define:

```python
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int
```

Then:

```python
@app.post("/users")
def create_user(user: User):
    return user
```

Client sends:

```json
{
    "name": "Sumanth",
    "age": 27
}
```

FastAPI/Pydantic handles much of the conversion and validation for you.

Conceptually:

```text
JSON Request
     ↓
FastAPI
     ↓
Pydantic Model
     ↓
Python Object
     ↓
Your Code
```

And when you return a response:

```text
Python Object
     ↓
FastAPI
     ↓
JSON Response
```

This is why understanding JSON now will make FastAPI much easier later.

---

# Phase 1 Complete 🎯

You've now covered the core HTTP foundation:

```text
1. HTTP
2. HTTP Request
3. HTTP Response
4. HTTP Methods
5. URL / Path / Query Parameters
6. HTTP Headers
7. JSON / Serialization
```

The next phase is **REST itself**.

We'll start with:

## Phase 2 — Topic 1: What exactly is REST?

We'll understand **REST vs HTTP**, resources, endpoints, CRUD, and why:

```text
GET /users/10
```

is considered RESTful while:

```text
GET /getUserById/10
```

is generally not good REST design.
