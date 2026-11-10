# Python Memory Management – Section 2: Reference Counting

Reference counting is one of the most important Python memory-management concepts for interviews, especially Python-heavy AI Engineer roles.

The main idea is simple:

Python keeps track of how many references point to an object. When an object's reference count reaches zero, CPython can generally deallocate it immediately.

Let's understand all 17 questions with examples.

## 21. What is reference counting in Python?

Interview answer:

Reference counting is a memory-management technique used by CPython to track how many references point to an object.

When an object has no remaining strong references, its reference count reaches zero, and CPython can deallocate it.

Example:

```
a = [10, 20, 30]
b = a
c = a

del b
del c
del a
```

Understand the reference count:

Step 1: Create a list

List object `[10, 20, 30]`

1 reference

a → list

Step 2: Assign b = a and c = a

List object `[10, 20, 30]`

3 references

a → list · b → list · c → list

Step 3: Delete b and c

List object `[10, 20, 30]`

1 reference

Only a → list

Step 4: Delete a

List object

0 references

Eligible for deallocation

## 22. How does reference counting work internally?

Interview answer:

In CPython, each object has an internal reference count maintained by the Python runtime.

When references to an object are created or removed, its reference count is adjusted.

When the count reaches zero, CPython generally deallocates the object and releases its owned resources.

Example:

```
import sys

a = [10, 20]

print(sys.getrefcount(a))

b = a

print(sys.getrefcount(a))

del b

print(sys.getrefcount(a))
```

Conceptually, the reference count changes like this:

| Operation      | References from our code |
| -------------- | ------------------------ |
| `a = [10, 20]` | 1                        |
| `b = a`        | 2                        |
| `del b`        | 1                        |
| `del a`        | 0                        |

The exact values from `sys.getrefcount()` will be higher because the function call itself temporarily creates another reference.

## 23. What is a reference count?

Interview answer:

A reference count is the number of strong references currently pointing to an object.

For example:

```
a = [1, 2, 3]
b = a
c = a
```

The list has three references from these variable bindings.

```
a ─────┐
b ─────┼────> [1, 2, 3]
c ─────┘
```

The reference count contributed by these bindings is 3.

Important: The actual internal count may include additional references from the interpreter or other parts of your program.

## 24. When does an object's reference count increase?

Interview answer:

An object's reference count generally increases when a new strong reference to that object is created.

Common situations include:

1. Assigning an object to another variable.
2. Adding an object to a list.
3. Adding an object as a dictionary value.
4. Passing an object to a function.
5. Returning an object from a function.
6. Capturing an object in a closure.

Example 1: Variable assignment

```
a = [10, 20]
b = a
```

The same list now has another reference.

Example 2: Adding to a list

```
a = [10, 20]
container = []

container.append(a)
```

Now both `a` and `container[0]` refer to the same list.

Example 3: Dictionary

```
a = [10, 20]
data = {"numbers": a}
```

The dictionary holds a reference to the list.

## 25. When does an object's reference count decrease?

Interview answer:

An object's reference count generally decreases when a strong reference to that object is removed.

Common situations:

1. Using `del` on a variable.
2. A local variable going out of scope.
3. Removing an object from a list.
4. Removing a dictionary entry.
5. Reassigning a variable to another object.
6. A temporary reference disappearing after an expression or function call.

Example 1: Deleting a reference

```
a = [10, 20]
b = a

del b
```

One reference is removed.

Example 2: Reassignment

```
a = [10, 20]
a = [30, 40]
```

What happens?

- Initially, `a` refers to `[10, 20]`.
- A new list `[30, 40]` is created.
- `a` is rebound to the new list.
- The old list loses the reference held by `a`.

If no other references to the old list exist, it becomes eligible for deallocation.

## 26. What happens when an object's reference count reaches zero?

Interview answer:

When an object's reference count reaches zero in CPython, the object can generally be deallocated immediately.

During deallocation:

1. The object's cleanup logic runs.
2. Resources owned by the object are released as appropriate.
3. References held by the object to other objects are released.
4. The object's memory is made available to the allocator for reuse.

