Here's **Phase 2 — Topic 7: Recursion** in notes-friendly format:

---

# Phase 2 — Topic 7: Recursion

## What is it?
Recursion is when a **function calls itself** to solve a smaller version of the same problem. Every recursive solution has two parts — a **base case** (stops the recursion) and a **recursive case** (calls itself with a smaller input). Senior devs must understand not just how to write recursion but what happens in memory (call stack) and when to avoid it.

---

## 1. The Two Rules of Recursion

```python
# RULE 1 — Base case — when to STOP
# RULE 2 — Recursive case — call yourself with SMALLER input

def countdown(n):
    if n == 0:          # BASE CASE — stop here
        print("Done!")
        return
    print(n)
    countdown(n - 1)    # RECURSIVE CASE — smaller input

countdown(5)
# 5
# 4
# 3
# 2
# 1
# Done!
```

---

## 2. What Happens in Memory — Call Stack

```python
def countdown(n):
    if n == 0:
        print("Done!")
        return
    print(n)
    countdown(n - 1)

countdown(3)
```

```
CALL STACK — grows downward with each call

countdown(3) → prints 3
    countdown(2) → prints 2
        countdown(1) → prints 1
            countdown(0) → prints "Done!" → RETURNS
        countdown(1) → RETURNS
    countdown(2) → RETURNS
countdown(3) → RETURNS

Stack builds UP then unwinds DOWN
Each function call waits for the one below it to finish
```

---

## 3. Classic Examples

### Factorial
```python
# n! = n × (n-1) × (n-2) × ... × 1
# 5! = 5 × 4 × 3 × 2 × 1 = 120

def factorial(n):
    if n == 0 or n == 1:    # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))   # 120

# What happens:
# factorial(5)
#   = 5 * factorial(4)
#   = 5 * 4 * factorial(3)
#   = 5 * 4 * 3 * factorial(2)
#   = 5 * 4 * 3 * 2 * factorial(1)
#   = 5 * 4 * 3 * 2 * 1
#   = 120
```

---

### Fibonacci
```python
# fib(n) = fib(n-1) + fib(n-2)
# 0,1,1,2,3,5,8,13,21...

def fib(n):
    if n <= 1:              # base case
        return n
    return fib(n-1) + fib(n-2)   # recursive case

print(fib(6))   # 8

# What happens for fib(4):
#           fib(4)
#          /      \
#       fib(3)   fib(2)
#       /    \   /    \
#    fib(2) fib(1) fib(1) fib(0)
#    /    \
# fib(1) fib(0)
# result: 3
```

---

### Sum of List
```python
def sum_list(lst):
    if len(lst) == 0:       # base case — empty list
        return 0
    return lst[0] + sum_list(lst[1:])  # first + rest

print(sum_list([1, 2, 3, 4, 5]))   # 15

# What happens:
# sum_list([1,2,3,4,5])
#   = 1 + sum_list([2,3,4,5])
#   = 1 + 2 + sum_list([3,4,5])
#   = 1 + 2 + 3 + sum_list([4,5])
#   = 1 + 2 + 3 + 4 + sum_list([5])
#   = 1 + 2 + 3 + 4 + 5 + sum_list([])
#   = 1 + 2 + 3 + 4 + 5 + 0
#   = 15
```

---

## 4. Recursion Depth — Stack Overflow

```python
# Python has a recursion limit — default 1000
import sys
print(sys.getrecursionlimit())   # 1000

def infinite(n):
    return infinite(n + 1)   # no base case!

infinite(0)   # RecursionError: maximum recursion depth exceeded


# Check current depth
def count_depth(n):
    print(f"depth: {n}")
    count_depth(n + 1)

count_depth(0)   # crashes at ~1000


# Increase limit — use carefully
sys.setrecursionlimit(10000)   # not recommended for deep recursion
```

---

## 5. Recursion vs Iteration — When to Use Which

```python
# FACTORIAL — recursion
def factorial_recursive(n):
    if n == 0: return 1
    return n * factorial_recursive(n - 1)

# FACTORIAL — iteration
def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

# Both give same result
# Iterative is FASTER — no function call overhead
# Iterative is SAFER — no stack overflow risk


# BUT some problems are NATURALLY recursive:
# → tree traversal
# → directory/file system traversal
# → JSON/nested data parsing
# → divide and conquer algorithms (merge sort, binary search)
```

---

## 6. Memoization — Fix Slow Recursion

