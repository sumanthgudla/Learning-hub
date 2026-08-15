# Phase 3 — Topic 3: Secret Versioning, Rotation & Zero-Downtime Updates

Now we're getting into **production-level Key Vault usage**.

A common interview question is:

> **"What happens if the API key stored in Key Vault needs to be rotated?"**

Let's understand that properly.

---

# 1. What is secret rotation?

Suppose your application uses:

```text
OPENAI_API_KEY = old-key
```

For security or operational reasons, you need to replace it.

Instead of changing your application code:

```text
❌ Change Python code
❌ Commit new key
❌ Rebuild application
❌ Redeploy
```

you can update the secret in Key Vault.

That's called **secret rotation**.

---

# 2. Key Vault supports secret versions

Suppose you have:

```text
OPENAI_API_KEY
```

Initially:

```text
Version 1
    ↓
old-key
```

Then you update the secret:

```text
OPENAI_API_KEY
│
├── Version 1 → old-key
└── Version 2 → new-key
```

The old version isn't necessarily destroyed immediately.

You now have a history of secret versions.

---

# 3. Why versions are useful

Imagine you accidentally change the secret.

You can have:

```text
Version 1
Version 2
Version 3
```

This gives you a history of values/versions and allows applications or operators to work with a specific version when appropriate.

Conceptually:

```text
Secret
 │
 ├── v1
 ├── v2
 └── v3 ← current/latest
```

---

# 4. What happens when you call `get_secret()`?

You normally do:

```python
secret = client.get_secret("OPENAI_API_KEY")
```

without specifying a version.

Conceptually:

```text
get_secret("OPENAI_API_KEY")
            ↓
Retrieve current/latest version
```

You can also request a particular version when your application explicitly needs one.

Conceptually:

```python
client.get_secret(
    "OPENAI_API_KEY",
    version="specific-version-id"
)
```

This is useful for controlled migrations or troubleshooting.

---

# 5. Important: Secret rotation does NOT automatically rotate the external credential

This is subtle.

Suppose Key Vault contains:

```text
OPENAI_API_KEY
    ↓
abc123
```

You change the Key Vault value to:

```text
xyz789
```

Key Vault has changed.

But if `xyz789` isn't actually a valid credential with the external service, your application will fail.

For example:

```text
External API
    │
    └── Actual credential = xyz789

Key Vault
    │
    └── Stored credential = xyz789
```

The external system and Key Vault need to be coordinated.

So secret rotation often means:

```text
Create new credential
       ↓
Store new credential in Key Vault
       ↓
Application starts using new credential
       ↓
Verify
       ↓
Revoke old credential
```

---

# 6. The safest rotation strategy

Let's say:

```text
Old API key = KEY_A
New API key = KEY_B
```

Don't immediately destroy `KEY_A`.

Instead:

```text
1. Create KEY_B
2. Store KEY_B in Key Vault
3. Make application use KEY_B
4. Verify application works
5. Revoke KEY_A
```

Conceptually:

```text
       External Service
       ┌───────────────┐
       │ KEY_A         │
       │ KEY_B         │
       └───────┬───────┘
               │
               ▼
          Azure Key Vault
               │
               └── KEY_B
                     │
                     ▼
                Application
```

Only after successful validation do you disable/remove `KEY_A`.

---

# 7. What about application caching?

This is where production systems can get tricky.

Suppose your application starts:

```text
Application startup
      ↓
Key Vault
      ↓
KEY_A
      ↓
Application memory
```

Now you rotate Key Vault:

```text
Key Vault
      ↓
KEY_B
```

But your application still has:

```text
Application memory
      ↓
KEY_A
```

So simply changing Key Vault doesn't necessarily mean your already-running application immediately stops using the old value.

---

# 8. Why caching matters

Suppose you cache:

```python
api_key = get_secret_from_key_vault()
```

for the entire lifetime of the process.

Then:

```text
12:00 → KEY_A loaded
12:30 → Key Vault changed to KEY_B
13:00 → Application still uses KEY_A
```

That's because the application has cached the old value.

Therefore:

> **Secret rotation strategy must account for application caching.**

---

# 9. Three common approaches

### Approach 1 — Retrieve on every request

```text
Request
  ↓
Key Vault
  ↓
Secret
```

Advantage:

```text
Always gets current value
```

Disadvantage:

```text
Many Key Vault calls
More latency
More dependency on Key Vault
```

Usually not ideal for high-throughput applications.

---

### Approach 2 — Load once at startup

```text
Application starts
       ↓
Key Vault
       ↓
Secret
       ↓
Memory
```

Advantage:

```text
Very few Key Vault calls
Fast runtime access
```

Disadvantage:

```text
Rotation isn't automatically picked up
```

You may need to restart/reload the application.

---

### Approach 3 — Cache with refresh

A common production pattern is:

```text
Application
     │
     ▼
Secret Cache
     │
     ├── Secret still valid → use cache
     │
     └── Refresh needed → Key Vault
```

For example:

```text
Every 5 minutes
      ↓
Check/refresh secret
```

The exact TTL should be based on your security and operational requirements.

---

# 10. Zero-downtime rotation

Now let's make this production-grade.

Suppose:

```text
Current credential = KEY_A
```

You want:

```text
New credential = KEY_B
```

A safe process can be:

```text
          External API
          /          \
       KEY_A        KEY_B
          \          /
           \        /
          Key Vault
              │
              ▼
         Application
```

### Step 1

Create KEY_B at the external provider.

```text
KEY_A ✅
KEY_B ✅
```

Both temporarily work.

---

### Step 2

Store KEY_B in Key Vault.

```text
Key Vault
│
├── KEY_A
└── KEY_B
```

