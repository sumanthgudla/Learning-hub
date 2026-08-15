# Phase 1 — Topic 3: Secrets vs Keys vs Certificates

The name **Azure Key Vault** can be confusing because it manages **three different types of security objects**:

```text
Azure Key Vault
│
├── Secrets
├── Keys
└── Certificates
```

They serve different purposes.

---

# 1. Secrets

A **secret is sensitive data that your application needs to retrieve**.

Examples:

```text
API keys
Passwords
Connection strings
Tokens
Client secrets
```

For example:

```text
Name: AZURE-OPENAI-API-KEY
Value: xxxxxxxxxxxxxxxxxxxxx
```

Your application can retrieve the secret:

```python
secret = client.get_secret("AZURE-OPENAI-API-KEY")

api_key = secret.value
```

### GenAI example

Suppose your application connects to:

```text
Azure OpenAI
PostgreSQL
Redis
Third-party API
```

You might have:

```text
Key Vault
│
├── AZURE-OPENAI-API-KEY
├── POSTGRES-PASSWORD
├── REDIS-PASSWORD
└── THIRD-PARTY-API-KEY
```

These are **secrets**.

### Think:

> **Secret = something my application needs to know.**

---

# 2. Keys

Keys are different.

A cryptographic **key is used to perform cryptographic operations**.

For example:

```text
Encryption
Decryption
Signing
Verification
```

Imagine you have:

```text
Message
   │
   │ encryption key
   ▼
Encrypted data
```

And later:

```text
Encrypted data
   │
   │ decryption key
   ▼
Original message
```

Azure Key Vault can manage cryptographic keys for these kinds of operations.

### Example

Suppose your application stores sensitive customer data.

You could use an encryption key:

```text
Customer data
      │
      ▼
Encryption
      │
      │ Key
      ▼
Encrypted data
```

The key itself is managed by Key Vault.

### Think:

> **Key = something used to perform cryptographic operations.**

---

# 3. Certificates

Certificates are primarily used to establish **identity and trust**.

A common example is HTTPS.

When you visit:

```text
https://example.com
```

the server uses a TLS certificate to prove its identity and establish a secure connection.

Conceptually:

```text
Client
   │
   │ HTTPS
   ▼
Server
   │
   └── TLS Certificate
```

Certificates contain information such as:

```text
Domain
Issuer
Validity period
Public key
```

Azure Key Vault can help manage certificates and their lifecycle.

### Think:

> **Certificate = something used to establish identity/trust, often for TLS.**

---

# 4. The easiest way to remember

Use this table:

| Object          | Purpose                  | Example           |
| --------------- | ------------------------ | ----------------- |
| **Secret**      | Store sensitive values   | API key, password |
| **Key**         | Cryptographic operations | Encryption key    |
| **Certificate** | Identity/trust           | TLS certificate   |

Or remember:

```text
Secret      → Something you KNOW
Key         → Something you USE for cryptography
Certificate → Something that proves IDENTITY
```

---

# 5. Real GenAI application example

Suppose you build:

```text
Customer Support AI
```

Architecture:

```text
User
  │
  ▼
FastAPI
  │
  ├──────────────► Azure OpenAI
  │
  ├──────────────► PostgreSQL
  │
  └──────────────► Vector DB
```

You might need:

### Secrets

```text
AZURE_OPENAI_API_KEY
POSTGRES_PASSWORD
VECTOR_DB_PASSWORD
```

### Keys

Maybe you need:

```text
DATABASE_ENCRYPTION_KEY
```

for cryptographic operations.

### Certificate

Your application may use:

```text
TLS certificate
```

for secure communication.

So one Key Vault can manage all three categories.

---

# 6. Very important interview distinction

Suppose the interviewer asks:

> "Where would you store an Azure OpenAI API key in Key Vault?"

Answer:

**Secret.**

Not:

```text
Key ❌
Certificate ❌
Secret ✅
```

Because an API key is simply a sensitive value that the application needs to retrieve.

---

# 7. Don't confuse Azure OpenAI API key with Key Vault Key

This is a common source of confusion.

### Azure OpenAI API key

```text
"abc123..."
```

This is a **secret**.

You store it as:

```text
Key Vault Secret
```

### Cryptographic key

For example:

```text
RSA key
```

used for encryption/signing.

This is a:

```text
Key Vault Key
```

So:

```text
Azure OpenAI API Key
        ↓
Key Vault Secret


RSA/AES cryptographic key
        ↓
Key Vault Key
```

---

# 8. One more important concept

When we use Key Vault in production, we don't necessarily want our application to **retrieve every sensitive thing and handle it itself**.

For cryptographic operations, Azure Key Vault can perform certain operations using managed keys, allowing applications to avoid directly handling key material in some scenarios.

That's one of the reasons **Keys** are fundamentally different from **Secrets**.

We'll come back to this when we discuss production architecture.

---

## Quick test

Before moving to the next topic, try these mentally:

**1. Azure OpenAI API key?**

→ **Secret**

**2. PostgreSQL password?**

→ **Secret**

**3. RSA key used for signing?**

→ **Key**

**4. HTTPS/TLS certificate?**

→ **Certificate**

**5. Third-party API token?**

→ **Secret**

If these are clear, you've understood the important distinction.

---

### Next: Phase 1 — Topic 4

**Azure Key Vault architecture — Vault, secrets, identities, authentication, authorization, and how a request actually flows from your Python application to the secret.**

This is where we'll start connecting the pieces together.
