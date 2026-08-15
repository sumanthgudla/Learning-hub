# Phase 3 — Topic 1: Create and Store Secrets in Azure Key Vault

Now we move from **concepts → practical usage**.

Our goal is to build this:

```text
                    Azure
                      │
                ┌─────┴─────┐
                │            │
          App Service    Key Vault
                             │
                    ┌────────┼────────┐
                    │        │        │
                 OpenAI    DB-PWD   Third-Party
                   Key
```

We'll start with the simplest thing: **creating a Key Vault and storing a secret.**

---

# 1. What is a Secret?

A secret is sensitive information that your application needs.

Examples:

```text
OPENAI_API_KEY
DATABASE_PASSWORD
STRIPE_API_KEY
THIRD_PARTY_API_KEY
JWT_SECRET
```

Instead of:

```python
OPENAI_API_KEY = "sk-xxxxxxxx"
```

you store:

```text
Azure Key Vault
    │
    └── OPENAI_API_KEY
```

Your application retrieves it when needed.

---

# 2. Create a Key Vault

You can create a Key Vault through the Azure Portal.

Search:

```text
Azure Portal
    ↓
Key Vaults
    ↓
Create
```

You'll provide things such as:

```text
Subscription
Resource Group
Key Vault Name
Region
Pricing/Configuration
```

For example:

```text
Name:
sumanth-prod-kv
```

Azure will give you a vault URI similar to:

```text
https://sumanth-prod-kv.vault.azure.net/
```

Your application will use this URI to identify the vault.

---

# 3. Create a secret

Inside the Key Vault:

```text
Key Vault
   ↓
Objects
   ↓
Secrets
   ↓
Generate/Import
```

Suppose you want to store your Azure OpenAI credential.

Name:

```text
AZURE-OPENAI-API-KEY
```

Value:

```text
xxxxxxxxxxxxxxxxxxxx
```

Then save it.

Your Key Vault now contains:

```text
sumanth-prod-kv
     │
     └── AZURE-OPENAI-API-KEY
```

---

# 4. Important: Secret name vs secret value

These are different.

```text
Secret Name
    ↓
AZURE-OPENAI-API-KEY

Secret Value
    ↓
xxxxxxxxxxxxxxxxxxxx
```

The **name** identifies the secret.

The **value** is the sensitive credential.

For example:

```python
secret = client.get_secret("AZURE-OPENAI-API-KEY")
```

Then:

```python
secret.value
```

contains the actual secret.

---

# 5. Secret versions

This is very important for production.

Suppose your secret is initially:

```text
AZURE-OPENAI-API-KEY
Version 1
    ↓
old-key
```

Later you rotate the key:

```text
AZURE-OPENAI-API-KEY
Version 1 → old-key
Version 2 → new-key
```

Key Vault maintains versions.

Conceptually:

```text
Secret
│
├── Version 1
│     └── old value
│
└── Version 2
      └── new value
```

This is useful for **secret rotation**.

We'll go deeper into rotation later.

---

# 6. Now access it from Python

Install the Azure packages:

```bash
pip install azure-identity azure-keyvault-secrets
```

Then:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

vault_url = "https://sumanth-prod-kv.vault.azure.net/"

credential = DefaultAzureCredential()

client = SecretClient(
    vault_url=vault_url,
    credential=credential
)

secret = client.get_secret("AZURE-OPENAI-API-KEY")

print(secret.value)
```

That's the basic Key Vault retrieval code.

---

# 7. What is happening here?

Let's break down:

```python
credential = DefaultAzureCredential()
```

This doesn't contain your secret.

It says:

> "Find an appropriate Azure identity that I can use to authenticate."

Then:

```python
client = SecretClient(
    vault_url=vault_url,
    credential=credential
)
```

creates a Key Vault client.

Then:

```python
client.get_secret("AZURE-OPENAI-API-KEY")
```

requests the secret.

---

# 8. What happens behind the scenes?

Your code:

```python
client.get_secret("AZURE-OPENAI-API-KEY")
```

causes roughly:

```text
Python
  │
  ▼
DefaultAzureCredential
  │
  ▼
Obtain Access Token
  │
  ▼
Azure Key Vault
  │
  ▼
Authenticate caller
  │
  ▼
Check RBAC
  │
  ▼
Return secret
```

So the SDK handles a lot of the authentication details for you.

---

# 9. What happens on your laptop?

Suppose you're developing locally.

Your laptop doesn't have the App Service's Managed Identity.

You might authenticate to Azure using Azure CLI:

```bash
az login
```

Then:

```python
credential = DefaultAzureCredential()
```

can use an available developer credential from its supported credential chain.

So:

```text
LOCAL

Laptop
  │
  ▼
Developer authentication
  │
  ▼
Entra ID
  │
  ▼
Key Vault
```

---

# 10. What happens after deployment?

Suppose you deploy the exact same application to:

```text
Azure App Service
```

and enable:

```text
System-assigned Managed Identity
```

Now:

```text
PRODUCTION

App Service
    │
    ▼
Managed Identity
    │
    ▼
Entra ID
    │
    ▼