```python
# PROBLEM — naive fibonacci is extremely slow
# fib(40) makes 300 million function calls!
# fib(3) gets calculated over and over

# fib(5) call tree — fib(2) calculated 3 times!
#           fib(5)
#          /      \
#       fib(4)   fib(3)
#       /    \   /    \
#    fib(3) fib(2) fib(2) fib(1)
#    ...

# FIX 1 — manual memoization (cache results)
def fib(n, cache={}):
    if n in cache:
        return cache[n]      # return cached result
    if n <= 1:
        return n
    cache[n] = fib(n-1) + fib(n-2)   # store result
    return cache[n]

print(fib(100))   # instant!  ← without memo: never finishes


# FIX 2 — use @lru_cache decorator (cleaner)
from functools import lru_cache

@lru_cache(maxsize=None)
def fib(n):
    if n <= 1: return n
    return fib(n-1) + fib(n-2)

print(fib(100))   # 354224848179261915075  — instant!
```

---

## 7. Real World Recursion — Flatten Nested List

```python
# Nested list — unknown depth
nested = [1, [2, 3], [4, [5, 6]], [7, [8, [9]]]]

def flatten(lst):
    result = []
    for item in lst:
        if isinstance(item, list):    # if it's a list — go deeper
            result.extend(flatten(item))   # recursive call
        else:
            result.append(item)       # base case — just a number
    return result

print(flatten(nested))
# [1, 2, 3, 4, 5, 6, 7, 8, 9]


# Directory tree traversal — same pattern
import os

def list_files(path, indent=0):
    for item in os.listdir(path):
        print(" " * indent + item)
        full_path = os.path.join(path, item)
        if os.path.isdir(full_path):
            list_files(full_path, indent + 2)   # recurse into folder
```

---

## 8. Binary Search — Recursive

```python
def binary_search(arr, target, low=0, high=None):
    if high is None:
        high = len(arr) - 1

    if low > high:          # base case — not found
        return -1

    mid = (low + high) // 2

    if arr[mid] == target:  # base case — found
        return mid
    elif arr[mid] < target:
        return binary_search(arr, target, mid+1, high)  # right half
    else:
        return binary_search(arr, target, low, mid-1)   # left half


arr = [1, 3, 5, 7, 9, 11, 13, 15]
print(binary_search(arr, 7))    # 3  ← index
print(binary_search(arr, 6))    # -1 ← not found
```

---

## Interview Questions They Actually Ask

**Q1: What are the two essential parts of a recursive function?**
> **Base case** — the condition that stops recursion and returns a value directly. **Recursive case** — calls itself with a smaller/simpler input moving toward the base case. Without a base case you get infinite recursion and a stack overflow.

**Q2: What is the call stack and how does recursion use it?**
> The call stack is a region of memory that tracks active function calls. Each recursive call adds a new **stack frame** storing local variables and return address. When base case is reached, frames are popped off one by one. Too many recursive calls = stack overflow (`RecursionError`).

**Q3: Why is naive Fibonacci O(2ⁿ)?**
> Each call branches into two more calls. For `fib(n)` this creates a binary tree of calls with ~2ⁿ nodes. With memoization it becomes O(n) because each value is computed only once.

**Q4: When would you choose recursion over iteration?**
> Recursion is preferred for **naturally recursive structures** — trees, graphs, nested data, divide-and-conquer algorithms. Iteration is preferred when the problem is linear and you need maximum performance or must avoid stack overflow risk.

**Q5: What is tail recursion and does Python optimize it?**
> Tail recursion is when the recursive call is the **last operation** in the function — nothing happens after it returns. Many languages optimize this to avoid stack growth. **Python does NOT optimize tail recursion** — each call still adds a stack frame. This is a deliberate design choice by Guido van Rossum.

---

## Practice Problems

**Beginner — `p2_t07_prac01_basics.py`**
Write recursive functions for:
1. Sum of digits of a number (`sum_digits(1234)` → `10`)
2. Reverse a string (`reverse("hello")` → `"olleh"`)
    3. Check if a string is a palindrome (`is_palindrome("racecar")` → `True`)

---

**Senior level — `p2_t07_prac02_nested.py`**
Write a recursive function `deep_sum` that sums ALL numbers in a deeply nested structure — lists inside lists inside lists, any depth.
```python
data = [1, [2, 3], [4, [5, [6, 7]]], [[[8, 9], 10]]]
print(deep_sum(data))   # 55

# Also write deep_count — count how many numbers exist
print(deep_count(data))   # 10
```

---

## Common Mistakes & Senior Traps

- **Missing base case** — function calls itself forever → `RecursionError`. Always define when to stop FIRST.
- **Base case never reached** — if input never gets smaller you still get infinite recursion. Make sure recursive call moves toward base case.
- **Mutable default argument in memo** — `def fib(n, cache={})` works but shares cache across all calls globally. Use `@lru_cache` instead — cleaner and safer.
- **Slicing creates new lists** — `sum_list(lst[1:])` creates a new list each call — O(n) space per call. Pass index instead for efficiency: `sum_list(lst, index+1)`.
- **Python has no tail call optimization** — deep recursion always risks stack overflow. For n > 1000 consider iterative approach or increase recursion limit carefully.

---

Say **next** for Topic 8: Classes & Objects!