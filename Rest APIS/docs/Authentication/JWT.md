# Phase 2 — Topic 8: JWT in Detail

Now let's go deeper into **JWT**, because you'll see it frequently when building FastAPI REST APIs.

---

## 1. What is JWT?

JWT = **JSON Web Token**.

It is a token that a server can issue to a client after authentication.

Typical flow:

```text
Client
   │
   │ username + password
   ↓
Server
   │
   │ verify credentials
   ↓
Generate JWT
   │
   ↓
Client
```

Then the client sends that JWT with future requests:

```http
Authorization: Bearer <JWT>
```

---

# 2. JWT Structure

A JWT looks like:

```text
xxxxx.yyyyy.zzzzz
```

It has three parts:

```text
Header.Payload.Signature
```

For example:

```text
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
.
eyJzdWIiOiIxMjMiLCJleHAiOjE3NTUwMDAwMDB9
.
SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c
```

Three sections:

```text
┌─────────────┐
│   Header    │
├─────────────┤
│   Payload   │
├─────────────┤
│  Signature  │
└─────────────┘
```

---

# 3. JWT Header

The header contains information about the token.

For example:

```json
{
    "alg": "HS256",
    "typ": "JWT"
}
```

`alg` means the algorithm used to create the signature.

For example:

```text
HS256
RS256
ES256
```

`typ` indicates the token type:

```text
JWT
```

---

# 4. JWT Payload

The payload contains **claims**.

For example:

```json
{
    "sub": "123",
    "name": "Sumanth",
    "role": "admin"
}
```

Claims are pieces of information about the token/user/context.

Common claims include:

### `sub`

Subject.

Usually identifies the user.

```json
{
    "sub": "123"
}
```

### `exp`

Expiration time.

```json
{
    "exp": 1786550400
}
```

After this time, the token should no longer be accepted.

### `iat`

Issued-at time.

```json
{
    "iat": 1786546800
}
```

### `iss`

Issuer.

```json
{
    "iss": "my-api"
}
```

### `aud`

Audience.

Identifies who the token is intended for.

---

# 5. Important: JWT Payload Isn't Secret

This is extremely important.

A JWT payload is typically **encoded, not encrypted**.

For example:

```json
{
    "sub": "123",
    "role": "admin"
}
```

Someone who possesses the token can generally decode the header and payload.

Therefore, don't put:

```text
password
credit card number
private API keys
database passwords
```

inside the payload.

The signature protects the token's integrity; it doesn't make the payload confidential.

---

# 6. JWT Signature

The third part is the signature.

Conceptually:

```text
Header
   +
Payload
   ↓
Signing algorithm + secret/private key
   ↓
Signature
```

For example, with an HMAC-based algorithm such as HS256:

```text
HMAC(
    base64url(header) + "." + base64url(payload),
    secret
)
```

The resulting signature is included in the JWT.

The server can later verify it.

---

# 7. Why Do We Need the Signature?

Imagine someone changes:

```json
{
    "role": "user"
}
```

to:

```json
{
    "role": "admin"
}
```

If they modify the payload, the original signature won't match the modified contents.

The server verifies:

```text
Header + Payload + Signature
          ↓
       Valid?
       /    \
     Yes     No
      ↓       ↓
   Accept   Reject
```

So the signature helps detect tampering.

---

# 8. Complete Login Flow

Let's put everything together.

### Step 1 — Login

```http
POST /login
Content-Type: application/json
```

```json
{
    "username": "sumanth",
    "password": "secret"
}
```

---

### Step 2 — Server validates credentials

```text
Username/password
       ↓
   Database
       ↓
Credentials valid?
```

If valid:

```text
Generate JWT
```

---

### Step 3 — Server returns JWT

```json
{
    "access_token": "eyJhbGciOiJIUzI1Ni..."
}
```

---

### Step 4 — Client sends JWT

```http
GET /users
Authorization: Bearer eyJhbGciOiJIUzI1Ni...
```

---

### Step 5 — Server validates JWT

