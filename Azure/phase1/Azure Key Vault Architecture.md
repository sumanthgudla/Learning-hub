# Phase 1 — Topic 4: Azure Key Vault Architecture

Now let's understand **how Azure Key Vault actually works**.

So far we know:

```text
Key Vault
├── Secrets
├── Keys
└── Certificates
```

But the important question is:

> **How does my Python application securely get a secret from Key Vault?**

---

# 1. The basic architecture

Imagine your GenAI application:

```text
┌──────────────────────┐
│   Python Application │
│                      │
│  FastAPI / LangGraph │
└──────────┬───────────┘
           │
           │ "Give me OPENAI-API-KEY"
           ▼
┌──────────────────────┐
│    Azure Key Vault   │
│                      │
│  OPENAI-API-KEY      │
│  DB-PASSWORD         │
│  API-SECRET           │
└──────────────────────┘
```

But Key Vault doesn't blindly give the secret to anyone.

It first asks:

> **Who are you?**

and then:

> **Are you allowed to access this secret?**

That gives us two major concepts:

```text
Authentication
      +
Authorization
```

---

# 2. Authentication

Authentication answers:

> **Who are you?**

For example, your application might identify itself using:

```text
Microsoft Entra ID
       │
       ▼
Managed Identity
```

Conceptually:

```text
Python Application
       │
       │ "I am application X"
       ▼
Microsoft Entra ID
       │
       │ Identity token
       ▼
Azure Key Vault
```

Key Vault can then identify the caller.

---

# 3. Authorization

Authentication alone isn't enough.

Suppose Key Vault knows:

```text
Application = MyGenAIApp
```

It still needs to determine:

> "Is MyGenAIApp allowed to read this secret?"

That's **authorization**.

For example:

```text
MyGenAIApp
    │
    ├── Read OPENAI-API-KEY     ✅
    ├── Read DB-PASSWORD        ❌
    └── Delete secrets          ❌
```

This is where **Azure RBAC** comes in.

We'll study RBAC in Phase 2.

---

# 4. Authentication + Authorization

This is one of the most important concepts to remember:

```text
Authentication
      ↓
"Who are you?"
      ↓
Authorization
      ↓
"What are you allowed to do?"
```

For example:

```text
Application
    │
    │ Authentication
    ▼
Microsoft Entra ID
    │
    │ Identity
    ▼
Azure Key Vault
    │
    │ Authorization / RBAC
    ▼
Secret
```

---

# 5. What is Microsoft Entra ID?

You may hear **Azure Active Directory (Azure AD)** in older tutorials.

The service was renamed to:

**Microsoft Entra ID**

It is Microsoft's identity and access-management service.

It manages identities such as:

```text
Users
Applications
Services
Managed identities
Service principals
```

For our Key Vault example, Entra ID helps establish:

> "This request is coming from this particular application identity."

---

# 6. What is Managed Identity?

This is **extremely important** for Azure interviews.

Suppose you deploy your Python application to Azure App Service.

You don't want to give the application another credential just so it can access Key Vault.

For example, you don't want:

```text
Python App
    │
    ├── Client ID
    ├── Client Secret
    └── Tenant ID
```

because now you've created **another secret that needs to be protected**.

Instead, Azure can provide the application with a **Managed Identity**.

Conceptually:

```text
Azure App Service
       │
       │ has
       ▼
Managed Identity
       │
       ▼
Microsoft Entra ID
       │
       ▼
Azure Key Vault
```

The identity is managed by Azure.

This removes the need for your application to manually manage credentials for authenticating to Azure resources.

We'll go deeply into Managed Identity in **Phase 2**.

---

# 7. Complete request flow

Now let's put everything together.

Suppose your Python application executes:

```python
secret = client.get_secret("OPENAI-API-KEY")
```

What conceptually happens?

### Step 1 — Application needs the secret

```text
Python Application
       │
       │ get_secret()
       ▼
```

### Step 2 — Application authenticates

The application uses an identity mechanism such as Managed Identity.