Example:

```
a = [10, 20, 30]

del a
```

If no other references exist, the list is deallocated.

Interview follow-up: Does this mean the memory is immediately returned to the operating system?

No. CPython may retain the memory in its allocator for reuse.

## 27. How can you check an object's reference count?

Interview answer:

We can use the `sys.getrefcount()` function from Python's `sys` module to inspect an object's reference count in CPython.

Example:

```
import sys

a = [10, 20, 30]

print(sys.getrefcount(a))
```

Output will typically be:

```
2
```

Why 2?

- One reference from variable `a`.
- One temporary reference created when passing `a` to `getrefcount()`.

The exact count can vary depending on the Python implementation and execution context.

## 28. What is the purpose of `sys.getrefcount()`?

Interview answer:

`sys.getrefcount()` is used to inspect an object's reference count, mainly for debugging and understanding object references in CPython.

Example:

```
import sys

a = [1, 2, 3]
print(sys.getrefcount(a))

b = a
print(sys.getrefcount(a))

del b
print(sys.getrefcount(a))
```

Expected conceptual behavior:

```
2
3
2
```

The additional reference is from the function argument.

Important: It is not a perfect tool for determining the exact number of references in a running program.

## 29. Why does `sys.getrefcount()` return a value higher than expected?

Interview answer:

Because passing an object to `sys.getrefcount()` itself creates a temporary reference to that object.

Example:

```
import sys

a = []

print(sys.getrefcount(a))
```

You might expect `1`, because only `a` refers to the list.

But the output is typically `2`:

```
2
```

Visual explanation:

```
a ──────────────────┐
                    |
getrefcount argument ├──> []
                    |
```

So the additional reference comes from the function call.

## 30. Does assigning an object to another variable increase its reference count?

Interview answer:

Yes. Assigning an existing object to another variable creates another reference to the same object.

Example:

```
a = [10, 20]
b = a
```

Now both variables refer to the same list.

```
a ─────┐
       ├────> [10, 20]
b ─────┘
```

The reference count increases by one for the additional binding, conceptually.

## 31. Does passing an object to a function increase its reference count?

Interview answer:

In CPython, passing an object to a function creates a reference in the function's execution context, so the reference count generally increases while that reference is held.

Example:

```
import sys

def display(obj):
    print(sys.getrefcount(obj))

a = [10, 20]

print(sys.getrefcount(a))
display(a)
```

The function parameter `obj` refers to the same list as `a`.

When the function finishes, the local parameter reference is released.

Important: Python uses object references when passing arguments; it does not automatically copy the object.

## 32. What happens to reference counts when a function returns?

Interview answer:

When a function finishes, its local references are released. However, if the function returns an object, the returned reference keeps that object alive.

Example 1: Function does not return the object

```
def create():
    numbers = [10, 20, 30]

create()
```

After the function finishes, its local reference disappears. If no other references exist, the list can be deallocated.

Example 2: Function returns the object

```
def create():
    numbers = [10, 20, 30]
    return numbers

result = create()
```

Here, `result` holds a reference to the returned list, so it survives after the function finishes.

## 33. What happens to reference counts when you delete a variable?

Interview answer:

When we use `del`, Python removes the variable's binding to the object. The object's reference count generally decreases by one if that binding was a strong reference.

Example:

```
a = [10, 20]
b = a

del a

print(b)
```

Output:

```
[10, 20]
```

The object remains alive because `b` still refers to it.

Remember: `del` deletes the reference, not necessarily the object.

## 34. Is reference counting enough to manage all Python memory?

Interview answer:

No. Reference counting alone cannot handle unreachable circular references.

For example:

```
a = []
b = []

a.append(b)
b.append(a)

del a
del b
```

The two lists still reference each other.

Even though we deleted the external variable references, their internal references remain.

Conceptually:

```
List A ─────> List B
   ^             |
   |_____________|
```

Their reference counts remain nonzero, even though neither is reachable from the program's roots.

Python uses cyclic garbage collection to detect and reclaim such unreachable cycles.

