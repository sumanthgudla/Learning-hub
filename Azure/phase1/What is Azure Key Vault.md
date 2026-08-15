# Phase 1 — Topic 1: What is Azure Key Vault?

**Azure Key Vault is a cloud service from Microsoft Azure used to securely store and control access to sensitive information.**

Think of it as a **secure digital locker for your application's secrets**.

### 1. The problem

Suppose your Python GenAI application calls Azure OpenAI:

```python
client = AzureOpenAI(
    api_key="abc123-secret-key"
)
```

The problem is that the secret is inside your source code.

If you push this to Git:

```text
GitHub
   ↓
Source code
   ↓
api_key = "abc123"
```

Someone who gets access to the repository could potentially get your API key.

Even using an environment variable:

```python
api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

is better, but you still need to figure out **where that environment variable's secret comes from and how to manage it securely in production**.

That's where Key Vault comes in.

---

# 2. What does Key Vault store?

There are three major types of objects:

### Secrets

Used for things like:

```text
API keys
Database passwords
Connection strings
Application secrets
Tokens
```

Example:

```text
Name: AZURE_OPENAI_API_KEY
Value: xxxxxxxxxxxxxxxxx
```

### Keys

Cryptographic keys used for operations such as:

```text
Encryption
Decryption
Signing
Verification
```

These are different from ordinary API secrets.

### Certificates

Used for things such as:

```text
TLS/SSL
Application authentication
Certificate-based security
```

So remember:

```text
Azure Key Vault
│
├── Secrets
├── Keys
└── Certificates
```

---

# 3. How your application uses it

Imagine your GenAI application needs an Azure OpenAI credential.

Instead of:

```text
Python application
      │
      └── API key hardcoded ❌
```

you do:

```text
                 Azure
                   │
          ┌────────▼─────────┐
          │   Key Vault      │
          │                  │
          │ OPENAI_API_KEY   │
          │ DB_PASSWORD      │
          │ OTHER_SECRET     │
          └────────▲─────────┘
                   │
                   │
             Secure access
                   │
          ┌────────┴─────────┐
          │ Python Backend   │
          │   GenAI App      │
          └──────────────────┘
```

Your application asks Key Vault:

> "Give me the `OPENAI_API_KEY` secret."

Key Vault verifies that the application is authorized.

If authorized, Key Vault returns the secret.

---

# 4. Important distinction

Key Vault **doesn't replace your application's authentication system**.

For example:

```text
User
 ↓
Your API
 ↓
Authentication
 ↓
Your application
 ↓
Azure Key Vault
```

Key Vault itself also needs to know:

> "Who is this application, and is it allowed to access this secret?"

That's where **Microsoft Entra ID, Managed Identity, Service Principals, and RBAC** come in.

We'll learn those in Phase 2.

---

# 5. Real-world GenAI example

Suppose you build a RAG application:

```text
User
 ↓
FastAPI
 ↓
LangGraph
 ↓
Azure OpenAI
 ↓
PostgreSQL / pgvector
```

You might have:

```text
Azure OpenAI API key
PostgreSQL password
Database connection string
Embedding service credentials
Other third-party API keys
```

Instead of putting them directly in your application:

```python
OPENAI_KEY = "..."
DB_PASSWORD = "..."
```

you can keep them in:

```text
Azure Key Vault
│
├── AZURE-OPENAI-KEY
├── POSTGRES-PASSWORD
├── DATABASE-CONNECTION
└── EMBEDDING-API-KEY
```

Your application retrieves them when needed.

---

# 6. Why companies use Key Vault

The main benefits are:

**Security**

Secrets aren't hardcoded into source code.

**Centralized management**

All sensitive credentials can be managed in one place.

**Access control**

You can specify which applications/users can access which secrets.

**Auditing**

You can monitor access to the vault.

**Secret rotation**

You can change credentials without modifying application source code.

**Integration with Azure**

It works with services such as App Service, AKS, Functions, VMs, Azure OpenAI applications, etc.

---

# 7. One interview question you should know

### Interviewer:

> "Where would you store an Azure OpenAI API key in a production application?"

A good answer:

> "I would store the API key in Azure Key Vault rather than hardcoding it in the application or committing it to source control. The application would authenticate to Azure using Managed Identity, and RBAC would grant it the minimum required permission to retrieve the secret."

That's a **production-level answer**.

---

## The most important concept from today's topic

Remember this:

```text
Hardcoded secret
      ❌
      
.env file
      ⚠️
      
Azure Key Vault
      ✅
      
Key Vault + Managed Identity + RBAC
      ✅✅
```

The **real production architecture** we'll eventually reach is:

```text
                Microsoft Entra ID
                       ▲
                       │
                Managed Identity
                       │
                       │
┌──────────────┐       │       ┌──────────────────┐
│ Python/GenAI │───────┼──────►│  Azure Key Vault │
│ Application  │               │                  │
└──────────────┘               │ OPENAI_KEY       │
                               │ DB_PASSWORD       │
                               └──────────────────┘
```

### Next: Phase 1 — Topic 2

**Why shouldn't we store API keys in code, `.env` files, or configuration files?**

This is important because it explains **why Key Vault is needed in the first place**.
