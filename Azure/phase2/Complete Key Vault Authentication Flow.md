# Phase 2 — Topic 9: Complete Key Vault Authentication Flow

Now let's put **everything we've learned together**.

We'll trace one real request:

> **Python application running on Azure App Service wants to read an OpenAI API key from Azure Key Vault.**

---

# 1. Our architecture

We have:

```text
Azure App Service
    │
    │ Python + LangGraph
    │
    ▼
Managed Identity
    │
    ▼
Microsoft Entra ID
    │
    ▼
Azure Key Vault
    │
    └── AZURE-OPENAI-API-KEY
```

And the identity has:

```text
Key Vault Secrets User
```

at the Key Vault scope.

---

# 2. Python code

Our application contains:

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

The interesting part is:

```python
credential = DefaultAzureCredential()
```

What actually happens here?

Let's go step by step.

---

# 3. Step 1 — Application starts

Your application is running:

```text
┌─────────────────────────┐
│ Azure App Service       │
│                         │
│ Python Application      │
└─────────────────────────┘
```

The App Service has a:

```text
Managed Identity
```

enabled.

So Azure knows:

> This App Service has an identity.

---

# 4. Step 2 — `DefaultAzureCredential`

Your code executes:

```python
credential = DefaultAzureCredential()
```

This creates a credential chain that Azure SDK libraries can use to obtain an access token.

You don't explicitly put:

```python
client_id = "..."
client_secret = "..."
```

in your production code.

---

# 5. Step 3 — Application requests a token

When you execute:

```python
client.get_secret("AZURE-OPENAI-API-KEY")
```

the Azure SDK needs a token to authenticate the request.

Conceptually:

```text
Python
   │
   │ "I need a token"
   ▼
DefaultAzureCredential
   │
   ▼
Managed Identity
```

---

# 6. Step 4 — Managed Identity contacts Azure identity infrastructure

The Azure environment provides a mechanism through which the application can obtain a token for its managed identity.

Conceptually:

```text
Python Application
       │
       ▼
Managed Identity
       │
       ▼
Microsoft Entra ID
```

The application isn't sending a client secret that you've stored in your source code.

Azure manages the underlying identity credentials.

---

# 7. Step 5 — Entra ID authenticates the identity

Microsoft Entra ID determines which identity is making the request.

Conceptually:

```text
Entra ID
   │
   │
   ▼
"This request represents
 the identity of App Service X."
```

If successful, Entra ID issues an:

```text
Access Token
```

---

# 8. Step 6 — Access token

The application now has a token.

Conceptually:

```text
Python Application
       │
       │ Access Token
       ▼
Azure Key Vault
```

You don't normally need to manually inspect or construct the token.

The Azure SDK handles this for you.

---

# 9. Step 7 — Request reaches Key Vault

Your application effectively makes a request equivalent to:

```text
Get secret:
AZURE-OPENAI-API-KEY
```

with the access token.

Conceptually:

```text
GET /secrets/AZURE-OPENAI-API-KEY

Authorization: Bearer <access-token>
```

The actual SDK handles the HTTP details.

---

# 10. Step 8 — Key Vault validates the identity

Key Vault receives the request.

It can determine:

```text
Who is calling me?
```

The token represents your application's identity.

So:

```text
Key Vault
   │
   ▼
"Who is this?"
   │
   ▼
Production App Managed Identity
```

Authentication has effectively established the caller's identity.

---

# 11. Step 9 — Key Vault checks authorization

Now comes the important part.

Key Vault asks:

> **"Is this identity allowed to read this secret?"**

Azure RBAC is involved.

We previously configured:

```text
Principal:
Production App Managed Identity

Role:
Key Vault Secrets User

Scope:
Production Key Vault
```

So the authorization check succeeds.

```text
Managed Identity
       │
       ▼
Key Vault Secrets User
       │
       ▼
Production Key Vault
       │
       ▼
Permission ✅
```

---

# 12. Step 10 — Key Vault returns the secret

Now Key Vault returns the secret value to the application.

```text
Key Vault
    │
    │ Secret value
    ▼
Python Application
```

Your code gets:

```python
secret.value
```

which might contain:

```text
xxxxxxxxxxxxxxxxxxxx
```

Your application can then use that credential when communicating with the relevant service.

---

# 13. Complete flow

This is the **most important diagram from Phase 2**:

```text
┌─────────────────────┐
│ Python Application  │
│ Azure App Service   │
└──────────┬──────────┘
           │
           │ 1. Request credential
           ▼
┌─────────────────────┐
│ DefaultAzure        │
│ Credential          │
└──────────┬──────────┘
           │
           │ 2. Use Managed Identity
           ▼
┌─────────────────────┐
│ Microsoft Entra ID  │
└──────────┬──────────┘
           │
           │ 3. Access Token
           ▼
┌─────────────────────┐
│ Python Application  │
└──────────┬──────────┘
           │
           │ 4. Request secret + token
           ▼
┌─────────────────────┐
│ Azure Key Vault     │
└──────────┬──────────┘
           │
           │ 5. Authorization check
           ▼
┌─────────────────────┐
│ Azure RBAC          │
│                     │
│ Secrets User        │
└──────────┬──────────┘
           │
           │ 6. Allowed
           ▼
┌─────────────────────┐
│ Secret Value        │
└─────────────────────┘
```

