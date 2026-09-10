# 5. Custom Exceptions ⭐

Sometimes Python's built-in exceptions don't clearly describe your application's problem.

For example, suppose you're building a banking application.

You could do:

```python
raise ValueError("Insufficient balance")
```

But `ValueError` is quite generic.

Instead, you can create your own exception:

```python
class InsufficientBalanceError(Exception):
    pass
```

Now you have a **custom exception**.

---

## 1. Why create custom exceptions?

Imagine these business rules:

```text
Insufficient balance
Invalid account
Payment already processed
User not authorized
Order already cancelled
```

These aren't really Python errors. They are **application/business errors**.

Custom exceptions make them explicit.

---

# 2. Creating a custom exception

```python
class InsufficientBalanceError(Exception):
    pass
```

That's enough.

The important part is:

```python
(Exception)
```

Your custom exception inherits from Python's built-in `Exception`.

So conceptually:

```text
Exception
    ↓
InsufficientBalanceError
```

---

# 3. Raising your custom exception

```python
class InsufficientBalanceError(Exception):
    pass


balance = 1000
withdraw = 1500

if withdraw > balance:
    raise InsufficientBalanceError("Insufficient balance")
```

Python produces:

```text
InsufficientBalanceError: Insufficient balance
```

---

# 4. Catching your custom exception

You handle it exactly like a built-in exception:

```python
class InsufficientBalanceError(Exception):
    pass


try:
    balance = 1000
    withdraw = 1500

    if withdraw > balance:
        raise InsufficientBalanceError("Insufficient balance")

except InsufficientBalanceError as e:
    print(e)
```

Output:

```text
Insufficient balance
```

---

# 5. Real-world example

Imagine an order system:

```python
class OrderAlreadyCancelledError(Exception):
    pass


def cancel_order(order_status):
    if order_status == "cancelled":
        raise OrderAlreadyCancelledError(
            "Order has already been cancelled"
        )

    print("Order cancelled")
```

Then:

```python
try:
    cancel_order("cancelled")

except OrderAlreadyCancelledError as e:
    print(e)
```

Output:

```text
Order has already been cancelled
```

This is much clearer than:

```python
raise ValueError("Order has already been cancelled")
```

because the exception itself tells you **what went wrong**.

---

# 6. Custom exceptions can have their own data

You can make them more powerful.

```python
class InsufficientBalanceError(Exception):

    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount

        super().__init__(
            f"Balance: {balance}, requested: {amount}"
        )
```

Then:

```python
raise InsufficientBalanceError(1000, 1500)
```

You can access:

```python
except InsufficientBalanceError as e:
    print(e.balance)
    print(e.amount)
```

Output:

```text
1000
1500
```

This is useful when the application needs structured information about the failure.

---

# 7. Custom exception hierarchy ⭐

You can create a hierarchy of your own exceptions:

```python
class PaymentError(Exception):
    pass


class PaymentFailedError(PaymentError):
    pass


class PaymentTimeoutError(PaymentError):
    pass
```

Now:

```text
Exception
    ↓
PaymentError
    ├── PaymentFailedError
    └── PaymentTimeoutError
```

You can catch a specific error:

```python
except PaymentTimeoutError:
    print("Payment timed out")
```

Or catch **all payment-related errors**:

```python
except PaymentError:
    print("Payment failed")
```

This becomes very useful in large applications.

---

# 8. Interview question ⭐

### Why use custom exceptions?

Good answer:

> "Custom exceptions allow us to represent application-specific or business-specific errors clearly. They make error handling more meaningful and allow different parts of the application to handle specific business failures independently."

---

## One important distinction

Don't create a custom exception for everything.

If Python already has an appropriate exception:

```python
int("abc")
```

use:

```python
ValueError
```

rather than creating:

```python
InvalidIntegerError
```

Use custom exceptions when the error represents a **specific application/business condition**.

---

### Remember this pattern

```python
class MyError(Exception):
    pass


try:
    if something_is_wrong:
        raise MyError("Something went wrong")

except MyError as e:
    print(e)
```

**Next → Exception hierarchy and `Exception` vs `BaseException`**, which explains *why* `except Exception` can catch many different errors.