Key Vault
```

The Python code can remain:

```python
credential = DefaultAzureCredential()
```

This is one of the major advantages of using Azure Identity abstractions.

---

# 11. RBAC setup

Remember:

**Managed Identity alone isn't enough.**

You need:

```text
App Service
    │
    └── Managed Identity
             │
             ▼
     Key Vault Secrets User
             │
             ▼
        Key Vault
```

For example:

```text
Principal:
App Service Managed Identity

Role:
Key Vault Secrets User

Scope:
Specific Key Vault
```

Then your application can retrieve the secret.

---

# 12. What if you don't assign the role?

Suppose:

```text
Managed Identity ✅
```

but:

```text
Key Vault RBAC ❌
```

Then:

```text
Application
    │
    ▼
Managed Identity
    │
    ▼
Entra ID
    │
    ▼
Access Token ✅
    │
    ▼
Key Vault
    │
    ▼
RBAC
    │
    ▼
Access denied ❌
```

This is a very common deployment issue.

You can have perfectly valid authentication but still fail authorization.

---

# 13. Don't put the secret in environment variables unnecessarily

You might be used to:

```bash
export OPENAI_API_KEY="xxxxx"
```

or:

```text
OPENAI_API_KEY=xxxxx
```

Environment variables are useful for configuration, but they are **not a replacement for a proper secret-management system** when you're dealing with production credentials.

Instead:

```text
Application
    │
    ▼
Managed Identity
    │
    ▼
Key Vault
    │
    ▼
Secret
```

This gives you centralized secret management and access control.

---

# 14. Don't log the secret

Never do this in production:

```python
print(secret.value)
```

I only showed it above so you can understand the flow.

Instead:

```python
openai_api_key = secret.value
```

and use it without logging it.

Avoid:

```python
logger.info(f"API key = {openai_api_key}")
```

because logs can become another place where credentials leak.

---

# 15. A better application pattern

Instead of retrieving the secret everywhere:

```python
def function_a():
    client.get_secret(...)

def function_b():
    client.get_secret(...)

def function_c():
    client.get_secret(...)
```

centralize secret retrieval.

For example:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient


class KeyVaultService:

    def __init__(self, vault_url):
        credential = DefaultAzureCredential()

        self.client = SecretClient(
            vault_url=vault_url,
            credential=credential
        )

    def get_secret(self, name):
        return self.client.get_secret(name).value
```

Then:

```python
vault = KeyVaultService(
    "https://sumanth-prod-kv.vault.azure.net/"
)

api_key = vault.get_secret("AZURE-OPENAI-API-KEY")
```

This keeps your application code cleaner.

---

# 16. One important production consideration: caching

Suppose your application receives:

```text
1000 requests/minute
```

and every request does:

```text
Key Vault → get secret
```

That's unnecessary.

Instead, you can retrieve the secret during application startup or cache it appropriately.

Conceptually:

```text
Application startup
      │
      ▼
Key Vault
      │
      ▼
Retrieve secret
      │
      ▼
Application memory
      │
      ├── Request 1
      ├── Request 2
      ├── Request 3
      └── ...
```

But caching secrets introduces its own considerations, especially around rotation. We'll cover that later.

---

# 17. Your GenAI example

Suppose your application uses Azure OpenAI:

```text
Python GenAI Application
        │
        ▼
Azure Key Vault
        │
        └── AZURE-OPENAI-API-KEY
```

Your application retrieves:

```python
api_key = client.get_secret(
    "AZURE-OPENAI-API-KEY"
).value
```

Then uses the credential to initialize the Azure OpenAI client.

The important security architecture is:

```text
❌ Python source code
      ↓
    API key

❌ Git repository
      ↓
    API key

❌ Dockerfile
      ↓
    API key


✅ Azure Key Vault
      ↑
      │
Managed Identity
      ↑
      │
Python Application
```

---

# 18. The production architecture you should be able to explain

```text
                    Azure
                      │
          ┌───────────┴───────────┐
          │                       │
          ▼                       ▼
    App Service               Key Vault
          │                       │
          │                       ├── OpenAI Key
          │                       ├── DB Password
          │                       └── Third Party Key
          │
          ▼
   Managed Identity
          │
          ▼
    Microsoft Entra ID
          │
          ▼
     Access Token
          │
          ▼
       Key Vault
          │
          ▼
         RBAC
          │
          ▼
     Secret Value
```

---

## What you learned in this topic

You now know how to:

* Create a Key Vault
* Create a secret
* Understand secret names and values
* Understand secret versions
* Connect Python to Key Vault
* Use `DefaultAzureCredential`
* Use `SecretClient`
* Understand local vs Azure authentication
* Use Managed Identity in production
* Give the application Key Vault Secrets User
* Avoid logging secrets
* Think about caching

---

## Next: Phase 3 — Topic 2: `DefaultAzureCredential` in Depth

This is worth learning separately because you'll see it everywhere in Azure Python applications.

We'll answer:

> **"When I write `DefaultAzureCredential()`, how does it actually decide whether to use Azure CLI, environment credentials, Managed Identity, etc.?"**

And we'll connect it to your **local development → Azure deployment** workflow.
