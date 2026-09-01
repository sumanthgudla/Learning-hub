Let's start with the **most important interview question: Why do we use decorators?**

### Why use decorators?

We use decorators when we want to **add common behavior to multiple functions without modifying their original code**.

For example, suppose you have these functions:

```python
def get_user():
    print("Fetching user")

def create_user():
    print("Creating user")

def delete_user():
    print("Deleting user")
```

Now you want to **log every function call**.

Without decorators, you might have to modify every function:

```python
def get_user():
    print("Function started")
    print("Fetching user")
    print("Function completed")

def create_user():
    print("Function started")
    print("Creating user")
    print("Function completed")
```

This causes **duplicate code**.

Instead, create the logging behavior once:

```python
def log(func):
    def wrapper():
        print("Function started")
        func()
        print("Function completed")

    return wrapper
```

Then apply it:

```python
@log
def get_user():
    print("Fetching user")

@log
def create_user():
    print("Creating user")
```

Now:

```python
get_user()
```

Output:

```text
Function started
Fetching user
Function completed
```

### The key idea

Think of a decorator as:

> **"Take an existing function and wrap additional behavior around it."**

So:

```text
Original function
       ↓
   Decorator
       ↓
Function + additional behavior
```

### Why are decorators useful?

They help with **cross-cutting concerns** — behavior that is needed across many functions.

Common examples:

| Use case       | What decorator does                    |
| -------------- | -------------------------------------- |
| Logging        | Logs function calls                    |
| Authentication | Checks whether user is authorized      |
| Timing         | Measures execution time                |
| Caching        | Stores previous results                |
| Retry          | Retries failed API calls               |
| Validation     | Validates inputs                       |
| Transactions   | Starts/commits/rolls back transactions |

For your **EPAM Python interview**, a strong answer would be:

> **"Decorators are used to add or modify the behavior of a function without changing its original implementation. They help us avoid duplicate code, especially for cross-cutting concerns like logging, authentication, caching, retries, and performance monitoring."**

Next, the natural question is **how `@decorator` actually works**.