The server checks things such as:

```text
✓ Signature
✓ Expiration
✓ Issuer, if required
✓ Audience, if required
✓ Required claims
```

---

### Step 6 — Authorization

After authentication succeeds:

```text
Who is this?
      ↓
User 123

What can User 123 do?
      ↓
role = employee
```

Then the API checks permissions.

---

# 9. Access Token

The JWT used to access protected APIs is commonly called an **access token**.

For example:

```text
Access Token
     ↓
GET /users
GET /orders
GET /profile
```

Access tokens are often intentionally short-lived.

For example:

```text
Access token
     ↓
Expires after a relatively short period
```

This limits the damage if a token is stolen.

---

# 10. Refresh Token

If the access token expires, you don't necessarily want the user to log in again every few minutes.

That's where a **refresh token** can be used.

Conceptually:

```text
Login
  ↓
Access Token + Refresh Token
  ↓
Client
```

Access token:

```text
Used for API requests
Shorter lifetime
```

Refresh token:

```text
Used to obtain a new access token
Longer lifetime
```

Flow:

```text
             Access Token
Client ─────────────────────> API
       expired
          ↓
Client ─── Refresh Token ────> Auth Server
                                  │
                                  ↓
                            New Access Token
                                  │
Client <─────────────────────────┘
```

---

# 11. Why Not Make the Access Token Last Forever?

Suppose:

```text
JWT expires in 10 minutes
```

If stolen, the attacker may have a limited window.

But if:

```text
JWT expires in 10 years
```

a stolen token could remain useful for a very long time.

So token lifetime is an important security design decision.

---

# 12. JWT vs Session

You'll encounter two common approaches.

### Traditional session

```text
Client
  ↓
Login
  ↓
Server creates session
  ↓
Session stored server-side
  ↓
Client gets session cookie
```

Server maintains session state.

### JWT-based approach

```text
Client
  ↓
Login
  ↓
Server generates JWT
  ↓
Client stores token
  ↓
Client sends JWT with requests
```

The server can validate the token without maintaining the same kind of server-side session for each client.

This fits nicely with stateless API designs.

---

# 13. JWT Does Not Automatically Mean "Secure"

Using JWT doesn't magically make an API secure.

You still need to think about:

```text
✓ HTTPS
✓ Token expiration
✓ Strong signing keys
✓ Secure token storage
✓ Proper validation
✓ Authorization checks
✓ Token revocation strategy where needed
```

For example, this is dangerous:

```python
SECRET_KEY = "password123"
```

A signing secret should be generated and managed securely, typically through environment/configuration management or a secrets manager.

---

# 14. Authentication vs JWT vs Authorization

Keep these concepts separate:

```text
Authentication
      ↓
JWT can be used as a credential/token
      ↓
Verify identity
      ↓
Authorization
      ↓
Check permissions
```

JWT is **one mechanism used in authentication**, not a synonym for authentication itself.

---

# 15. FastAPI Connection

Eventually, you'll build something like:

```python
@app.post("/login")
def login(...):
    ...
```

and protected endpoints like:

```python
@app.get("/users")
def get_users(...):
    ...
```

FastAPI provides security utilities that can extract a bearer token from:

```http
Authorization: Bearer <token>
```

Then your application verifies the token and identifies the user.

We'll implement this later rather than jumping into security code now.

---

## The JWT Mental Model

Remember this flow:

```text
┌──────────────┐
│ Login        │
└──────┬───────┘
       ↓
Validate credentials
       ↓
Generate JWT
       ↓
┌──────────────┐
│ Access Token │
└──────┬───────┘
       ↓
Authorization: Bearer <JWT>
       ↓
Validate JWT
       ↓
Identify user
       ↓
Check permissions
       ↓
Return API response
```

And:

```text
JWT
├── Header
├── Payload
└── Signature
```

### Phase 2 is now essentially complete.

Next, we'll move into **Phase 3: Building REST APIs with FastAPI**, starting with **setting up FastAPI and creating your first GET endpoint**.
