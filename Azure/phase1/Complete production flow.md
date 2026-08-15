# Phase 1 — Topic 6: Complete Real-World Example

Let's put everything together using a **Python + Azure OpenAI application**.

Imagine you're building a RAG application:

```text
User
  ↓
Python / FastAPI
  ↓
LangGraph
  ↓
Azure OpenAI
  ↓
PostgreSQL / pgvector
```

Your application needs credentials for Azure OpenAI and the database.

---

## 1. The bad architecture

A beginner might write:

```python
from openai import AzureOpenAI

client = AzureOpenAI(
    api_key="my-secret-key",
    azure_endpoint="https://my-resource.openai.azure.com/"
)
```

Problem:

```text
Source code
    │
    └── API key ❌
         │
         ├── Git
         ├── GitHub
         ├── Backups
         └── Developer machines
```

Never commit secrets like this.

---

# 2. Better: `.env` locally

During development:

```text
.env
```

```text
AZURE_OPENAI_API_KEY=xxxxxxxx
AZURE_OPENAI_ENDPOINT=https://my-resource.openai.azure.com/
```

Python:

```python
import os

api_key = os.getenv("AZURE_OPENAI_API_KEY")
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
```

This is convenient for your laptop.

But now imagine deploying the application to Azure.

We want something better for production.

---

# 3. Production architecture

We'll store the API key in Key Vault:

```text
Azure Key Vault
│
└── AZURE-OPENAI-API-KEY
```

And our application:

```text
Azure App Service
       │
       │ Managed Identity
       ▼
Microsoft Entra ID
       │
       ▼
Azure Key Vault
       │
       │ Secret
       ▼
Python Application
       │
       ▼
Azure OpenAI
```

---

# 4. Step 1 — Create the Key Vault

You create a Key Vault in Azure.

Conceptually:

```text
Resource Group
    │
    └── Key Vault
          │
          ├── Secrets
          ├── Keys
          └── Certificates
```

Let's say the vault is:

```text
my-company-kv
```

Its URL would look conceptually like:

```text
https://my-company-kv.vault.azure.net/
```

---

# 5. Step 2 — Store the secret

Inside the vault:

```text
Secret Name:
AZURE-OPENAI-API-KEY

Secret Value:
xxxxxxxxxxxxxxxx
```

You can also have:

```text
AZURE-OPENAI-ENDPOINT
POSTGRES-PASSWORD
POSTGRES-CONNECTION-STRING
```

So:

```text
my-company-kv
│
├── AZURE-OPENAI-API-KEY
├── AZURE-OPENAI-ENDPOINT
├── POSTGRES-PASSWORD
└── POSTGRES-CONNECTION-STRING
```

---

# 6. Step 3 — Give your application an identity

Suppose your Python application is deployed to:

```text
Azure App Service
```

You enable:

```text
Managed Identity
```

Now Azure gives that application an identity in Microsoft Entra ID.

Conceptually:

```text
App Service
     │
     └── Managed Identity
              │
              ▼
       Microsoft Entra ID
```

Your application now has an Azure identity without you manually storing another password/client secret.

---

# 7. Step 4 — Give the identity permission

Now we have:

```text
Application identity
```

But it doesn't automatically have permission to read Key Vault.

We assign an appropriate Azure RBAC role.

Conceptually:

```text
Managed Identity
       │
       ▼
Azure RBAC
       │
       ▼
Key Vault
       │
       └── Read secret ✅
```

We follow **least privilege**.

If the application only needs to read secrets, don't give it unnecessary administrative permissions.

---

# 8. Step 5 — Python application

Now your Python application can use Azure's identity libraries.

Install:

```bash
pip install azure-identity azure-keyvault-secrets
```

Then:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = "https://my-company-kv.vault.azure.net/"

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=vault_url,
    credential=credential
)

secret = client.get_secret("AZURE-OPENAI-API-KEY")

api_key = secret.value
```

Notice something important.

There is **no Key Vault username/password** in the code.

There is no:

```python
client_secret = "..."
```

The application uses its Azure identity.

---

# 9. What does `DefaultAzureCredential` do?

This is an important concept we'll explore more later.

```python
credential = DefaultAzureCredential()
```

It provides a convenient way for your application to obtain an Azure credential using supported authentication mechanisms.

For example, during local development it may use your developer's Azure login.

When running on an Azure resource with Managed Identity, it can use that managed identity.

Conceptually:

```text
Local development
      │
      ▼
