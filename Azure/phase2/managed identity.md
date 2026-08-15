# Phase 2 — Topic 3: Managed Identity

This is one of the **most important concepts** to understand for Azure Key Vault and Azure production interviews.

The problem Managed Identity solves is:

> **How can an Azure application authenticate to another Azure service without us storing credentials inside the application?**

---

## 1. The problem without Managed Identity

Suppose your Python application is running on Azure App Service:

```text id="8exn8u"
Azure App Service
       │
       ▼
Azure Key Vault
```

The application needs to authenticate to Key Vault.

One approach is to create an application identity with credentials:

```text id="9g6r8x"
Client ID
Client Secret
Tenant ID
```

Then your application might need:

```python id="vpy1yq"
client_id = "..."
client_secret = "..."
tenant_id = "..."
```

But now you have a problem.

### Where do you store `client_secret`?

You need another secret-management solution.

That becomes:

```text id="f4i8qv"
Application
   │
   ├── Key Vault credential ❌
   │
   └── needs Key Vault
          │
          └── circular problem
```

Managed Identity solves this.

---

# 2. What is Managed Identity?

A **Managed Identity is an identity assigned to an Azure resource**, such as:

```text id="4ij8k5"
App Service
Virtual Machine
Azure Functions
AKS
Container Apps
```

Azure manages the identity's credentials for you.

Your application doesn't need to store a password/client secret to authenticate as that identity.

Conceptually:

```text id="9t6v5g"
Azure App Service
       │
       └── Managed Identity
                │
                ▼
        Microsoft Entra ID
```

---

# 3. Think of it like an employee badge

Imagine Azure creates an employee badge for your application.

```text id="3x5lcz"
Azure App Service
       │
       ▼
"Employee badge"
       │
       ▼
Managed Identity
```

When your application wants to access Key Vault:

```text id="l6b9qf"
Application
     │
     │ "This is my identity"
     ▼
Entra ID
     │
     ▼
Token
     │
     ▼
Key Vault
```

Azure knows which application that identity belongs to.

---

# 4. Managed Identity is NOT a Key Vault secret

This distinction is important.

Managed Identity:

```text id="q2q0yj"
Identity
```

Key Vault secret:

```text id="5g4w70"
Sensitive value
```

For example:

```text id="av7e1z"
Managed Identity
      ↓
Identifies your application

Key Vault Secret
      ↓
Contains:
AZURE-OPENAI-API-KEY
```

They serve completely different purposes.

---

# 5. Two types of Managed Identity

There are two types:

```text id="s7v6gk"
Managed Identity
│
├── System-assigned
└── User-assigned
```

Understanding the difference is important.

---

# 6. System-assigned Managed Identity

A system-assigned identity is tied directly to an Azure resource.

For example:

```text id="4qj6i9"
App Service
    │
    └── System-assigned identity
```

Azure creates the identity for that resource.

If you delete the Azure resource, the identity is also removed.

So the lifecycle is:

```text id="r2q8z4"
Create App Service
       ↓
Identity created
       ↓
Use identity
       ↓
Delete App Service
       ↓
Identity deleted
```

### When is this useful?

When one Azure resource needs its own identity.

For example:

```text id="t4jqgk"
App Service A
      │
      └── System-assigned identity
             │
             ▼
         Key Vault
```

Very straightforward.

---

# 7. User-assigned Managed Identity

A user-assigned identity is a **separate Azure resource**.

For example:

```text id="7n9d4s"
User-assigned Managed Identity
             │
        ┌────┴────┐
        │         │
        ▼         ▼
    App Service   VM
```

Multiple Azure resources can use the same identity.

The lifecycle is independent.

```text id="n1zv3k"
User-assigned Identity
        │
        ├── App Service
        ├── Azure Function
        └── VM
```

If you delete the App Service, the identity can remain.

---

# 8. System vs User assigned

Remember this table:

|                               | System-assigned  | User-assigned     |
| ----------------------------- | ---------------- | ----------------- |
| Identity lifecycle            | Tied to resource | Independent       |
| Created with resource         | Usually          | Separate resource |
| Deleted with resource         | Yes              | No                |
| Can be shared                 | No               | Yes               |
| Simple setup                  | ✅                | More flexible     |
| Useful for multiple resources | ❌                | ✅                 |

A simple mental model:

```text id="g0y5hx"
System-assigned
Resource owns identity


User-assigned
Identity exists separately
and can be assigned to resources
```

---

# 9. Real Key Vault example

Suppose you have:

```text id="v4ml8b"
Azure App Service
        │
        │ System-assigned Managed Identity
        ▼
Microsoft Entra ID
        │
        ▼
Azure Key Vault
```

Inside Key Vault:

```text id="2kly8j"
AZURE-OPENAI-API-KEY
```

You assign the application's identity an appropriate Key Vault RBAC role.

Now:

```text id="m2yn2h"
App Service
    │
    │ Managed Identity
    ▼
Entra ID
    │
    │ Token
    ▼
Key Vault
    │
    │ RBAC check
    ▼
Secret
```

No client secret needs to be embedded in your Python code.

---

# 10. What does your Python code look like?

You can use:

```python id="n3db0q"
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url="https://my-vault.vault.azure.net/",
    credential=credential
)

secret = client.get_secret("AZURE-OPENAI-API-KEY")

print(secret.value)
```

The important part is:

```python id="e1u1mt"
DefaultAzureCredential()
```

You aren't doing:

```python id="p3d7kp"
client_secret = "my-secret"
```

Instead, Azure can provide the application identity through Managed Identity when running in Azure.

---

# 11. What happens behind the scenes?

Suppose this line runs:

```python id="j2i7zh"
secret = client.get_secret("AZURE-OPENAI-API-KEY")
```

Conceptually:

### Step 1

Your Python application needs a credential.

```text id="ypuw0u"
Python Application
       ↓
DefaultAzureCredential
```

### Step 2

In Azure, the credential can use the application's Managed Identity.

```text id="a4b8di"
Managed Identity
       ↓
Microsoft Entra ID
```

### Step 3

Entra ID authenticates the identity and provides an access token.

```text id="1thpws"
Entra ID
    ↓
Access Token
```

### Step 4

The application uses that token to call Key Vault.

```text id="p4g4e1"
Python
   │
   │ Token
   ▼
Key Vault
```

### Step 5

Key Vault evaluates permissions.

```text id="1v3rkj"
Identity
   ↓
RBAC
   ↓
Can read secret?
```

If yes:

```text id="s6pkqf"
Secret returned ✅
```

---

# 12. Why is this better?

Without Managed Identity:

```text id="j8x9k7"
Python
   │
   └── Client Secret
          │
          ▼
       Entra ID
```

Now you have to protect:

```text
client_secret
```

With Managed Identity:

```text id="u8s9zw"
Python
   │
   ▼
Managed Identity
   │
   ▼
Entra ID
```

Azure handles the identity credentials.

Therefore:

> **You don't need to manually manage a long-lived client secret for the Azure resource's identity.**

---

# 13. Managed Identity does NOT automatically grant access

This is another critical point.

Suppose you enable Managed Identity:

```text id="z2d9x0"
App Service
    │
    └── Managed Identity ✅
```

You might think:

> "Now it can access Key Vault."

**Not necessarily.**

The identity exists, but it still needs authorization.

You must assign appropriate permissions.

```text id="n8o2k4"
Managed Identity
       │
       ▼
Azure RBAC
       │
       ▼
Key Vault
       │
       ▼
Secret
```

So:

```text id="8xw7h0"
Managed Identity
      +
RBAC permission
      =
Authorized Key Vault access
```

---

# 14. This is the architecture you should remember

```text id="8g1g2x"
                Azure
                  │
        ┌─────────▼──────────┐
        │    App Service     │
        │                    │
        │  Python / FastAPI  │
        └─────────┬──────────┘
                  │
           Managed Identity
                  │
                  ▼
        ┌────────────────────┐
        │ Microsoft Entra ID │
        └─────────┬──────────┘
                  │
             Access Token
                  │
                  ▼
        ┌────────────────────┐
        │   Azure Key Vault  │
        │                    │
        │ OPENAI-API-KEY     │
        │ DB-PASSWORD        │
        └────────────────────┘
```

And authorization happens at Key Vault through Azure RBAC.

---

# 15. Interview question

### Interviewer:

> "Why would you use Managed Identity instead of a Service Principal with a client secret?"

A strong answer:

> "Managed Identity allows an Azure resource to authenticate to other Azure services without the application having to store and manage a client secret. Azure manages the identity credentials, which reduces secret-management overhead and the risk of credential leakage. I would then use Azure RBAC to give that identity only the permissions it needs."

---

## One thing to memorize

Don't say:

> **"Managed Identity gives access to Key Vault."**

Say:

> **"Managed Identity provides an identity that the Azure resource can use to authenticate. We still need to authorize that identity with the appropriate permissions, such as Azure RBAC roles on Key Vault."**

That's a much more accurate production-level understanding.

---

# Next: Phase 2 — Topic 4

**System-assigned vs User-assigned Managed Identity — in depth**

We'll use a real example with:

```text
1 App → 1 Key Vault
3 Apps → 1 Key Vault
Dev / QA / Production
Multiple Azure resources
```

and understand **when you would actually choose system-assigned vs user-assigned identity**.
