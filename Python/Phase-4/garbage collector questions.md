Let's cover Python Garbage Collection (GC) from the basics to interview-level understanding. I'll explain each question with simple examples, internal working, and important interview points.

One important thing to understand first:

Python uses two mechanisms for memory management:

1. Reference Counting – primarily handles object cleanup immediately when references disappear.
2. Cyclic Garbage Collection – detects circular references that reference counting cannot clean up.

# 3. Garbage Collection (GC)

## 38. What is garbage collection in Python?

Garbage collection is the process of identifying and cleaning up objects that are no longer being used by a program.

Python automatically manages memory, so developers generally don't need to manually free memory.

Example:

```
class Employee:
    pass

emp = Employee()

emp = None
```

What happens?

1. An Employee object is created in memory.
2. `emp` refers to that object.
3. `emp = None` removes the reference to the Employee object.
4. If no other references exist, its reference count becomes zero.
5. Python can reclaim its memory.

Interview answer: Garbage collection is Python's automatic memory management mechanism that reclaims memory occupied by objects that are no longer reachable or needed.

## 39. Why does Python need garbage collection?

Python needs garbage collection to:

- Prevent unnecessary memory usage.
- Reclaim memory occupied by unused objects.
- Handle circular references.
- Reduce manual memory management.
- Improve application stability.

Without garbage collection, unused objects could occupy memory unnecessarily.

## 40. Difference between reference counting and garbage collection?

This is an important interview question.

| Reference Counting                      | Cyclic Garbage Collection              |
| --------------------------------------- | -------------------------------------- |
| Tracks object references                | Detects unreachable reference cycles   |
| Counts references to an object          | Examines relationships between objects |
| Usually immediate cleanup at zero       | Runs periodically or manually          |
| Cannot handle circular references alone | Can collect circular references        |
| Core memory management mechanism        | Additional cleanup mechanism           |

Example of reference counting:

```
import sys

class Employee:
    pass

emp = Employee()

print(sys.getrefcount(emp))

emp2 = emp

print(sys.getrefcount(emp))

del emp2

print(sys.getrefcount(emp))
```

The reference count increases when another variable points to the same object.

Remember: Reference counting is not the same as the cyclic garbage collector. Both contribute to Python memory management.

## 41. How does Python's garbage collector work?

Python primarily uses two mechanisms:

1\. Reference Counting

- Every object maintains a reference count.
- When a reference is added, the count increases.
- When a reference is removed, the count decreases.
- When the count reaches zero, the object can be deallocated.

2\. Cyclic Garbage Collection

- Detects groups of objects referencing each other.
- Identifies objects that cannot be reached from outside the group.
- Collects unreachable cycles.

Example:

```
a = []
b = []

a.append(b)
b.append(a)
```

Here:

- `a` references `b`.
- `b` references `a`.
- Both objects reference each other.

Even if external references disappear, their reference counts won't become zero.

Python's cyclic garbage collector handles this situation.

## 42. What is cyclic garbage collection?

Cyclic garbage collection is the mechanism that identifies and removes objects involved in circular references when those objects are no longer reachable.

Example:

```
a = []
b = []

a.append(b)
b.append(a)

del a
del b
```

Although `a` and `b` are deleted, the two lists still reference each other.

Their reference counts remain above zero.

Python's cyclic garbage collector can identify and reclaim them.

## 43. What is a circular reference?

A circular reference occurs when two or more objects reference each other, directly or indirectly, forming a cycle.

Example:

```
class Employee:
    pass

a = Employee()
b = Employee()

a.manager = b
b.employee = a
```

Visual representation:

## Circular reference

Object A

Object B

Each object holds a reference to the other.

## 44. Why can't reference counting alone detect circular references?

Because objects inside a circular reference continue referencing each other.

Example:

```
a = []
b = []

a.append(b)
b.append(a)

del a
del b
```

Even after deleting the external variables:

- Object A still has a reference from B.
- Object B still has a reference from A.
- Both reference counts remain greater than zero.

Reference counting sees those references and doesn't consider the objects deallocatable.

However, there are no external references to either object.

This is why Python needs cyclic garbage collection.

## 45. How does Python identify circular references?

Python's cyclic garbage collector uses a graph-based approach.

It examines tracked objects and their references to determine whether objects are reachable from outside a reference cycle.

Conceptually:

1. Identify candidate objects.
2. Examine references between them.
3. Account for internal references.
4. Identify objects that have no external reachability.
5. Collect unreachable cycles.

The implementation uses algorithms based on trial deletion.

## 46. How does Python collect unreachable circular references?

Python's cyclic garbage collector:

