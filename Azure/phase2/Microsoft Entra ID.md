# Phase 2 — Topic 1: Microsoft Entra ID

Now we move into the **authentication and authorization** part of Azure Key Vault.

The first thing you need to understand is **Microsoft Entra ID**.

---

## 1. What is Microsoft Entra ID?

**Microsoft Entra ID is Microsoft's cloud identity and access management service.**

Its job is essentially to answer:

> **Who are you?**

and help Azure determine:

> **What are you allowed to access?**

It manages identities for:

```text
Users
Applications
Services
Managed Identities
Service Principals
```

You may also see older tutorials call it:

```text
Azure Active Directory
Azure AD
AAD
```

These refer to the predecessor name. The current name is **Microsoft Entra ID**.

---

# 2. Why do we need it for Key Vault?

Suppose you have:

```text
Python Application
       │
       ▼
Azure Key Vault
```

Key Vault cannot simply say:

> "Anyone who asks for `OPENAI-API-KEY` gets it."

It needs to know:

```text
Who is making this request?
```

For example:

```text
Application A
    ↓
Key Vault

Application B
    ↓
Key Vault
```

Key Vault needs to distinguish between them.

That's where Entra ID comes in.

---

# 3. User identity vs Application identity

This is an important distinction.

Imagine **you** log into Azure.

You are a user:

```text
Sumanth
   │
   ▼
Microsoft Entra ID
```

But your production Python application isn't a human.

It's an **application/service identity**:

```text
Python Application
       │
       ▼
Microsoft Entra ID
```

Both can have identities managed through Entra ID.

---

# 4. Example with a human

Suppose you open Azure Portal and log in.

```text
You
 │
 │ username/password/MFA
 ▼
Microsoft Entra ID
 │
 │ authenticates you
 ▼
Azure Portal
```

Azure now knows:

> "This is Sumanth."

It can then check your permissions.

For example:

```text
Can Sumanth:
    │
    ├── View Key Vault?        ✅
    ├── Read secrets?          ✅
    ├── Delete secrets?        ❌
    └── Delete Key Vault?      ❌
```

That's authorization.

---

# 5. Example with an application

Now imagine your Python application running in Azure.

There is no human typing a username and password.

Instead:

```text
Python Application
       │
       ▼
Managed Identity
       │
       ▼
Microsoft Entra ID
```

Entra ID can authenticate that application identity.

Then Key Vault can determine what that identity is allowed to do.

---

# 6. Authentication vs Authorization

This is so important that you should memorize it.

### Authentication

> **Who are you?**

Example:

```text
Application → "I am Application A."
```

### Authorization

> **What are you allowed to do?**

Example:

```text
Application A
    │
    ├── Read secrets?    ✅
    ├── Write secrets?   ❌
    └── Delete secrets?  ❌
```

So:

```text
Authentication
       ↓
Identity
       ↓
Authorization
       ↓
Permissions
```

---

# 7. Where does Entra ID fit?

The overall architecture is:

```text
┌────────────────────┐
│ Python Application │
└─────────┬──────────┘
          │
          │ "Who am I?"
          ▼
┌────────────────────┐
│ Microsoft Entra ID │
└─────────┬──────────┘
          │
          │ Identity / Token
          ▼
┌────────────────────┐
│   Azure Key Vault  │
└─────────┬──────────┘
          │
          │ "What can this identity do?"
          ▼
┌────────────────────┐
│    Azure RBAC      │
└────────────────────┘
```

---

# 8. What is an access token?

When your application authenticates with Entra ID, it can obtain an **access token**.

You can think of the token as a temporary credential that says, roughly:

> "Microsoft Entra ID has authenticated this identity, and this token can be presented when accessing the relevant Azure service."

Conceptually:

```text
Application
     │
     │ authenticate
     ▼
Entra ID
     │
     │ Access Token
     ▼
Application
     │
     │ request + token
     ▼
Key Vault
```

Key Vault can validate the token and determine the identity behind it.

---

# 9. Why not just use an API key?

This is an important production concept.

Suppose you authenticate to some service using:

```text
API_KEY=abc123
```

The application has to possess a long-lived secret.

That creates another secret-management problem.

Azure's identity model allows Azure resources to authenticate using identities such as **Managed Identity**, avoiding the need for your application to manually store a client secret for Azure-to-Azure authentication.

So instead of:

```text
Application
    │
    └── Client Secret
           │
           ▼
       Entra ID
```

you can use:

```text
Azure Application
       │
       ▼
Managed Identity
       │
       ▼
Microsoft Entra ID
```

This is one of the major benefits of Managed Identity.

---

# 10. Entra ID and Key Vault are different things

Don't confuse these two.

### Microsoft Entra ID

Responsible for:

```text
Identity
Authentication
Access tokens
Identity management
```

### Azure Key Vault

Responsible for:

```text
Secrets
Keys
Certificates
Secret/key management
```

### Azure RBAC

Responsible for:

```text
Permissions
Authorization
```

So:

```text
            Microsoft Entra ID
                    │
              "Who are you?"
                    │
                    ▼
              Identity Token
                    │
                    ▼
             Azure Key Vault
                    │
              "What can you do?"
                    │
                    ▼
                Azure RBAC
```

---

# 11. Real GenAI example

Your application:

```text
LangGraph RAG Application
          │
          ▼
     Azure OpenAI
```

The application needs an OpenAI credential stored in Key Vault.

Production flow:

```text
┌───────────────────┐
│ LangGraph / Python│
│ Application       │
└─────────┬─────────┘
          │
          │ Managed Identity
          ▼
┌──────────────────────┐
│ Microsoft Entra ID   │
└─────────┬────────────┘
          │
          │ Access Token
          ▼
┌──────────────────────┐
│ Azure Key Vault      │
│                      │
│ AZURE-OPENAI-KEY     │
└─────────┬────────────┘
          │
          │ Secret
          ▼
┌──────────────────────┐
│ Python Application   │
└─────────┬────────────┘
          │
          ▼
    Azure OpenAI
```

Notice that:

**Entra ID doesn't store your OpenAI API key.**

**Key Vault stores the secret.**

Entra ID provides the identity mechanism used to authenticate the application to Azure services.

---

# 12. Interview question

### "What is Microsoft Entra ID?"

A strong answer:

> **"Microsoft Entra ID is Microsoft's cloud identity and access management service. It manages identities for users, applications, and services and provides authentication and identity tokens that Azure resources can use for authorization. In a Key Vault scenario, an application can authenticate using a Managed Identity through Entra ID, and Azure RBAC determines what that identity is allowed to access."**

That's enough for an interview unless they ask for deeper details.

---

# 13. Your mental model

Remember these three:

```text
Microsoft Entra ID
        ↓
Identity / Authentication


Azure RBAC
        ↓
Authorization / Permissions


Azure Key Vault
        ↓
Secrets / Keys / Certificates
```

And the complete picture:

```text
Application
     │
     │ Managed Identity
     ▼
Entra ID
     │
     │ Authentication
     ▼
Access Token
     │
     ▼
Key Vault
     │
     │ Authorization
     ▼
RBAC
     │
     ▼
Secret
```

---

## Next: Phase 2 — Topic 2

**Authentication vs Authorization in depth**

We'll use a concrete example and distinguish:

* Authentication
* Authorization
* Access token
* Roles
* Permissions
* 401 vs 403

This will also connect directly to the REST API authentication concepts you've been learning.
