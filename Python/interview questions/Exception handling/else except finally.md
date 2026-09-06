# 3. `else` and `finally` ⭐

This is one of the **most important exception-handling topics for interviews**.

We already know:

```python
try:
    # risky code
except:
    # handle error
```

Python also gives us:

```python
try:
    ...
except:
    ...
else:
    ...
finally:
    ...
```

Let's understand them one by one.

---

## 1. `else`

The `else` block runs **only when NO exception occurs** in `try`.

```python
try:
    result = 10 / 2

except ZeroDivisionError:
    print("Error")

else:
    print("Calculation successful")
```

Output:

```text
Calculation successful
```

Because:

```text
try
 ↓
10 / 2
 ↓
No exception
 ↓
else
 ↓
Calculation successful
```

---

### What if an exception occurs?

```python
try:
    result = 10 / 0

except ZeroDivisionError:
    print("Error")

else:
    print("Calculation successful")
```

Output:

```text
Error
```

`else` does **not** execute.

So remember:

> **`else` = execute when `try` succeeds.**

---

# 2. Why do we even need `else`?

Consider:

```python
try:
    result = 10 / 2
    print("Saving result...")
    save_to_database(result)

except Exception:
    print("Something failed")
```

The `except` could potentially handle an exception from **both** the calculation and `save_to_database()`.

Sometimes we want the `try` block to contain only the code where we expect the exception.

We can do:

```python
try:
    result = 10 / 2

except ZeroDivisionError:
    print("Calculation failed")

else:
    print("Saving result...")
    save_to_database(result)
```

Now it's clearer:

```text
try    → code where exception is expected
except → handle failure
else   → code that should run after successful try
```

---

# 3. `finally`

`finally` is different.

It is used for **cleanup code**.

```python
try:
    result = 10 / 2

except ZeroDivisionError:
    print("Error")

finally:
    print("Cleanup")
```

Output:

```text
Cleanup
```

The important thing is that `finally` runs **whether or not an exception occurs**.

---

## No exception

```python
try:
    print("Try")

except:
    print("Except")

finally:
    print("Finally")
```

Output:

```text
Try
Finally
```

---

## Exception occurs

```python
try:
    print("Try")
    10 / 0

except ZeroDivisionError:
    print("Except")

finally:
    print("Finally")
```

Output:

```text
Try
Except
Finally
```

So:

```text
             Exception? 
                 │
          ┌──────┴──────┐
         YES            NO
          ↓              ↓
       except          else
          └──────┬───────┘
                 ↓
              finally
```

---

# 4. Real-world example

Imagine you're working with a file:

```python
file = open("data.txt")

try:
    data = file.read()

except Exception:
    print("Something went wrong")

finally:
    file.close()
```

Why `finally`?

Because regardless of whether reading the file succeeds or fails, we want to **close the file**.

Other examples:

* Closing database connections
* Releasing locks
* Closing network connections
* Cleaning temporary resources

---

# 5. `try + except + else + finally`

You can use all four together:

```python
try:
    number = int(input("Enter number: "))
    result = 100 / number

except ValueError:
    print("Invalid number")

except ZeroDivisionError:
    print("Cannot divide by zero")

else:
    print("Result:", result)

finally:
    print("Execution completed")
```

### Input: `10`

```text
Result: 10.0
Execution completed
```

### Input: `0`

```text
Cannot divide by zero
Execution completed
```

### Input: `abc`

```text
Invalid number
Execution completed
```

Notice:

**`finally` runs in all three cases.**

---

# 6. The interview table ⭐

| Block     | When does it execute?                  |
| --------- | -------------------------------------- |
| `try`     | Always attempted                       |
| `except`  | When a matching exception occurs       |
| `else`    | When NO exception occurs               |
| `finally` | Almost always, regardless of exception |

The simplest way to remember:

```text
try      → Try this
except   → If it fails, handle it
else     → If it succeeds, do this
finally  → Do this regardless
```

---

# 7. Very common interview question

### What is the difference between `else` and `finally`?

**Answer:**

> `else` executes only when the `try` block completes without an exception, whereas `finally` executes regardless of whether an exception occurs and is commonly used for cleanup.

That's a **good interview-ready answer**.

---

### One subtle point

Don't say:

> "`finally` always executes."

It's better to say:

> "`finally` normally executes regardless of whether an exception occurs."

There are extreme situations such as forced process termination where Python may not get a chance to execute it.

---

## 🎯 Quick test

What will this print?

```python
try:
    print("A")
    x = 10 / 0
    print("B")

except ZeroDivisionError:
    print("C")

else:
    print("D")

finally:
    print("E")

print("F")
```

Think about the execution order before moving on.