---

# 14. What if authentication fails?

Suppose the application doesn't have a usable identity/token.

Conceptually:

```text
Application
     │
     ▼
Key Vault
     │
     ▼
Authentication fails
```

The request cannot be successfully authenticated.

This is where **401-type authentication failures** can occur.

---

# 15. What if authorization fails?

Suppose the application has a Managed Identity:

```text
Authentication ✅
```

but you forgot to assign the required Key Vault RBAC role.

Then:

```text
Application
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
Permission ❌
```

The identity is known, but access is denied.

This corresponds to a **403-type authorization failure**.

---

# 16. This is why "Managed Identity enabled" isn't enough

A common beginner mistake is:

> "I enabled Managed Identity, so my application can now access Key Vault."

No.

You need **both**:

```text
Managed Identity
       +
RBAC permission
```

Think:

```text
Identity
   ↓
Who are you?

RBAC
   ↓
What are you allowed to do?
```

---

# 17. Where does the secret actually live?

This is another important point.

The OpenAI API key is stored here:

```text
Azure Key Vault
    │
    └── AZURE-OPENAI-API-KEY
```

It is **not** stored in:

```text
❌ Entra ID
❌ Managed Identity
❌ RBAC
❌ Access Token
```

Their responsibilities are different:

| Component        | Responsibility                  |
| ---------------- | ------------------------------- |
| Entra ID         | Identity/authentication         |
| Managed Identity | Azure resource identity         |
| Access Token     | Authenticated access credential |
| RBAC             | Authorization                   |
| Key Vault        | Stores the secret               |

---

# 18. Why this architecture is secure

Notice what your source code doesn't contain:

```python
client_secret = "..."
openai_key = "..."
database_password = "..."
```

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

This reduces the number of long-lived credentials you have to embed in your application.

---

# 19. What about local development?

This is where `DefaultAzureCredential` becomes especially useful.

Your laptop doesn't normally have the same Managed Identity as your production App Service.

For example:

```text
LOCAL DEVELOPMENT

Your Laptop
    │
    ▼
Developer Azure Login
    │
    ▼
Entra ID
    │
    ▼
Key Vault
```

Production:

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

Yet your Python code can remain:

```python
credential = DefaultAzureCredential()
```

The credential mechanism can select an appropriate available authentication method for the environment.

---

# 20. Why `DefaultAzureCredential` is useful

Without it, you might write separate authentication logic:

```text
Local
   ↓
Developer credentials

Production
   ↓
Managed Identity
```

With:

```python
DefaultAzureCredential()
```

your application can use the Azure Identity library's supported credential chain.

So you can keep the application code consistent across environments.

---

# 21. Interview question

### Interviewer:

> "Explain how an Azure App Service retrieves a secret from Key Vault using Managed Identity."

A strong answer:

> "I enable a Managed Identity on the App Service and assign it the minimum required Key Vault RBAC role, such as Key Vault Secrets User, at the appropriate scope. In the application I use the Azure Identity SDK, typically `DefaultAzureCredential`, together with the Key Vault SDK. The application obtains an access token through its Managed Identity and Microsoft Entra ID, sends the authenticated request to Key Vault, and Key Vault authorizes the request using RBAC before returning the secret."

That answer demonstrates that you understand the **whole flow**, not just individual Azure features.

---

# 22. The one diagram to memorize

If you remember only one thing from this entire phase, remember this:

```text
                 AUTHENTICATION
                       │
                       ▼
Application ───► Managed Identity
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
                  AUTHORIZATION
                       │
                       ▼
                     RBAC
                       │
                       ▼
                    Secret
```

---

# Phase 2 Complete ✅

You now understand the complete Azure Key Vault security model:

```text
Entra ID
     ↓
Identity

Managed Identity
     ↓
Azure resource identity

Access Token
     ↓
Authentication credential

RBAC
     ↓
Authorization

Key Vault
     ↓
Secret storage
```

### Phase 3 will be hands-on Key Vault usage

We'll move from **"how Azure security works"** to **"how I actually use Key Vault in an application."**

We'll cover:

1. Creating a Key Vault
2. Creating secrets
3. Reading secrets
4. Updating/versioning secrets
5. Python SDK
6. `DefaultAzureCredential`
7. Environment variables
8. Local development
9. Azure App Service deployment
10. Key Vault references
11. Secret rotation
12. Production architecture
13. Troubleshooting common errors
14. Complete Python + Azure OpenAI example
