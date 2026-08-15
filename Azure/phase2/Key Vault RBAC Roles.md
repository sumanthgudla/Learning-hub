# Phase 2 — Topic 8: Key Vault RBAC Roles

Now let's focus specifically on **which Key Vault role you should give an application**.

The most important idea is:

> **Don't give an application more permission than it needs.**

---

# 1. First understand what you're protecting

Azure Key Vault can contain different types of objects:

```text
Key Vault
│
├── Secrets
├── Keys
└── Certificates
```

For your GenAI application, you might have:

```text
Key Vault
│
├── AZURE-OPENAI-API-KEY
├── DATABASE-PASSWORD
└── THIRD-PARTY-API-KEY
```

Your Python application might only need to **read secret values**.

Therefore, you don't want to give it administrator permissions.

---

# 2. Key Vault Secrets User

This is one of the most important roles for applications.

Conceptually:

```text
Key Vault Secrets User
        ↓
Can read secret values
```

For example:

```text
Python RAG Application
        │
        ▼
Managed Identity
        │
        ▼
Key Vault Secrets User
        │
        ▼
Azure Key Vault
        │
        ▼
OPENAI-API-KEY
```

If your application only needs to retrieve existing secrets, this is typically the kind of role you want.

---

# 3. Key Vault Secrets Officer

Now imagine your application needs to **manage secrets**, not merely read them.

For example:

```text
Create secret
Update secret
Delete secret
```

A broader role such as:

```text
Key Vault Secrets Officer
```

may be appropriate.

Conceptually:

```text id="e2w2c1"
Secrets Officer
    │
    ├── Read
    ├── Create/update
    └── Delete/manage secrets
```

You generally shouldn't give this role to a normal application if it only needs to retrieve secrets.

---

# 4. Key Vault Administrator

This is a very powerful role.

Conceptually:

```text id="c1qj0a"
Key Vault Administrator
       │
       ├── Manage secrets
       ├── Manage keys
       ├── Manage certificates
       └── Broad Key Vault data-plane permissions
```

This is typically an administrative role, **not an application runtime role**.

For example:

```text id="z5t9y8"
Developer/Admin
       ↓
Key Vault Administrator
```

would make more sense than:

```text id="4g8v3b"
Production Python App
       ↓
Key Vault Administrator ❌
```

---

# 5. Key Vault Reader

This one is particularly important to understand.

A role such as:

```text id="s0x8q2"
Key Vault Reader
```

is about reading **Key Vault resource information/metadata**, rather than giving your application the ability to retrieve secret values.

So don't think:

```text
Reader
  =
Can read secret values
```

That's not necessarily true.

For application secret retrieval, you need an appropriate **secret data-plane role**.

---

# 6. Simple comparison

| Role                          | Typical purpose                              |
| ----------------------------- | -------------------------------------------- |
| **Key Vault Reader**          | Read Key Vault resource/metadata information |
| **Key Vault Secrets User**    | Read secret values                           |
| **Key Vault Secrets Officer** | Manage secrets                               |
| **Key Vault Administrator**   | Broad Key Vault data-plane administration    |

The exact permissions of built-in roles are defined by Azure, so in real projects you should verify the current role definition rather than relying only on a role name.

---

# 7. Your GenAI application example

Suppose you have:

```text id="3v9d5w"
Azure App Service
       │
       └── Python + LangGraph
```

And Key Vault:

```text id="3j1t7s"
my-prod-kv
│
├── AZURE-OPENAI-API-KEY
├── POSTGRES-PASSWORD
└── THIRD-PARTY-API-KEY
```

Your application only needs to retrieve these secrets.

You would generally use:

```text id="w6y7q1"
Managed Identity
       │
       ▼
Key Vault Secrets User
       │
       ▼
my-prod-kv
```

Not:

```text id="e3n5v7"
Managed Identity
       │
       ▼
Key Vault Administrator ❌
```

---

# 8. Why least privilege matters

Suppose your application is compromised.

### With Secrets User

The attacker potentially gets access to the secrets that identity is authorized to read.

### With Administrator

The attacker may have much broader capabilities over Key Vault data.

So:

```text id="7u3b0k"
More permissions
      ↓
Larger blast radius
```

Therefore:

```text id="q0s1df"
Minimum required permissions
      ↓
Smaller blast radius
```

That's the principle of **least privilege**.

---

# 9. Scope matters too

Suppose you have:

```text id="n5m8q2"
Subscription
│
├── Dev Resource Group
│     └── Dev Key Vault
│
└── Prod Resource Group
      └── Prod Key Vault
```

Your production app needs access to:

```text id="2c6p5d"
Prod Key Vault
```

