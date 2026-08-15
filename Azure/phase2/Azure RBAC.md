# Phase 2 — Topic 7: Azure RBAC

Now we get to **authorization**.

You already know:

```text
Microsoft Entra ID
    ↓
Authentication
    ↓
"Who are you?"
```

Now Azure needs to answer:

> **"What is this identity allowed to do?"**

That's where **Azure RBAC** comes in.

---

# 1. What is RBAC?

**RBAC = Role-Based Access Control**

Instead of giving permissions individually to every identity, Azure provides **roles** containing permissions.

Conceptually:

```text
Identity
   ↓
Role
   ↓
Permissions
   ↓
Resource
```

For example:

```text
App Service Managed Identity
        ↓
Key Vault Secrets User
        ↓
Read secrets
        ↓
MyKeyVault
```

---

# 2. The three things you need to understand

Azure RBAC can be understood using:

```text
Role
Scope
Role Assignment
```

Let's look at each.

---

# 3. Role

A **role** is a collection of permissions.

For example, conceptually:

```text
Key Vault Secrets User
    │
    ├── Read secrets
    └── Access secret values
```

Another role might have much broader permissions.

So instead of saying:

```text
Application can do X
Application can do Y
Application cannot do Z
```

you assign an appropriate built-in role.

---

# 4. Scope

**Scope** answers:

> **Where does this permission apply?**

Azure resources have a hierarchy.

Conceptually:

```text
Management Group
      │
      ▼
Subscription
      │
      ▼
Resource Group
      │
      ▼
Key Vault
      │
      ▼
Secret
```

A role assignment can be made at an appropriate scope.

For example:

```text
Subscription
```

would potentially affect many resources.

Whereas:

```text
Specific Key Vault
```

is much narrower.

---

# 5. Why scope matters

Suppose your application only needs:

```text
Read secrets from:
my-production-vault
```

You shouldn't unnecessarily give it permissions at:

```text
Subscription
```

because that could affect many resources.

Prefer the smallest useful scope.

```text
❌ Subscription-wide access

        ↓

✅ Specific Key Vault
```

This is another example of **least privilege**.

---

# 6. Role assignment

A role by itself doesn't give your application access.

You need a **role assignment**.

Conceptually:

```text
Identity
   +
Role
   +
Scope
   ↓
Role Assignment
```

Example:

```text
Production RAG App Identity
        +
Key Vault Secrets User
        +
Production Key Vault
        ↓
Role Assignment
```

Now the identity has that permission at that scope.

---

# 7. Complete example

Suppose we have:

```text
Azure App Service
       │
       └── Managed Identity
```

and:

```text
Azure Key Vault
       │
       └── OPENAI-API-KEY
```

We want:

> App Service can read secrets from this Key Vault.

We create an authorization relationship:

```text
Managed Identity
      │
      │ assigned role
      ▼
Key Vault Secrets User
      │
      │ at scope
      ▼
Production Key Vault
```

Now the application can access secrets according to that role's permissions.

---

# 8. Full request flow

Let's put authentication and authorization together.

```text
Python Application
       │
       │ Managed Identity
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
       │ "What can this identity do?"
       ▼
Azure RBAC
       │
       │ Check role assignment
       ▼
Permission
       │
   ┌───┴────┐
   │        │
  YES       NO
   │        │
   ▼        ▼
Secret     403
```

This is the complete picture.

---

# 9. Key Vault example

Suppose your vault is:

```text
my-production-kv
```

Your App Service identity is:

```text
prod-rag-api
```

You want:

```text
prod-rag-api
      ↓
read secrets
      ↓
my-production-kv
```

You assign an appropriate Key Vault RBAC role to the application's managed identity at the Key Vault scope.

Conceptually:

```text
Principal:
    prod-rag-api Managed Identity

Role:
    Key Vault Secrets User

Scope:
    my-production-kv
```

This is a **role assignment**.

---

# 10. What is a principal?

You'll see this word frequently in Azure documentation.

A **security principal** is an identity that can be granted permissions.

Examples include:

```text
User
Group
Service Principal
Managed Identity
```

So in our example:

```text
Principal
    ↓
App Service Managed Identity
```

Then:

```text
Principal
   +
Role
   +
Scope
   ↓
Role Assignment
```

---

# 11. Important Key Vault roles

For Key Vault, you'll encounter roles such as:

```text
Key Vault Secrets User
Key Vault Secrets Officer
Key Vault Administrator
```

They don't all provide the same level of access.

The important lesson is:

> **Choose the smallest role that provides the permissions your application actually needs.**

For example, an application that only needs to retrieve secret values shouldn't automatically be made a Key Vault administrator.

---

# 12. Reader vs Secrets User

This is a common source of confusion.

Suppose you give an identity:

```text
Key Vault Reader
```

That doesn't necessarily mean:

> "The application can read the actual secret values."

Being able to **see metadata about a resource** is different from being allowed to **read secret values**.

For an application that needs secret values, you need an appropriate data-plane role, such as a suitable Key Vault secrets role.

---

# 13. Control plane vs data plane

This is an important Azure concept.

### Control plane

Managing the Azure resource itself.

For example:

```text
Create Key Vault
Delete Key Vault
Change configuration
Manage resource settings
```

### Data plane

Accessing the data stored inside it.

For example:

```text
Read secret
Write secret
Delete secret
Read key
```

So:

```text
Azure Resource Management
        ↓
Control Plane


Secret/Key access
        ↓
Data Plane
```

This distinction explains why simply having a general resource-management role doesn't necessarily mean your application can retrieve secret values.

---

# 14. Example of a common mistake

Suppose you give:

```text
App Identity
    ↓
Contributor
    ↓
Key Vault
```

You might think:

> "Contributor means the app can access everything in the vault."

That's not the right mental model.

Resource management permissions and data access permissions are distinct.

For application secret retrieval, assign the appropriate Key Vault data-plane role.

---

# 15. RBAC vs Key Vault access policies

You may see older Azure Key Vault tutorials talking about:

> **Access Policies**

Historically, Key Vault supported access policies for data-plane permissions.

Azure Key Vault can also use **Azure RBAC** for access control.

For modern Azure designs, you'll frequently encounter:

```text
Azure RBAC
```

and Microsoft generally recommends RBAC for Key Vault authorization because it provides a consistent Azure authorization model.

For your learning, focus on:

```text
Managed Identity
      ↓
Azure RBAC
      ↓
Key Vault
```

---

# 16. The complete production architecture

Now you should be able to understand this:

```text
                    Azure
                      │
        ┌─────────────┴─────────────┐
        │                           │
        ▼                           ▼
   App Service                Microsoft Entra ID
        │                           │
        │ Managed Identity          │
        └──────────────┬────────────┘
                       │
                       │ Access Token
                       ▼
                Azure Key Vault
                       │
                       ▼
                  Azure RBAC
                       │
                       │ Role Assignment
                       ▼
             Key Vault Secrets User
                       │
                       ▼
                  Secret Value
```

---

# 17. Interview question

### Interviewer:

> "How would you give an Azure App Service access to a secret in Key Vault?"

A strong answer:

> "I would enable a Managed Identity on the App Service, then assign that identity an appropriate Key Vault RBAC role at the narrowest practical scope, such as the specific Key Vault. The application would authenticate using the Managed Identity through Microsoft Entra ID and obtain an access token. Key Vault would then authorize the request based on the RBAC role assignment."

That's a **production-level answer**.

---

# 18. The four words to remember

When discussing RBAC, always think:

```text
Principal
   ↓
Role
   ↓
Scope
   ↓
Role Assignment
```

For our example:

```text
Principal:
App Service Managed Identity

Role:
Key Vault Secrets User

Scope:
Specific Key Vault

Assignment:
Principal + Role + Scope
```

---

# Phase 2 progress

You now understand:

```text
✅ Microsoft Entra ID
✅ Authentication vs Authorization
✅ Managed Identity
✅ System-assigned vs User-assigned
✅ Service Principal
✅ Tenant ID
✅ Client ID
✅ Client Secret
✅ Object ID
✅ Access Token
✅ Azure RBAC
✅ Role
✅ Scope
✅ Principal
✅ Role Assignment
✅ Control plane vs Data plane
```

## Next: Phase 2 — Topic 8: Key Vault RBAC Roles

We'll go specifically into:

```text
Key Vault Reader
Key Vault Secrets User
Key Vault Secrets Officer
Key Vault Administrator
```

and answer the practical question:

> **"My application only needs to read an OpenAI API key. Which role should I give it, and why?"**
