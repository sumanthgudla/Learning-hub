# Phase 1 — Topic 2: Why shouldn't we store API keys in code?

Let's understand this from a **real production application** perspective.

Suppose you have a GenAI application that calls Azure OpenAI.

## 1. Hardcoding the API key

You might initially write:

```python
client = AzureOpenAI(
    api_key="sk-123456789"
)
```

This is a **bad practice**.

### Why?

Because the secret becomes part of your source code.

```text
Python code
    │
    └── API key
          │
          ├── Git
          ├── GitHub/GitLab
          ├── Code backups
          └── Developer machines
```

If someone gets access to the repository, they may get the key.

---

# 2. What if you use Git?

Imagine:

```bash
git add .
git commit -m "Added Azure OpenAI integration"
git push
```

Now your secret has potentially been stored in Git history.

Even if you later do:

```python
api_key = "new-key"
```

the **old key may still exist in Git history**.

That's why simply deleting the secret from the latest version of the code isn't necessarily enough.

---

# 3. What about `.env`?

A common improvement is:

```text
.env
```

with:

```text
AZURE_OPENAI_API_KEY=secret123
```

and Python:

```python
import os

api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

This is **better than hardcoding**.

Usually you also put:

```text
.env
```

inside:

```text
.gitignore
```

so it isn't committed.

For example:

```text
project/
│
├── app.py
├── requirements.txt
├── .gitignore
└── .env
```

`.gitignore`:

```text
.env
```

### Is this secure enough?

For **local development**, `.env` is commonly useful.

But for a **production application**, you generally need a stronger secret-management solution.

Why?

Because now you have to manage:

```text
Where is .env stored?
Who can access it?
How is it deployed?
How do we rotate the secret?
Who has permission to read it?
How do we audit access?
```

That's where Key Vault becomes valuable.

---

# 4. Environment variables aren't a secret-management system

This distinction is important.

You might have:

```python
api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

This is perfectly reasonable application code.

But the question becomes:

> **Where does `AZURE_OPENAI_API_KEY` come from?**

In production, you don't want developers manually copying secrets around.

Instead:

```text
Azure Key Vault
       │
       │ secure access
       ▼
Production Application
       │
       ▼
Environment / application configuration
```

The exact mechanism depends on the Azure service you're deploying to.

---

# 5. Configuration files have the same problem

Imagine:

```json
{
    "azure_openai_key": "secret123",
    "database_password": "password123"
}
```

This is also dangerous.

You now have credentials sitting inside a configuration file.

If the file gets:

* committed to Git
* copied to another machine
* included in a Docker image
* exposed in a backup
* accidentally logged

your secrets can leak.

---

# 6. Docker makes this even more important

Suppose you build:

```dockerfile
FROM python:3.12

COPY . /app

WORKDIR /app

CMD ["python", "app.py"]
```

If your secret is inside the application/configuration files that get copied into the image, you could accidentally put the secret inside the Docker image.

That's a serious production problem.

Instead:

```text
Docker Image
     │
     │ contains application code
     │
     │ ❌ no secrets
     │
     ▼
Container
     │
     │ authenticates using identity
     ▼
Azure Key Vault
     │
     ▼
Secret
```

---

# 7. Secret rotation

This is one of the biggest reasons for using a secret-management system.

Imagine your API key is:

```text
KEY_V1
```

After some time, security policy requires you to change it.

Without centralized secret management, you might have to:

```text
Find all applications
       ↓
Change configuration
       ↓
Redeploy
       ↓
Restart services
       ↓
Verify everything
```

With Key Vault, you can centrally manage the secret and its versions.

Conceptually:

```text
Azure Key Vault

OPENAI_API_KEY
│
├── Version 1
│
└── Version 2  ← new secret
```

We'll study **secret versions and rotation** later.

---

# 8. Access control

Suppose your company has:

```text
Developer A
Developer B
Production App
Admin
```

You don't want everyone to have unrestricted access to every secret.

For example:

```text
Production App
      │
      └── Can read OPENAI_API_KEY ✅

Developer
      │
      └── No production secret access ❌
```

Azure Key Vault works with Azure identity and authorization mechanisms to control this.

We'll learn **Managed Identity + RBAC** in Phase 2.

---

# 9. Auditing

Another important production requirement is:

> "Who accessed this secret?"

A centralized service makes it possible to monitor and audit access.

For example:

```text
Key Vault
   │
   ├── Secret accessed
   ├── Identity
   ├── Timestamp
   └── Operation
```

This is much harder to manage when secrets are scattered across:

```text
.env
config.json
Docker files
developer laptops
CI/CD variables
```

---

# 10. Important distinction: `.env` isn't "bad"

Don't take away the wrong lesson.

### Local development

```text
.env
```

is often perfectly reasonable.

For example:

```text
Developer laptop
      │
      └── .env
            │
            └── AZURE_OPENAI_API_KEY
```

### Production

You generally want:

```text
Production Application
       │
       ▼
Managed Identity
       │
       ▼
Azure Key Vault
       │
       ▼
Secret
```

So the better rule is:

> **Don't commit secrets to source control. Use a proper secret-management solution such as Azure Key Vault for production secrets.**

---

# 11. Interview question

### Interviewer:

> "Why shouldn't you store API keys in environment variables?"

Be careful here.

Don't say:

> "Environment variables are insecure."

That's too simplistic.

A better answer:

> "Environment variables are commonly used to provide configuration to applications, and they can be appropriate in some environments. The bigger concern is how the secret is provisioned, managed, rotated, and accessed. In Azure production environments, I would prefer a centralized secret manager such as Key Vault and use Managed Identity with least-privilege RBAC rather than distributing long-lived secrets manually."

That's a much stronger **Senior AI Engineer** answer.

---

## The mental model

Remember these three levels:

```text
LEVEL 1
Hardcoded secret
    ↓
❌ Never do this


LEVEL 2
.env / environment variable
    ↓
✅ Useful for local development
⚠️ Requires secure provisioning in production


LEVEL 3
Azure Key Vault
    +
Managed Identity
    +
RBAC
    ↓
✅ Production approach
```

### Next topic: Secrets vs Keys vs Certificates

This is important because **Azure Key Vault doesn't just store "keys."** It has three different object types, and interviewers can ask you the difference.