```text
Application
       │
       ▼
Microsoft Entra ID
```

### Step 3 — Entra ID provides an access token

Conceptually:

```text
Application
       │
       │ authentication
       ▼
Entra ID
       │
       │ access token
       ▼
Application
```

### Step 4 — Application calls Key Vault

```text
Application
       │
       │ token + request
       ▼
Azure Key Vault
```

### Step 5 — Key Vault checks permissions

```text
Is this identity allowed
to read this secret?
```

If:

```text
YES → return secret
NO  → return authorization error
```

### Step 6 — Application receives the secret

```text
Azure Key Vault
       │
       │ secret
       ▼
Python Application
```

---

# 8. Complete architecture

Put everything together:

```text
                         Azure
                          │
                ┌─────────▼──────────┐
                │  Microsoft Entra ID│
                │                    │
                │  Application       │
                │  Identity          │
                └─────────▲──────────┘
                          │
                    Access Token
                          │
                          │
┌─────────────────┐       │
│ Python / GenAI  │───────┼──────────────┐
│ Application     │       │              │
└─────────────────┘       │              │
                          │              ▼
                          │      ┌─────────────────┐
                          └─────►│  Azure Key Vault│
                                 │                 │
                                 │ OPENAI_API_KEY  │
                                 │ DB_PASSWORD     │
                                 │ API_SECRET      │
                                 └─────────────────┘
                                          │
                                          ▼
                                    Secret returned
```

---

# 9. Where does RBAC fit?

RBAC controls permissions.

For example:

```text
Managed Identity
       │
       ▼
Azure RBAC
       │
       ├── Can read secrets?       ✅
       ├── Can write secrets?     ❌
       └── Can delete secrets?    ❌
```

This follows the **principle of least privilege**:

> Give an application only the permissions it actually needs.

For example, if your application only needs to read an API key, don't give it permission to delete every secret in the vault.

---

# 10. A real GenAI example

Imagine you deploy your RAG application:

```text
                  Azure
                    │
          ┌─────────▼──────────┐
          │     App Service    │
          │                    │
          │ Python + LangGraph │
          └─────────┬──────────┘
                    │
             Managed Identity
                    │
                    ▼
          ┌────────────────────┐
          │   Microsoft Entra  │
          │        ID          │
          └─────────┬──────────┘
                    │
               Access Token
                    │
                    ▼
          ┌────────────────────┐
          │    Azure Key Vault │
          │                    │
          │ AZURE-OPENAI-KEY   │
          │ DB-PASSWORD        │
          └────────────────────┘
```

Your Python code doesn't need to contain:

```python
CLIENT_SECRET = "..."
```

That's the major security improvement.

---

# 11. Four components you should remember

For Azure Key Vault, keep this mental model:

```text
1. Key Vault
      ↓
Stores secrets/keys/certificates

2. Microsoft Entra ID
      ↓
Provides identity

3. Managed Identity
      ↓
Allows Azure resources to have an identity

4. RBAC
      ↓
Controls what that identity can do
```

Together:

```text
Managed Identity
       │
       ▼
Entra ID
       │
       ▼
Authentication
       │
       ▼
Key Vault
       │
       ▼
RBAC authorization
       │
       ▼
Secret
```

---

## Interview question

**Interviewer:**

> "How does your Azure-hosted Python application access a secret stored in Azure Key Vault without storing credentials in the application?"

A strong answer:

> "I would enable a Managed Identity for the Azure-hosted application. The application uses that identity to authenticate through Microsoft Entra ID. I would then assign the identity the minimum required Azure RBAC permissions on the Key Vault, such as permission to read secrets. The application can then retrieve the secret using the Azure SDK and `DefaultAzureCredential`, without hardcoding Azure credentials."

That's the **production-level concept** we're building toward.

---

### Next: Phase 1 — Topic 5

**Azure Key Vault vs `.env` vs Environment Variables**

We'll compare them directly and understand **what you should use during local development and what you should use in production**.