## 35. What are the limitations of reference counting?

Interview answer:

The main limitations are:

1. Circular references: Reference counting alone cannot collect unreachable cycles.
2. Performance overhead: Reference counts must be updated as references are created and removed.
3. Not a complete leak detector: Objects that remain referenced unintentionally will not be deallocated.
4. Implementation differences: Not every Python implementation uses the same reference-counting strategy.

Example of an unintended reference:

```
cache = []

def store_data():
    data = [1, 2, 3]
    cache.append(data)
```

Even after `store_data()` finishes, the list remains alive because `cache` still references it.

This is an example of memory being retained unintentionally.

## 36. Does Python use reference counting in every implementation?

Interview answer:

No. Reference counting is an implementation detail, not a requirement of the Python language.

- CPython: Uses reference counting along with cyclic garbage collection.
- PyPy: Primarily uses a tracing garbage collector rather than CPython-style reference counting.
- Other implementations: May use different memory-management techniques.

Interview tip: When explaining reference counting, say "CPython uses reference counting" rather than claiming every Python implementation does.

## 37. Is reference counting the same as garbage collection?

Interview answer:

No. Reference counting and garbage collection are related but different memory-management techniques.

| Reference counting                                    | Cyclic garbage collection                                 |
| ----------------------------------------------------- | --------------------------------------------------------- |
| Tracks references to objects                          | Detects unreachable reference cycles                      |
| Used by CPython for normal object lifetime management | Supplements reference counting                            |
| Can deallocate objects when count reaches zero        | Reclaims unreachable cycles with nonzero reference counts |
| Usually acts immediately when count reaches zero      | Runs periodically or when triggered manually              |

Example:

Reference counting:

```
a = [10, 20]
del a
```

Cyclic garbage collection:

```
a = []
b = []

a.append(b)
b.append(a)

del a
del b

import gc
gc.collect()
```

The second example demonstrates why cyclic garbage collection is needed.

# Quick revision – Reference counting

| Question                                 | Key point to remember                 |
| ---------------------------------------- | ------------------------------------- |
| What is reference counting?              | Tracks references to objects          |
| What increases reference count?          | Creating strong references            |
| What decreases reference count?          | Removing strong references            |
| What happens at zero?                    | CPython can deallocate the object     |
| How to inspect it?                       | `sys.getrefcount()`                   |
| Why extra count?                         | Temporary function argument reference |
| Does assignment copy objects?            | No, it binds another name             |
| Does `del` destroy objects?              | Not necessarily                       |
| Is reference counting sufficient?        | No, cycles need cyclic GC             |
| Does every Python implementation use it? | No                                    |

# Practical coding exercise

Run this code and predict the output before executing it.

```
import sys

a = [10, 20, 30]

print("1:", sys.getrefcount(a))

b = a
print("2:", sys.getrefcount(a))

c = a
print("3:", sys.getrefcount(a))

del b
print("4:", sys.getrefcount(a))

def test(obj):
    print("5:", sys.getrefcount(obj))

test(a)

del c
print("6:", sys.getrefcount(a))
```

Remember that `sys.getrefcount()` creates a temporary reference, and the function parameter `obj` is another reference while the function executes.

## Interview knowledge check

Test your understanding

0/5 answered

1\. What happens when the reference count of an object reaches zero in CPython?

It moves to the stack

It can be deallocated immediately

It is always sent to cyclic GC

2\. Why does sys.getrefcount(a) usually show one extra reference?

Because Python creates a copy

Because the function call creates a temporary reference

Because all lists have two references

3\. What happens here?

a = [1, 2]\
b = a\
del a\
print(b)

Error

None

[1, 2]

4\. Can reference counting alone collect an unreachable circular reference?

Yes, always

No

Only when gc.disable() is used

5\. Does PyPy use the same reference-counting strategy as CPython?

Yes, exactly the same

No, it primarily uses tracing garbage collection

PyPy does not manage memory

Submit answers

Next section: Circular references and cyclic garbage collection. This is a natural continuation because it explains the biggest limitation of reference counting.