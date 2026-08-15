# Phase 2 — Topic 5: Service Principal

Now we come to **Service Principals**.

This is important because when people discuss Azure authentication, you'll often hear:

> **Managed Identity vs Service Principal**

The concepts are related, but they're not the same thing.

---

# 1. First: What is an application identity?

Suppose your Python application needs to access Azure Key Vault.

It's not a human.

```text id="ihv7d0"
Human
  ❌

Python Application
  ✅
```

Azure needs a way to identify that application.

One mechanism is a **Service Principal**.

A Service Principal is essentially an **identity for an application/service in Microsoft Entra ID** that can be assigned permissions to Azure resources.

---

# 2. Simple example

Imagine your application is:

```text id="p1xj6r"
MyGenAIApp
```

You register it in Microsoft Entra ID.

Conceptually:

```text id="s6u7jw"
MyGenAIApp
     │
     ▼
Microsoft Entra ID
     │
     ▼
Application Identity
```

A Service Principal represents that application's identity within a tenant and is what Azure can authorize for resource access.

---

# 3. How does the application authenticate?

A common Service Principal setup uses:

```text id="1j8jgu"
Tenant ID
Client ID
Client Secret
```

Think of them as:

```text id="74l9q0"
Tenant ID
    ↓
Which Entra ID tenant?

Client ID
    ↓
Which application?

Client Secret
    ↓
Can this application prove its identity?
```

The **client secret is sensitive**.

It should never be hardcoded.

---

# 4. Example

Suppose you have:

```text id="m1y2r3"
TENANT_ID=...
CLIENT_ID=...
CLIENT_SECRET=...
```

Your Python application could use a credential such as:

```python id="a7y5f1"
from azure.identity import ClientSecretCredential

credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret
)
```

Then:

```python id="q4x8v0"
client = SecretClient(
    vault_url=vault_url,
    credential=credential
)
```

The application can authenticate to Azure using the Service Principal.

---

# 5. The problem with this approach

Look at what your application now needs:

```text id="8r0y1b"
Python Application
      │
      ├── Tenant ID
      ├── Client ID
      └── Client Secret ❌
```

The client secret is another credential you need to protect.

You could store it in Key Vault—but now you have a chicken-and-egg problem:

> How does the application authenticate to Key Vault to retrieve the credential it needs to authenticate to Key Vault?

You need another mechanism for bootstrapping that credential.

This is one reason **Managed Identity** is so attractive for Azure-hosted workloads.

---

# 6. Managed Identity vs Service Principal

This is the important comparison.

### Service Principal

```text id="v7h3cp"
Application
     │
     ├── Client ID
     ├── Tenant ID
     └── Client Secret
             │
             ▼
       Microsoft Entra ID
```

You are responsible for managing the credential.

### Managed Identity

```text id="d6o2m7"
Azure Resource
     │
     ▼
Managed Identity
     │
     ▼
Microsoft Entra ID
```

Azure manages the identity's credentials.

So:

```text id="xk6t2v"
Service Principal
→ Application identity
→ Usually requires credential management


Managed Identity
→ Azure-managed application identity
→ No application-managed client secret
```

---

# 7. Why would we still use Service Principals?

You might ask:

> "If Managed Identity is better, why do Service Principals exist?"

Because not every application runs as an Azure resource.

Imagine:

```text id="xg8w2m"
GitHub Actions
      │
      ▼
Azure
```

or:

```text id="kq5r7n"
On-premises application
      │
      ▼
Azure
```

or:

```text id="qj7r2p"
External CI/CD system
      │
      ▼
Azure
```

These workloads may not have an Azure resource with a Managed Identity available in the same way.

Service principals can be useful for such scenarios.

---

# 8. Example: CI/CD

Suppose you have:

```text id="t7z2gc"
GitHub Actions
      │
      │ deploy
      ▼
Azure
```

The CI/CD pipeline needs to authenticate to Azure.

A traditional approach could use a Service Principal.

A more modern approach is often **federated identity / workload identity federation**, which avoids storing a long-lived client secret.