Or update the relevant secret to the new credential, depending on your secret-management design.

---

### Step 3

Make the application load KEY_B.

For example:

```text
Application refresh
       ↓
Key Vault
       ↓
KEY_B
```

---

### Step 4

Verify.

```text
Application → External API
             ↓
           Success
```

---

### Step 5

Revoke KEY_A.

```text
External API
    │
    ├── KEY_A ❌
    └── KEY_B ✅
```

Now you've rotated without taking the application offline.

---

# 11. What if you have multiple application instances?

Suppose:

```text
Load Balancer
      │
 ┌────┼────┐
 ▼    ▼    ▼
App1 App2 App3
```

Initially:

```text
App1 → KEY_A
App2 → KEY_A
App3 → KEY_A
```

You rotate to KEY_B.

You need to make sure all instances eventually transition:

```text
App1 → KEY_B
App2 → KEY_B
App3 → KEY_B
```

**before** you revoke KEY_A.

Otherwise:

```text
App1 → KEY_B ✅
App2 → KEY_B ✅
App3 → KEY_A ❌
```

and App3 starts failing.

This is why rotation and caching matter in distributed systems.

---

# 12. Secret version vs external API credential

Don't confuse these.

Key Vault:

```text
Secret Version
```

is a Key Vault concept.

External service:

```text
API Key
```

is a credential issued by that external service.

You can have:

```text
Key Vault
│
└── OPENAI_API_KEY
      │
      ├── Version 1 → KEY_A
      └── Version 2 → KEY_B
```

But the actual external service may have its own credential lifecycle.

Key Vault is **storing and controlling access to the credential**; it doesn't magically manage the external provider's credential lifecycle unless you build/integrate an automated rotation process.

---

# 13. Why secret versions are valuable for rollback

Imagine:

```text
v1 → working credential
v2 → new credential
```

You deploy v2 and discover:

```text
External API calls failing
```

If v1 is still valid, you can potentially roll back to v1 while investigating.

Conceptually:

```text
v2 ❌
 ↓
rollback
 ↓
v1 ✅
```

This is one reason controlled credential transitions are safer than destructive replacement.

---

# 14. Key Vault isn't necessarily queried every time

This is another interview point.

If your application calls:

```python
client.get_secret("OPENAI_API_KEY")
```

that doesn't mean your whole architecture should necessarily make a Key Vault network call for every business request.

A better architecture can be:

```text
Application
     │
     ▼
Secret Provider
     │
     ▼
Cache
     │
     ▼
Key Vault
```

The application can use a controlled refresh strategy.

---

# 15. What if the Key Vault itself is temporarily unavailable?

If your application depends on Key Vault at runtime:

```text
Application
    │
    ▼
Key Vault
```

you should consider failure behavior.

For example:

```text
Key Vault unavailable
       ↓
Can cached credential still be used?
       ↓
Yes → continue temporarily
No  → fail safely
```

This is an architectural decision.

For highly available applications, you need to consider:

* caching
* retry behavior
* startup failures
* Key Vault availability
* secret refresh
* monitoring

---

# 16. Don't over-cache sensitive credentials

Caching reduces Key Vault calls, but there is a trade-off.

Long cache:

```text
Low Key Vault traffic
+
Old credential may remain longer
```

Short cache:

```text
More Key Vault traffic
+
Faster rotation propagation
```

So:

```text
Security
    ↕
Performance
    ↕
Availability
```

You need to choose a strategy appropriate for your application.

---

# 17. Interview question

### "How would you rotate an API key stored in Key Vault without downtime?"

A strong answer:

> "I would first create the new credential with the external provider while keeping the old credential valid. I'd store the new credential in Key Vault and ensure all application instances refresh and start using it. After validating that the new credential works across the deployment, I'd revoke the old credential. I'd also account for application-side caching so that no instance continues using the old credential after it has been revoked."

That's a strong production-level answer.

---

# 18. Another interview question

### "If I update a secret in Key Vault, will my application automatically use the new value?"

The correct answer is:

> **"Not necessarily."**

It depends on how the application retrieves and caches the secret.

If the application:

```text
reads on every request
```

it can see the latest value.

If it:

```text
loads once at startup
```

it may continue using the old value until it refreshes or restarts.

---

# 19. The complete rotation architecture

```text
                External Provider
                 /           \
                /             \
          OLD KEY             NEW KEY
              │                  │
              │                  │
              └────────┬─────────┘
                       │
                       ▼
                  Azure Key Vault
                       │
                       ▼
                Secret Version
                       │
                       ▼
                Application Cache
                       │
                       ▼
                  App Instances
                  /     |      \
                App1   App2    App3
                       │
                       ▼
                External Provider
```

Rotation:

```text
Create NEW
    ↓
Store NEW
    ↓
Refresh applications
    ↓
Validate
    ↓
Revoke OLD
```

---

# Key takeaway

Remember this sequence:

```text
Credential rotation ≠ just changing a Key Vault value
```

A proper production rotation is:

```text
Create new credential
        ↓
Store it securely
        ↓
Propagate to applications
        ↓
Verify
        ↓
Revoke old credential
```

And always consider:

```text
Caching
Multiple instances
Rollback
Availability
```

---

## Next: Phase 3 — Topic 4: Key Vault References in Azure App Service

This is a very useful Azure feature.

Instead of writing:

```python
client.get_secret(...)
```

you can configure an **App Service setting that references a Key Vault secret**, while the App Service uses its Managed Identity to resolve it.

We'll compare:

```text
Python → Key Vault
```

vs

```text
App Service → Key Vault → Environment Setting → Python
```

and discuss **when each approach is better**.
