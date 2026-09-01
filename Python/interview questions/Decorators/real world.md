## Real-world use case: Retry decorator

For your EPAM interview, a **retry decorator** is a very good example because it shows how decorators can handle common API/service behavior without duplicating code.

Imagine you have multiple functions calling external APIs:

```python
def get_user():
    # API call
    pass

def get_orders():
    # API call
    pass

def get_products():
    # API call
    pass
```

External APIs can temporarily fail because of:

* Network problems
* Timeout
* Temporary server errors
* Rate limits

Instead of writing retry logic inside every function, create it **once as a decorator**.

### Example

```python
from functools import wraps
import time

def retry(max_attempts):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    print(f"Attempt {attempt + 1} failed")

                    if attempt == max_attempts - 1:
                        raise

                    time.sleep(1)

        return wrapper

    return decorator
```

Now use it:

```python
@retry(3)
def call_api():
    print("Calling API...")
    raise Exception("API failed")

call_api()
```

Output:

```text
Calling API...
Attempt 1 failed

Calling API...
Attempt 2 failed

Calling API...
Attempt 3 failed
```

After the third failure, the exception is raised.

---

### Execution flow

When Python sees:

```python
@retry(3)
def call_api():
```

it effectively does:

```python
call_api = retry(3)(call_api)
```

First:

```text
retry(3)
    ↓
returns decorator
```

Then:

```text
decorator(call_api)
    ↓
returns wrapper
```

Then when you call:

```python
call_api()
```

you're actually calling:

```text
wrapper()
   ↓
try call_api()
   ↓
failure?
   ↓
retry
   ↓
retry
   ↓
success OR raise exception
```

---

### Why is this better?

Without a decorator:

```python
def get_user():
    for attempt in range(3):
        try:
            ...
        except:
            ...
```

```python
def get_orders():
    for attempt in range(3):
        try:
            ...
        except:
            ...
```

```python
def get_products():
    for attempt in range(3):
        try:
            ...
        except:
            ...
```

Lots of duplicate code.

With a decorator:

```python
@retry(3)
def get_user():
    ...

@retry(3)
def get_orders():
    ...

@retry(3)
def get_products():
    ...
```

The retry logic is centralized.

---

### EPAM interview answer

If they ask **"Give me a real-world use case for decorators"**, say:

> **"A common use case is retrying external API calls. Instead of putting retry logic in every API function, I can create a parameterized retry decorator. The decorator handles exceptions, retries the function a configured number of times, and can also implement exponential backoff. This keeps the business logic clean and avoids duplication."**

### Your decorator checklist

You should now be comfortable with:

1. **What is a decorator?**
2. **Why use decorators?**
3. **How `@decorator` works**
4. **Multiple decorators**
5. **Parameterized decorators**
6. **`functools.wraps`**
7. **Real-world retry/authentication/logging use cases**

One **very likely follow-up** is: **"What are `*args` and `**kwargs` doing inside the wrapper?"** That's worth knowing because otherwise your decorator only works with functions that take no arguments.
