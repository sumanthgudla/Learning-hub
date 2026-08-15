# Phase 2 — Topic 6: Tenant ID, Client ID, Client Secret, Object ID & Access Token

These terms are confusing because Azure tutorials often throw all of them at you together.

Let's separate them clearly.

---

# 1. Tenant ID

A **Tenant ID** identifies your Microsoft Entra ID tenant.

Think of a tenant as your organization's identity boundary.

For example:

```text
Your Company
     │
     ▼
Microsoft Entra Tenant
     │
     └── Tenant ID
```

It is typically a GUID-like value:

```text
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

### Think:

> **Tenant ID = Which organization's Entra ID directory?**

---

# 2. Client ID

A **Client ID** identifies an application registration in Microsoft Entra ID.

Suppose you create:

```text
MyGenAIApplication
```

Entra ID gives the application an identifier:

```text
Client ID
```

Conceptually:

```text
Microsoft Entra ID
      │
      └── MyGenAIApplication
                │
                └── Client ID
```

### Think:

> **Client ID = Which application?**

---

# 3. Client Secret

A **Client Secret** is a credential that an application can use to prove its identity.

Think of it like an application password.

```text
Application
     │
     ├── Client ID
     └── Client Secret
```

The application sends these to Entra ID to authenticate.

### Important

The Client Secret is **sensitive**.

Unlike:

```text
Tenant ID
Client ID
```

which are generally identifiers, the:

```text
Client Secret
```

must be protected.

---

# 4. Putting them together

Suppose you have:

```text
Tenant ID       → Company/Entra directory
Client ID       → Your application
Client Secret   → Application credential
```

The authentication flow conceptually looks like:

```text
Python Application
       │
       │ Tenant ID
       │ Client ID
       │ Client Secret
       ▼
Microsoft Entra ID
       │
       │ authenticate application
       ▼
Access Token
```

The application then uses the access token to call an Azure service.

---

# 5. What is an Access Token?

An **access token** is a credential issued by the identity provider that the application presents when calling a protected service.

Conceptually:

```text
Application
     │
     │ "I want to authenticate"
     ▼
Entra ID
     │
     │ Access Token
     ▼
Application
     │
     │ Token
     ▼
Azure Key Vault
```

The access token contains information about the authenticated identity and the intended audience/scope of the token.

You generally don't manually create the token yourself.

Entra ID issues it.

---

# 6. API key vs Access Token

This is important because you've been learning about API keys and tokens.

### API key

Usually:

```text id="9kq7q1"
Static credential
```

Example:

```text
abc123xyz
```

You send it to the API.

### Access token

Usually:

```text id="s3k5de"
Short-lived credential
```

issued by an identity provider.

Conceptually:

```text id="5z4q9j"
Credentials
     ↓
Entra ID
     ↓
Access Token
     ↓
Azure Service
```

So:

```text id="i7g6g8"
API Key
→ Application/service credential


Access Token
→ Credential issued by an identity provider
```

---

# 7. What is Object ID?

This one causes a lot of confusion.

There can be multiple IDs associated with an Azure identity.

For example:

```text id="t4y2d6"
Client ID
Object ID
Tenant ID
```

They are **not interchangeable**.

### Client ID

Identifies the application registration.

Think:

> "Which application is this?"

### Object ID

Identifies a particular object in the Entra ID directory.

For example, a service principal has its own object ID.

Think:

> "Which specific directory object is this?"

### Tenant ID

Identifies the Entra ID directory.

Think:

> "Which organization/directory?"

---

# 8. Simple analogy

Imagine a university.

```text id="h4m7qf"
University
    │
    └── University ID
```

That's like:

```text id="q6x0ab"
Tenant ID
```

Now imagine an application:

```text id="7b1t3p"
Student Application
    │
    └── Application ID
```

That's similar to:

```text id="j5p0s7"
Client ID
```

And the specific directory object representing that application:

```text id="1b8s6n"
Directory Object
    │
    └── Object ID
```

The exact Azure object relationships are more nuanced, but this gives you the right mental model.

---

# 9. Service Principal example

Suppose:

```text id="x2f3t4"
Application:
MyGenAIApp
```

In Entra ID, you might have:

```text id="q0v1j8"
Tenant ID
    ↓
Your organization

Client ID
    ↓