1. Finds candidate objects involved in reference cycles.
2. Calculates their internal reference relationships.
3. Identifies objects that have no external references.
4. Determines which objects are unreachable.
5. Clears references and reclaims their memory.

Example:

```
import gc

a = []
b = []

a.append(b)
b.append(a)

del a
del b

collected = gc.collect()

print(collected)
```

`gc.collect()` triggers garbage collection and returns the number of collected objects (with some implementation-specific accounting details).

## 47. What is trial deletion?

Trial deletion is an algorithmic technique used by Python's cyclic garbage collector to identify unreachable reference cycles.

The basic idea:

1. Temporarily calculate how many references come from within the candidate objects.
2. Subtract internal references from the reference counts.
3. Remaining references indicate references coming from outside the candidate group.
4. Objects with no external references may be garbage.
5. Identify and collect unreachable objects.

Example:

Imagine:

- A references B.
- B references A.
- Neither has an external reference.

| Object | Total references | Internal references | Remaining |
| ------ | ---------------- | ------------------- | --------- |
| A      | 1                | 1                   | 0         |
| B      | 1                | 1                   | 0         |

Both have zero remaining external references, so they may be unreachable.

Interview point: Trial deletion helps distinguish objects kept alive only by references within a cycle from objects that have external references.

## 48. Are all circular references considered garbage?

No.

A circular reference is not automatically garbage.

It becomes garbage only when the objects in the cycle are unreachable from the program's live references.

Example:

```
a = []
b = []

a.append(b)
b.append(a)

print(a)
```

The circular reference is still reachable through `a`.

Therefore, Python must not collect it.

## 49. Can circular references be collected if they are still reachable?

No.

If objects are reachable through active references, Python considers them live objects.

Example:

```
a = []
b = []

a.append(b)
b.append(a)

del b

print(a)
```

Even though `b` is deleted, `a` still references the list previously assigned to `b`.

The cycle is still reachable through `a`.

Therefore, it must not be collected.

## 50. What is the `gc` module?

The `gc` module is a built-in Python module that provides an interface to the cyclic garbage collector.

It allows developers to:

- Manually trigger garbage collection.
- Enable or disable cyclic garbage collection.
- Check GC status.
- Retrieve garbage collection statistics.
- Configure GC thresholds.
- Inspect tracked objects.

Example:

```
import gc

print(gc.isenabled())
```

## 51. What is the purpose of `gc.collect()`?

`gc.collect()` manually triggers garbage collection.

Example:

```
import gc

collected = gc.collect()

print("Collected objects:", collected)
```

It attempts to collect unreachable cyclic objects.

Important: Python already performs automatic garbage collection. You generally don't need to call `gc.collect()` manually.

## 52. What does `gc.isenabled()` do?

It checks whether automatic cyclic garbage collection is enabled.

```
import gc

print(gc.isenabled())
```

Possible output:

```
True
```

- `True`: Automatic cyclic garbage collection is enabled.
- `False`: Automatic cyclic garbage collection is disabled.

## 53. What happens when you call `gc.disable()`?

It disables automatic cyclic garbage collection.

```
import gc

gc.disable()

print(gc.isenabled())
```

Output:

```
False
```

Python will no longer automatically perform cyclic garbage collection until it is enabled again.

You can enable it using:

```
gc.enable()
```

## 54. Does disabling garbage collection disable reference counting?

No. This is an important interview question.

Disabling garbage collection only disables automatic cyclic garbage collection.

Reference counting continues working.

Example:

```
import gc

gc.disable()

class Employee:
    pass

emp = Employee()

del emp
```

The Employee object can still be deallocated when its reference count reaches zero.

However, unreachable circular references may remain in memory until cyclic collection runs.

## 55. How do you manually trigger garbage collection?

Use `gc.collect()`.

```
import gc

gc.collect()
```

You can also specify a generation:

```
gc.collect(0)  # Collect generation 0
gc.collect(1)  # Collect generation 1
gc.collect(2)  # Full collection
```

## 56. How do you check garbage collection statistics?

Use:

```
import gc

print(gc.get_stats())
```

It returns a list of dictionaries containing collection statistics for each generation.

## 57. What does `gc.get_count()` return?

It returns the current collection counters for the garbage collector.

```
import gc

print(gc.get_count())
```

Example output:

```
(150, 5, 2)
```

These values represent generation-related allocation/deallocation tracking counters.

They are not the number of objects in each generation.

## 58. What does `gc.get_threshold()` return?

It returns the configured garbage collection thresholds.

```
import gc

print(gc.get_threshold())
```

For example, in CPython versions with the traditional three-generation configuration, you might see:

