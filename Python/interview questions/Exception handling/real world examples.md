# 7. Real-World Exception Handling ⭐

Now let's move from **Python syntax → production-level thinking**.

In real applications, the goal isn't just:

> "Catch the exception."

The goal is:

> **Handle failures safely, clearly, and without hiding bugs.**

---

## 1. Catch specific exceptions

❌ Avoid:

```python
try:
    data = int(user_input)
except Exception:
    print("Something went wrong")
```

You don't know what actually went wrong.

Prefer:

```python
try:
    data = int(user_input)
except ValueError:
    print("Invalid number")
```

### Why?

Because different exceptions may require different actions.

```text
ValueError          → Tell user input is invalid
FileNotFoundError   → Check whether file exists
TimeoutError        → Retry
PermissionError     → Report permission problem
```

---

# 2. Don't silently swallow exceptions ⭐

This is bad:

```python
try:
    process_payment()
except Exception:
    pass
```

The application encountered an error, but you've completely hidden it.

You might end up thinking:

```text
Payment successful
```

when actually:

```text
Payment failed
```

At minimum, log or handle the error appropriately.

---

# 3. Logging exceptions

In production, instead of:

```python
except Exception:
    print("Error")
```

you'll commonly use logging:

```python
import logging

try:
    process_payment()

except Exception:
    logging.exception("Payment processing failed")
```

`logging.exception()` is useful because it records the exception and traceback.

This helps developers diagnose:

```text
What failed?
Where did it fail?
What was the exception?
```

---

# 4. API example

Imagine calling an external API:

```python
try:
    response = call_api()

except TimeoutError:
    print("API timed out")

except ConnectionError:
    print("Could not connect to API")

except Exception:
    print("Unexpected error")
```

This is much better than treating every failure identically.

In production, you might additionally:

```text
Timeout
   ↓
Retry with backoff
   ↓
Still failing?
   ↓
Log + return controlled error
```

---

# 5. Database example

Suppose:

```python
try:
    update_database()

except ConnectionError:
    print("Database unavailable")
```

But database operations can involve another important concept:

**cleanup / rollback**.

Conceptually:

```python
try:
    begin_transaction()
    update_user()
    update_order()
    commit()

except Exception:
    rollback()

finally:
    close_connection()
```

Here each part has a purpose:

```text
try       → perform transaction
except    → rollback if something fails
finally   → release connection
```

---

# 6. Don't put too much code inside `try` ⭐

Consider:

```python
try:
    data = get_data()
    process_data(data)
    save_data(data)
    send_email()
except Exception:
    print("Something failed")
```

What failed?

Could be:

```text
get_data()
process_data()
save_data()
send_email()
```

It's difficult to know.

Instead, keep the `try` block focused:

```python
try:
    data = get_data()
except ConnectionError:
    print("Could not get data")
    return

process_data(data)
save_data(data)
send_email()
```

### Rule:

> **Keep the `try` block as small as reasonably possible.**

This makes error handling more precise.

---

# 7. Don't use exceptions for normal control flow

Avoid things like:

```python
try:
    value = my_dict["name"]
except KeyError:
    value = "Unknown"
```

This can be valid in some situations, but if you're simply checking whether a key exists, you could use:

```python
value = my_dict.get("name", "Unknown")
```

Exceptions are primarily for **exceptional situations**, not every normal decision.

---

# 8. Use `finally` for cleanup

Example:

```python
connection = None

try:
    connection = create_connection()
    process_data(connection)

except ConnectionError:
    print("Connection failed")

finally:
    if connection:
        connection.close()
```

The important principle:

> Resources that need to be released should be cleaned up even when an error occurs.

This is one reason `finally` exists.

---

# 9. Context managers are often even better ⭐

For files, you normally don't need to manually use `finally`.

Instead:

```python
with open("data.txt") as file:
    data = file.read()
```

Python automatically handles closing the file.

Conceptually:

```text
with
 ↓
open resource
 ↓
use resource
 ↓
exception or success
 ↓
cleanup automatically
```

So in modern Python:

```python
with open(...) as f:
```

is generally preferable to manually doing:

```python
try:
    f = open(...)
finally:
    f.close()
```

We'll cover **context managers** separately later in your Python roadmap.

---

# 10. Production pattern ⭐

A common pattern is:

```python
def process_order(order):

    try:
        validate_order(order)
        result = process_payment(order)
        save_order(result)

    except ValueError as e:
        logger.warning("Invalid order: %s", e)
        return "Invalid order"

    except TimeoutError:
        logger.error("Payment service timed out")
        return "Please try again"

    except Exception:
        logger.exception("Unexpected error")
        raise
```

Notice something important:

```python
except Exception:
    logger.exception(...)
    raise
```

We **log it and re-raise it**.

We're not hiding an unexpected programming/system error.

---

# 🎯 Interview Best Practices

If an interviewer asks:

> **"What are some best practices for exception handling in Python?"**

Give these points:

1. **Catch specific exceptions** rather than blindly catching `Exception`.
2. **Don't silently swallow exceptions.**
3. Use **logging** for production diagnostics.
4. Keep the `try` block **small and focused**.
5. Use `finally` or context managers for **cleanup**.
6. Use `raise` when you need to **propagate an error**.
7. Use **custom exceptions** for application-specific errors.
8. Don't use exceptions unnecessarily for normal control flow.

---

## 🧠 Complete Exception Handling Picture

You've now covered the major concepts:

```text
try / except
     ↓
multiple except
     ↓
else / finally
     ↓
raise
     ↓
custom exceptions
     ↓
exception hierarchy
     ↓
production best practices
```

### One last topic remains: **exception chaining** ⭐

For example:

```python
try:
    ...
except ValueError as e:
    raise RuntimeError("Processing failed") from e
```

This is a **very good interview topic**, especially for senior Python roles.