MyGenAIApp application

Service Principal
    ↓
Tenant-specific application identity

Object ID
    ↓
ID of that service principal object
```

Then:

```text id="p7v2y1"
Client Secret
    ↓
Credential used by the application
```

And after authentication:

```text id="u9w4s5"
Access Token
    ↓
Used to call Azure services
```

---

# 10. Managed Identity makes this simpler

This is one reason Managed Identity is attractive.

With a traditional Service Principal:

```text id="2xj9va"
Application
   │
   ├── Tenant ID
   ├── Client ID
   └── Client Secret
   │
   ▼
Entra ID
```

With Managed Identity:

```text id="7f3m2q"
Azure Resource
      │
      ▼
Managed Identity
      │
      ▼
Entra ID
      │
      ▼
Access Token
```

Your application doesn't need to manage a client secret for this Azure authentication flow.

---

# 11. Python example

With a Service Principal:

```python id="p2s8k4"
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)
```

Then:

```python id="5k9q2m"
from azure.keyvault.secrets import SecretClient

client = SecretClient(
    vault_url=vault_url,
    credential=credential
)
```

With a Managed Identity:

```python id="3v7n1x"
from azure.identity import DefaultAzureCredential

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=vault_url,
    credential=credential
)
```

Notice how the second approach doesn't require you to put:

```text id="d8y5k2"
Client Secret
```

into your application.

---

# 12. The complete Service Principal flow

```text id="5f8m2v"
                    Your Application
                          │
                          │
              ┌───────────┼───────────┐
              │           │           │
          Tenant ID    Client ID   Client Secret
              │           │           │
              └───────────┼───────────┘
                          ▼
                  Microsoft Entra ID
                          │
                          │ Authenticate
                          ▼
                    Access Token
                          │
                          ▼
                    Azure Key Vault
                          │
                          ▼
                    RBAC Check
                          │
                     ┌────┴────┐
                     │         │
                    YES        NO
                     │         │
                     ▼         ▼
                  Secret     403
```

---

# 13. The complete Managed Identity flow

```text id="z5r6v8"
                 Azure App Service
                        │
                        ▼
                Managed Identity
                        │
                        ▼
                Microsoft Entra ID
                        │
                        │ Access Token
                        ▼
                  Azure Key Vault
                        │
                        ▼
                    RBAC Check
                        │
                   ┌────┴────┐
                   │         │
                  YES        NO
                   │         │
                   ▼         ▼
                Secret      403
```

This is the flow you should be comfortable explaining in a Senior AI Engineer interview.

---

# 14. What you should memorize

| Term              | Meaning                                                          |
| ----------------- | ---------------------------------------------------------------- |
| **Tenant ID**     | Identifies the Entra ID directory                                |
| **Client ID**     | Identifies an application registration                           |
| **Client Secret** | Credential used by an application                                |
| **Object ID**     | Identifies a specific directory object                           |
| **Access Token**  | Credential issued by Entra ID for accessing a protected resource |

And:

```text id="j8d4x1"
Tenant ID
   ↓
Which organization?

Client ID
   ↓
Which application?

Client Secret
   ↓
Prove application's identity

Access Token
   ↓
Credential used to call the service
```

---

# 15. Interview question

### "What is the difference between Client ID and Client Secret?"

Answer:

> **"The Client ID identifies the application, while the Client Secret is a credential used by the application to authenticate. The Client ID is generally not treated as a secret, whereas the Client Secret must be protected."**

### "What is the difference between Client ID and Object ID?"

Answer:

> **"The Client ID identifies the application registration, while the Object ID identifies a specific object in the Entra ID directory, such as a service principal."**

---

## Phase 2 progress

We've covered:

```text
✅ Entra ID
✅ Authentication vs Authorization
✅ Managed Identity
✅ System vs User-assigned Identity
✅ Service Principal
✅ Tenant ID
✅ Client ID
✅ Client Secret
✅ Object ID
✅ Access Token
```

The next major piece is **Azure RBAC**.

# Next: Phase 2 — Topic 7: Azure RBAC

We'll learn:

**Role → Permission → Scope → Assignment**

and then apply it to:

**Managed Identity → Key Vault → Secret**

This is where you'll understand exactly **how Azure decides whether your application is allowed to read a secret**.
