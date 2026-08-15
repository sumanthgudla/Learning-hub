# Phase 2 — Topic 2: Authentication vs Authorization

This is one of the **most important concepts** in Azure security and REST APIs.

The simplest way to remember it:

> **Authentication = Who are you?**
> **Authorization = What are you allowed to do?**

---

# 1. Authentication

Authentication verifies the identity of whoever is making the request.

For example, when you log in:

```text
Username + Password
       ↓
Microsoft Entra ID
       ↓
Identity verified ✅
```

The system now knows:

> "This is Sumanth."

For an application, it's similar:

```text
Python Application
       ↓
Microsoft Entra ID
       ↓
Application identity verified ✅
```

---

# 2. Authorization

Once the identity is known, we ask:

> **What is this identity allowed to do?**

For example:

```text
Application A
    │
    ├── Read secrets       ✅
    ├── Create secrets     ❌
    ├── Delete secrets     ❌
    └── Manage Key Vault   ❌
```

The identity is authenticated, but it has limited permissions.

That's authorization.

---

# 3. Simple real-world example

Think about an office building.

### Authentication

You show your employee badge.

```text
Security Guard
      ↓
"Who are you?"
      ↓
Employee verified ✅
```

### Authorization

The badge determines which rooms you can enter.

```text
Employee
   │
   ├── Office       ✅
   ├── Cafeteria    ✅
   ├── Server Room  ❌
   └── CEO Office   ❌
```

So:

```text
Badge = Authentication
Room permissions = Authorization
```

---

# 4. How this applies to Key Vault

Suppose your Python application wants:

```python
secret = client.get_secret("OPENAI-API-KEY")
```

Two things happen conceptually.

### Authentication

Key Vault asks:

> "Who is making this request?"

The application authenticates using its identity.

```text
Application
    ↓
Managed Identity
    ↓
Microsoft Entra ID
    ↓
Identity Token
```

### Authorization

Key Vault then asks:

> "Is this identity allowed to read secrets?"

Azure RBAC determines that.

```text
Identity
   ↓
RBAC
   ↓
Allowed to read secrets? 
   ↓
YES → return secret
NO  → deny request
```

---

# 5. Complete flow

```text
                 Authentication
                       │
                       ▼
Application ──────► Entra ID
                       │
                       │ Token
                       ▼
                    Key Vault
                       │
                       │
                 Authorization
                       │
                       ▼
                     RBAC
                       │
                 ┌─────┴─────┐
                 │           │
                YES          NO
                 │           │
                 ▼           ▼
             Secret       Denied
```

---

# 6. Authentication does NOT mean access

This is a very important point.

Imagine:

```text
Application A
     │
     ▼
Entra ID
     │
     ▼
Authenticated ✅
```

That does **not** automatically mean:

```text
Application A
     │
     ▼
Read every Key Vault secret
```

No.

It still needs authorization.

```text
Authentication
       ↓
"I know who you are."
       ↓
Authorization
       ↓
"Now I'll check what you're allowed to do."
```

---

# 7. 401 vs 403

This connects directly to REST APIs.

### 401 Unauthorized

Usually means:

> **The request isn't successfully authenticated.**

For example:

```text
No valid token
Invalid/expired token
Missing authentication
```

Conceptually:

```text
Application
   ↓
Key Vault
   ↓
❌ "I don't know who you are."
```

Result:

```text
401
```

---

### 403 Forbidden

Means:

> **I know who you are, but you're not allowed to do this.**

Example:

```text
Application
   ↓
Entra ID
   ↓
Authenticated ✅
   ↓
Key Vault
   ↓
RBAC
   ↓
No permission ❌
```

Result:

```text
403
```

So remember:

```text
401 → Authentication problem
403 → Authorization problem
```

---

# 8. Example

Suppose:

```text
MyGenAIApp
```

has a Managed Identity.

It requests:

```text
OPENAI-API-KEY
```

### Case 1 — No valid identity

```text
MyGenAIApp
     ↓
Key Vault
     ↓
Can't authenticate
     ↓
401 ❌
```

### Case 2 — Valid identity, no permission

```text
MyGenAIApp
     ↓
Entra ID
     ↓
Identity verified ✅
     ↓
Key Vault
     ↓
RBAC
     ↓
Secret read permission? NO
     ↓
403 ❌
```

### Case 3 — Valid identity + permission

```text
MyGenAIApp
     ↓
Entra ID
     ↓
Identity verified ✅
     ↓
Key Vault
     ↓
RBAC
     ↓
Permission ✅
     ↓
Secret returned
```

---

# 9. Authentication in Azure

There are several ways an application can authenticate to Azure.

You'll encounter:

```text
Managed Identity
Service Principal
Azure CLI login
Developer credentials
```

For production Azure-to-Azure communication, **Managed Identity** is especially important.

For example:

```text
Azure App Service
       │
       ▼
Managed Identity
       │
       ▼
Entra ID
```

We'll cover this next.

---

# 10. Authorization in Azure

Azure commonly uses **Azure RBAC**.

RBAC stands for:

> **Role-Based Access Control**

Instead of saying:

```text
Application A can do everything.
```

you assign a role.

For example, conceptually:

```text
Application A
      │
      ▼
Key Vault Secrets User
      │
      ▼
Can read secrets
```

While another identity might have:

```text
Key Vault Administrator
```

with much broader permissions.

The exact built-in roles and their scopes matter, and we'll cover those when we reach RBAC.

---

# 11. Why least privilege matters

Suppose your application only needs:

```text
Read OPENAI-API-KEY
```

Don't give it:

```text
Read
Write
Delete
Manage access
Manage vault
```

Instead:

```text
Application
    │
    ▼
Minimum required permission
```

This is called:

> **Principle of Least Privilege**

If your application is compromised, the damage is limited.

---

# 12. Interview question

### Interviewer:

> "What's the difference between authentication and authorization?"

A strong answer:

> **"Authentication verifies the identity of the user or application, while authorization determines what that authenticated identity is allowed to access or perform. In Azure Key Vault, Microsoft Entra ID can authenticate an application's identity, and Azure RBAC determines whether that identity has permission to read or manage secrets."**

If they ask:

> "What's the difference between 401 and 403?"

Answer:

> **"401 generally indicates an authentication problem, while 403 indicates that the caller is authenticated but doesn't have permission to perform the requested operation."**

---

# 13. Mental model

Keep this diagram in your head:

```text
             WHO ARE YOU?
                  │
                  ▼
        Microsoft Entra ID
                  │
                  │
                  ▼
           Authentication
                  │
                  ▼
           Access Token
                  │
                  ▼
             Key Vault
                  │
                  │
                  ▼
          WHAT CAN YOU DO?
                  │
                  ▼
              Azure RBAC
                  │
          ┌───────┴───────┐
          │               │
        Allowed         Denied
          │               │
          ▼               ▼
       Secret            403
```

---

## Next: Phase 2 — Topic 3: Managed Identity

This is probably the **single most important Key Vault concept for Azure interviews**.

We'll cover:

* What Managed Identity actually is
* Why it exists
* System-assigned vs user-assigned identity
* How Azure creates the identity
* How Entra ID fits in
* How your Python application uses it
* Why you don't need to store a client secret
* A complete App Service → Key Vault example
