# Phase 1 — Topic 5: Key Vault vs `.env` vs Environment Variables

This is a very important topic because in real projects you'll encounter all three.

The key idea is:

> **`.env`, environment variables, and Azure Key Vault are not exactly alternatives. They solve different parts of the configuration/secrets problem.**

---

## 1. `.env` file

A `.env` file is simply a local file containing configuration values.

Example:

```text
AZURE_OPENAI_API_KEY=abc123
DATABASE_PASSWORD=xyz789
```

Your Python application can read it:

```python
import os

api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

Usually, you use a library such as `python-dotenv` during local development to load the `.env` file.

### Typical use

```text
Your laptop
   │
   ├── Python application
   │
   └── .env
        ├── API key
        └── DB password
```

### Advantage

Very convenient for development.

### Problem

The secret physically exists on your machine as a file.

You must make sure it isn't committed to Git:

```text
.env
```

should normally be in:

```text
.gitignore
```

---

# 2. Environment variables

An environment variable is a value provided to the running process by the operating environment.

For example:

```bash
export AZURE_OPENAI_API_KEY="abc123"
```

Then:

```python
import os

api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

Your application doesn't need to know where the value came from.

It just asks the operating system:

> "Give me `AZURE_OPENAI_API_KEY`."

---

# 3. `.env` vs environment variable

This distinction is important.

A `.env` file:

```text
.env
   ↓
AZURE_OPENAI_API_KEY=abc123
```

is just a **file**.

An environment variable:

```text
Process environment
   ↓
AZURE_OPENAI_API_KEY=abc123
```

is part of the environment available to the running application.

A `.env` library can load values from the file into environment variables.

So:

```text
.env file
   │
   │ load
   ▼
Environment variables
   │
   ▼
Python application
```

---

# 4. Azure Key Vault

Key Vault is a **centralized cloud service for managing secrets, keys, and certificates**.

Instead of:

```text
Developer laptop
      │
      └── .env
```

you can have:

```text
Azure Key Vault
      │
      ├── OPENAI-API-KEY
      ├── DB-PASSWORD
      └── API-SECRET
```

Your application retrieves the required secret securely.

---

# 5. The important production difference

Let's compare them.

| Feature                      | `.env`      | Environment Variable | Key Vault |
| ---------------------------- | ----------- | -------------------- | --------- |
| Local development            | ✅ Excellent | ✅ Good               | ✅         |
| Centralized management       | ❌           | ❌                    | ✅         |
| Access control               | ❌           | Limited              | ✅         |
| Secret rotation              | Manual      | Manual               | ✅         |
| Auditing                     | ❌           | Limited              | ✅         |
| Secret versioning            | ❌           | ❌                    | ✅         |
| Azure integration            | ❌           | ⚠️                   | ✅         |
| Production secret management | ⚠️          | ⚠️                   | ✅         |

The important point is:

**Environment variables are a way to provide configuration to an application. Key Vault is a secret-management service.**

---

# 6. Local development

Suppose you're developing your RAG application on your Mac.

You could have:

```text
project/
│
├── app.py
├── requirements.txt
├── .gitignore
└── .env
```

`.env`:

```text
AZURE_OPENAI_API_KEY=xxxxxxxx
```

Python:

```python
import os

api_key = os.getenv("AZURE_OPENAI_API_KEY")
```

That's a perfectly reasonable development setup.

You don't necessarily need to introduce Key Vault immediately for every local experiment.

---

# 7. Production

Now suppose you've deployed your application to Azure.

Instead of:

```text
Production server
      │
      └── .env
           └── production secret
```

you can use:

```text
Production application
       │
       │ Managed Identity
       ▼
Microsoft Entra ID
       │
       ▼
Azure Key Vault
       │
       ▼
Secret
```

This gives you centralized management and access control.

---

# 8. What happens to the secret after retrieval?

This is an important subtle point.

Suppose your Python application does:

```python
secret = client.get_secret("OPENAI-API-KEY")
```

Key Vault has returned the secret to your application.

At that point, **your application has the secret in memory**.

Key Vault doesn't magically make the secret disappear from your application's memory.

So you still need to follow good practices:

```text
Don't:
- print secrets
- log secrets
- expose secrets in API responses
- commit secrets
- put secrets into error messages
```

For example, avoid:

```python
print(secret.value)  # ❌
```

---

# 9. What should you use?

For your learning and interview preparation, use this simple rule:

### Local development

```text
.env
```

is convenient.

### Production

```text
Azure Key Vault
+
Managed Identity
+
RBAC
```

is the preferred Azure architecture for many workloads.

---

# 10. A real project

Imagine your **LangGraph RAG application**.

### Development

```text
                 Developer Laptop
                       │
                ┌──────▼──────┐
                │ Python App  │
                └──────┬──────┘
                       │
                       ▼
                     .env
                       │
              AZURE_OPENAI_KEY
```

### Production

```text
                    Azure
                      │
              ┌───────▼────────┐
              │ Python / GenAI │
              │   Application  │
              └───────┬────────┘
                      │
               Managed Identity
                      │
                      ▼
              Microsoft Entra ID
                      │
                      ▼
              ┌────────────────┐
              │  Key Vault     │
              │                │
              │ OPENAI-KEY     │
              │ DB-PASSWORD    │
              └────────────────┘
```

This is a very common pattern.

---

# 11. Interview question

### Interviewer:

> "Would you use `.env` in production?"

Don't answer simply:

> "No."

A better answer is:

> "I commonly use `.env` for local development because it's convenient for providing configuration. For production, I prefer a centralized secret-management solution such as Azure Key Vault. In Azure, the application can use Managed Identity to authenticate to Key Vault and RBAC to enforce least-privilege access."

That's a much better production-oriented answer.

---

# One important correction to remember

Don't think:

```text
.env = insecure
Key Vault = secure
```

It's more nuanced.

Think:

```text
.env
→ local configuration mechanism

Environment variable
→ runtime configuration mechanism

Key Vault
→ centralized secret-management mechanism
```

And in a production Azure architecture:

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
Key Vault
     │
     ▼
Secret
```

---

## Phase 1 almost complete

You've now covered:

1. ✅ What is Azure Key Vault?
2. ✅ Why shouldn't secrets be hardcoded?
3. ✅ Secrets vs Keys vs Certificates
4. ✅ Key Vault architecture
5. ✅ Key Vault vs `.env` vs Environment Variables

### Next: Phase 1 — Topic 6: A complete real-world example

We'll take a **Python + Azure OpenAI application** and walk through the entire flow from:

**developer → Key Vault → identity → permissions → Python application → Azure OpenAI**

Then Phase 1 will be complete, and we'll move into the **most important part: Managed Identity, Entra ID, Service Principals, and RBAC.**