You could assign the role at the Key Vault scope:

```text id="h8j2q5"
Prod App Identity
       │
       ▼
Key Vault Secrets User
       │
       ▼
Prod Key Vault
```

That's preferable to unnecessarily assigning it at:

```text id="j5r8x0"
Entire Subscription
```

because the Key Vault scope is narrower.

---

# 10. Role + Scope

Remember:

```text id="1x8k4v"
Role
  +
Scope
  =
What the identity can do and where
```

For example:

```text id="8j2s0p"
Principal:
Production App Managed Identity

Role:
Key Vault Secrets User

Scope:
Production Key Vault
```

This means:

> The production app identity has the permissions provided by the Secrets User role at that Key Vault scope.

---

# 11. What about a single secret?

You might think:

> "Can I give the application permission to only `OPENAI-API-KEY` and nothing else?"

Azure RBAC scope granularity for Key Vault data-plane permissions is an important design consideration. Key Vault RBAC is generally assigned at scopes such as the vault, resource group, subscription, etc., rather than simply treating every secret as an independent RBAC target in the same way as a resource.

So if you have:

```text id="q2v8e3"
Key Vault
│
├── OPENAI-KEY
├── DB-PASSWORD
└── STRIPE-KEY
```

and give an identity a secret-reading role at the vault scope, you should assume it can read the secrets that role permits within that vault.

If you need stronger isolation, consider separating sensitive secrets into different vaults and identities.

---

# 12. A good production design

Instead of:

```text id="0w8s1m"
One giant Key Vault
│
├── Dev secrets
├── QA secrets
├── Prod secrets
├── Finance secrets
└── Everything
```

you might have:

```text id="g7y4f3"
Dev Key Vault
     ↑
 Dev Identity


QA Key Vault
     ↑
 QA Identity


Production Key Vault
     ↑
 Prod Identity
```

This gives you better isolation.

---

# 13. Control plane vs Data plane again

This distinction becomes clearer now.

### Control plane

Things like:

```text id="n8h3y4"
Create Key Vault
Delete Key Vault
Change Key Vault configuration
```

### Data plane

Things like:

```text id="u5f9r1"
Read secret
Create secret
Delete secret
Read key
```

Your runtime application usually needs **data-plane access**, not administrative control over the Key Vault resource.

So:

```text id="8j5f2k"
Runtime App
    ↓
Secret read permission
```

rather than:

```text id="6c9m1v"
Runtime App
    ↓
Full Key Vault administration
```

---

# 14. Interview question

### Interviewer:

> "Your Python application needs to read an Azure OpenAI API key stored in Key Vault. What permissions would you give it?"

A strong answer:

> "I'd enable a Managed Identity on the application and assign it the minimum Key Vault RBAC role required to read secret values, such as Key Vault Secrets User, at the narrowest practical scope, typically the specific Key Vault. I would not give the application an administrative role because it only needs runtime read access."

That's a very good production answer.

---

# 15. One subtle but important point

You may hear:

> "Give the application Key Vault Reader."

Be careful.

**Reader does not mean "read secret values."**

Always ask:

> **Read what?**

Azure has a distinction between:

```text
Resource metadata
       vs
Secret data
```

That's why understanding **control plane vs data plane** is important.

---

# 16. Final mental model

You should now be able to reason about this entire chain:

```text
                    Python App
                        │
                        ▼
                Managed Identity
                        │
                        ▼
                Microsoft Entra ID
                        │
                 Authentication
                        │
                        ▼
                  Access Token
                        │
                        ▼
                  Azure Key Vault
                        │
                  Authorization
                        │
                        ▼
                 Azure RBAC
                        │
                        ▼
              Key Vault Secrets User
                        │
                        ▼
                  Secret Value
```

And the security principle:

```text
        Need
         │
         ▼
   Minimum Role
         │
         ▼
   Minimum Scope
         │
         ▼
   Least Privilege
```

---

## Phase 2 is almost complete ✅

We've covered:

1. Microsoft Entra ID
2. Authentication vs Authorization
3. Managed Identity
4. System vs User-assigned Identity
5. Service Principal
6. Tenant/Client/Object IDs + Access Tokens
7. Azure RBAC
8. Key Vault RBAC roles

### Next: Phase 2 — Topic 9: Complete Key Vault Authentication Flow

We'll trace **one actual request from your Python application to Key Vault**, including:

```text
DefaultAzureCredential
        ↓
Managed Identity
        ↓
Entra ID
        ↓
Access Token
        ↓
Key Vault
        ↓
RBAC
        ↓
Secret
```

This will connect everything we've learned so far into one flow.