Developer Azure identity


Production
      │
      ▼
Managed Identity
```

Your application code can remain largely the same.

That's one of the reasons `DefaultAzureCredential` is so useful.

---

# 10. The complete request

When this runs:

```python
secret = client.get_secret("AZURE-OPENAI-API-KEY")
```

the conceptual flow is:

```text
1. Python application
        │
        │ I need the secret
        ▼

2. DefaultAzureCredential
        │
        │ authenticate
        ▼

3. Microsoft Entra ID
        │
        │ identity/access token
        ▼

4. Azure Key Vault
        │
        │ check authorization
        ▼

5. Azure RBAC
        │
        │ allowed?
        ▼

6. Key Vault
        │
        │ return secret
        ▼

7. Python application
```

Then your application can use the credential to call Azure OpenAI.

---

# 11. Full architecture

Putting everything together:

```text
                         Azure
                           │
                           │
                  ┌────────▼─────────┐
                  │ Microsoft Entra  │
                  │       ID         │
                  └────────▲─────────┘
                           │
                     Identity Token
                           │
                           │
┌──────────────────┐       │       ┌──────────────────┐
│  Azure App       │       │       │   Azure Key      │
│    Service       │───────┼──────►│     Vault        │
│                  │       │       │                  │
│ Python +         │       │       │ OPENAI-API-KEY   │
│ LangGraph + RAG  │       │       │ DB-PASSWORD      │
└────────┬─────────┘       │       └──────────────────┘
         │
         │ API Key
         ▼
┌──────────────────┐
│   Azure OpenAI   │
└──────────────────┘
```

---

# 12. What happens if someone tries to access the secret?

Suppose another application:

```text
BadApplication
```

tries:

```text
get_secret("AZURE-OPENAI-API-KEY")
```

Key Vault checks its identity and permissions.

If it doesn't have the required permission:

```text
BadApplication
      │
      ▼
Key Vault
      │
      ▼
❌ Authorization denied
```

This is why **authentication + authorization** are both required.

---

# 13. Why this is better

Compare the two architectures.

### Bad

```text
Python
  │
  └── API key hardcoded
```

### Better

```text
Python
  │
  └── .env
```

### Production

```text
Python
   │
   ▼
Managed Identity
   │
   ▼
Entra ID
   │
   ▼
RBAC
   │
   ▼
Key Vault
   │
   ▼
Secret
```

The production architecture gives you:

* Centralized secret management
* Identity-based access
* Least-privilege permissions
* Auditing
* Secret rotation/versioning
* No hardcoded Azure credentials

---

# 14. Interview scenario

Imagine you're asked:

> **"You have built a LangGraph RAG application using Azure OpenAI. How would you securely store the Azure OpenAI credentials in production?"**

You can answer:

> "I would store the Azure OpenAI credential as a secret in Azure Key Vault. If the application is deployed to an Azure service such as App Service or AKS, I would use Managed Identity for the application. The identity would authenticate through Microsoft Entra ID, and I would assign the minimum required Key Vault RBAC permissions, such as reading secrets. In Python, I would use `DefaultAzureCredential` with the Azure Key Vault SDK to retrieve the secret. I would avoid hardcoding the credential or committing it to source control."

That's a solid production answer.

---

# Phase 1 Complete ✅

You now understand:

```text
Topic 1 → What is Key Vault?
Topic 2 → Why not hardcode secrets?
Topic 3 → Secrets vs Keys vs Certificates
Topic 4 → Key Vault architecture
Topic 5 → Key Vault vs .env/environment variables
Topic 6 → Complete production flow
```

Now we're ready for the **most important phase**.

# Phase 2 — Authentication & Authorization

We'll learn:

```text
1. Microsoft Entra ID
2. Authentication vs Authorization
3. Managed Identity
4. System-assigned vs User-assigned Managed Identity
5. Service Principal
6. Client ID / Tenant ID / Client Secret
7. Azure RBAC
8. Key Vault roles
9. Least privilege
10. Complete authentication flow
```

### Next topic: **Microsoft Entra ID**

This is the foundation for understanding **Managed Identity and how your application gets permission to access Key Vault**.
