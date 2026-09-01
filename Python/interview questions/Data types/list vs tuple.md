### Q: What is the difference between a List and a Tuple in Python?

> **Interview answer:**
> The main difference is that a **list is mutable**, whereas a **tuple is immutable**.
>
> A list is used when I need a collection whose elements may change during execution. A tuple is useful when the data should remain fixed.
>
> For example:
>
> ```python
> numbers = [1, 2, 3]
> numbers.append(4)       # Valid
>
> coordinates = (10, 20)
> # coordinates[0] = 15   # TypeError
> ```
>
> Because tuples are immutable, they can also be used as **dictionary keys** or elements of a set, provided all their elements are hashable.
>
> In terms of performance, tuples generally have **less memory overhead** and can be slightly faster to iterate over than lists.
>
> So, my rule of thumb is: **use a list for a collection that can change, and a tuple for fixed or read-only data.**

### Quick comparison

| Feature               | List             | Tuple           |
| --------------------- | ---------------- | --------------- |
| Mutable               | ✅ Yes            | ❌ No            |
| Syntax                | `[1, 2, 3]`      | `(1, 2, 3)`     |
| Can append/remove     | ✅                | ❌               |
| Can be dictionary key | ❌                | ✅*              |
| Memory                | Generally higher | Generally lower |
| Best for              | Dynamic data     | Fixed data      |

* A tuple is hashable only when all of its elements are hashable.

**Likely follow-up:** *“Why would you choose a tuple over a list in a real project?”*