This is an important production topic, but we'll keep it separate for now.

---

# 9. Service Principal vs Managed Identity

|                                    | Service Principal | Managed Identity                              |
| ---------------------------------- | ----------------- | --------------------------------------------- |
| Application identity               | ✅                 | ✅                                             |
| Managed by Entra ID                | ✅                 | ✅                                             |
| Client secret commonly used        | ✅                 | ❌                                             |
| Azure manages credential lifecycle | ❌                 | ✅                                             |
| Good for Azure-hosted apps         | ⚠️                | ✅                                             |
| Useful outside Azure               | ✅                 | Limited                                       |
| Credential rotation required       | If using secrets  | Much less application-managed credential work |

---

# 10. Important terminology

You'll encounter these terms together:

```text id="2x4kcv"
App Registration
      ↓
Application
      ↓
Service Principal
```

This can initially be confusing.

### App Registration

Represents the application definition in Entra ID.

It contains things such as:

```text id="y6k5jz"
Application / Client ID
Tenant information
Authentication configuration
```

### Service Principal

Represents the application's identity in a particular Entra tenant and is the security principal that can be granted permissions.

For interview purposes, remember:

> **App registration defines the application; the service principal is the tenant-specific identity used for access.**

---

# 11. Real example

Suppose you build a Python application outside Azure:

```text id="5s2b3a"
Company Data Center
       │
       ▼
Python Application
       │
       ▼
Microsoft Entra ID
       │
       ▼
Service Principal
       │
       ▼
Azure Key Vault
```

The application might authenticate using:

```text id="7m2y2w"
Tenant ID
Client ID
Client Secret
```

Then Key Vault checks whether that identity has permission.

---

# 12. What should you choose?

### Application running on Azure

For example:

```text id="2v5w3g"
App Service
Azure Function
VM
AKS workload
```

Prefer:

```text id="b6y9rx"
Managed Identity
```

when appropriate.

### Application outside Azure

For example:

```text id="7k8m4d"
On-prem server
External CI/CD
External application
```

A Service Principal or workload identity federation may be appropriate depending on the platform.

---

# 13. Interview question

### Interviewer:

> "What is the difference between a Service Principal and Managed Identity?"

A strong answer:

> "Both provide application identities through Microsoft Entra ID. A Service Principal is an application identity that can authenticate using credentials such as a client secret or certificate. Managed Identity is an Azure-managed identity associated with an Azure resource, which avoids the application having to manage a client secret for Azure authentication. For an application running on Azure, I would generally prefer Managed Identity when supported."

---

# 14. Very important security point

If you use a Service Principal with a client secret:

**Never do this:**

```python id="t0j6t5"
client_secret = "my-super-secret"
```

And don't put it in:

```text id="v4g9km"
Git
Docker image
Source code
README
Logs
```

Instead, use a secure mechanism such as:

```text id="l6x7qf"
Secret Manager
Key Vault
CI/CD secret store
```

Or, preferably where supported, use **federated identity** to avoid long-lived secrets.

---

# 15. Your mental model

Keep this picture:

```text id="yq7v3p"
                  Microsoft Entra ID
                         │
             ┌───────────┴───────────┐
             │                       │
             ▼                       ▼
      Service Principal       Managed Identity
             │                       │
             │                       │
      Application identity    Azure resource identity
             │                       │
      Often credentials        Azure-managed
             │                       │
             └───────────┬───────────┘
                         ▼
                  Azure Resource
                         │
                         ▼
                    Key Vault
```

The biggest thing to remember:

> **Managed Identity is essentially the Azure-managed way for an Azure resource to have an identity, while a Service Principal is an application identity that you can use more broadly and may require you to manage credentials.**

---

## Next: Phase 2 — Topic 6: Client ID, Tenant ID, Client Secret & Access Tokens

This is where we'll decode the confusing values you see in Azure tutorials:

```text
Tenant ID
Client ID
Client Secret
Object ID
Access Token
```

We'll understand **exactly what each one means and how they relate to Service Principals and Managed Identity.**
