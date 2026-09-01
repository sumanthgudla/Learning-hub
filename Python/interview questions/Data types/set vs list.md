### Q: What is the difference between a Set and a List in Python?

> **Interview answer:**
> The main difference is that a **list is ordered and allows duplicates**, while a **set is an unordered collection of unique elements**.
>
> For example:
>
> ```python
> numbers = [1, 2, 2, 3, 4]
> print(numbers)
> # [1, 2, 2, 3, 4]
>
> numbers = {1, 2, 2, 3, 4}
> print(numbers)
> # {1, 2, 3, 4}
> ```
>
> I would use a **list** when I need to maintain order, allow duplicates, or access elements using an index.
>
> I would use a **set** when I mainly care about **uniqueness** and fast membership checking.
>
> For example, if I want to check whether an employee ID exists:
>
> ```python
> employee_ids = {101, 102, 103, 104}
>
> if 103 in employee_ids:
>     print("Employee exists")
> ```
>
> Set membership is typically **O(1) average case**, whereas searching for an element in a list is **O(n)**.
>
> So, in short: **list for ordered collections and sets for uniqueness and fast membership checks.**

### Quick comparison

| Feature         | List         | Set                              |
| --------------- | ------------ | -------------------------------- |
| Ordered         | ✅ Yes        | ❌ Not indexed/ordered for access |
| Duplicates      | ✅ Allowed    | ❌ Not allowed                    |
| Indexing        | ✅ `list[0]`  | ❌                                |
| Mutable         | ✅            | ✅                                |
| Membership `in` | O(n)         | O(1) average                     |
| Main use        | Ordered data | Unique data / fast lookup        |

**Likely follow-up:** *“Can a set contain a list?”*

> No. Set elements must be **hashable**, and lists are mutable and therefore unhashable. A tuple can be a set element if all its contents are hashable.