```
(700, 10, 10)
```

These thresholds influence when automatic garbage collection runs.

The exact defaults depend on the Python version and implementation.

## 59. What does `gc.get_stats()` return?

It returns a list of dictionaries containing statistics for each garbage collection generation.

```
import gc

for stats in gc.get_stats():
    print(stats)
```

Typical dictionary fields include:

| Field         | Meaning                         |
| ------------- | ------------------------------- |
| collections   | Number of collections           |
| collected     | Number of objects collected     |
| uncollectable | Number of uncollectable objects |

Exact output and number of generations depend on Python version.

## 60. What are generations in garbage collection?

Generations are groups used by Python's cyclic garbage collector to organize tracked objects according to their age.

In traditional CPython generational GC, there are three generations:

- Generation 0 – Young objects.
- Generation 1 – Intermediate-aged objects.
- Generation 2 – Old objects.

## Generational garbage collection

Generation 0 – Young

Recently allocated tracked objects

Generation 1 – Intermediate

Objects that survive younger-generation collections

Generation 2 – Old

Objects that survive multiple collections

Conceptual traditional three-generation model.

Version note: Python 3.14 changed CPython's generational GC design. It now has two generations (young and old), rather than the traditional three. The following traditional interview questions are often taught using the older model.

## 61. Why does Python use generational garbage collection?

Because most objects have short lifetimes.

For example:

```
def calculate():
    result = [1, 2, 3, 4, 5]
    return sum(result)
```

The temporary list becomes unnecessary after the function finishes.

If Python examined every tracked object every time it performed cyclic garbage collection, it could waste processing time.

Generational GC optimizes this by:

- Frequently checking younger objects.
- Less frequently checking older objects.
- Reducing unnecessary collection work.

## 62. What is the generational hypothesis?

The generational hypothesis states:

Most objects die young.

In other words:

- Many objects are created temporarily.
- Most become unnecessary quickly.
- Only a small percentage survive for a long time.

Python uses this assumption to optimize garbage collection.

## 63. What are young and old generations?

Young generation:

- Contains recently allocated tracked objects.
- Checked frequently.
- Many temporary objects are collected here.

Old generation:

- Contains objects that survived previous collections.
- Checked less frequently.
- Generally contains longer-lived objects.

In traditional CPython, there was also an intermediate generation.

## 64. How does Python decide when to perform garbage collection?

In traditional CPython, automatic collection depends on GC allocation counters and configured thresholds.

Example:

```
import gc

print(gc.get_count())
print(gc.get_threshold())
```

When the relevant counters cross configured thresholds, Python may trigger a collection.

You can configure thresholds using:

```
gc.set_threshold(1000, 15, 15)
```

The precise behavior is version-dependent. In Python 3.14, the collection strategy and threshold interpretation changed.

## 65. Does Python immediately collect every unreachable object?

No.

There are two important cases:

1\. Reference counting

When an object's reference count reaches zero, CPython generally deallocates it immediately.

2\. Cyclic garbage collection

Unreachable circular references may remain in memory until the cyclic garbage collector runs.

Example:

```
import gc

a = []
b = []

a.append(b)
b.append(a)

del a
del b

# The cycle may still occupy memory here.

gc.collect()

# Explicitly request cyclic collection.
```

# Important interview revision

These are the concepts I recommend being particularly comfortable explaining.

| Concept                 | Key point                      |
| ----------------------- | ------------------------------ |
| Reference counting      | Counts object references       |
| Circular reference      | Objects reference each other   |
| Cyclic GC               | Collects unreachable cycles    |
| Trial deletion          | Identifies external references |
| `gc.collect()`          | Manually triggers collection   |
| `gc.disable()`          | Disables automatic cyclic GC   |
| `gc.isenabled()`        | Checks GC status               |
| `gc.get_count()`        | Returns GC counters            |
| `gc.get_threshold()`    | Returns GC thresholds          |
| Generational GC         | Groups objects by age          |
| Generational hypothesis | Most objects die young         |

# Test your understanding

Let's check whether you can explain these concepts in an interview. I'll ask one question at a time, and after your answer I'll explain what is correct, what is missing, and how to improve your interview response.

Knowledge check

Question 1 of 5

What happens when you call gc.disable()?

It disables reference counting and cyclic GC

It disables automatic cyclic GC, but reference counting continues

It immediately deletes all unreachable objects

It prevents Python from allocating new objects

Previous

Check answer

0 of 5 answered

My recommendation: After this topic, study Python memory management internals, shallow copy vs deep copy, stack vs heap, and `__del__()` because interviewers often connect these topics.