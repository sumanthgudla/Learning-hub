### Q: What is a Dictionary in Python?

> **Interview answer:**
> A dictionary is a **mutable collection of key-value pairs** in Python. It is mainly used when I want to store and retrieve data using a **key** rather than an index.
>
> For example:
>
> ```python
> employee = {
>     "name": "John",
>     "age": 30,
>     "salary": 80000
> }
>
> print(employee["name"])
> # John
> ```
>
> Internally, Python dictionaries are implemented using a **hash table**. The key is hashed, and that hash is used to efficiently locate the corresponding value.
>
> Therefore, operations like **lookup, insertion, and deletion are O(1) on average**.
>
> Dictionary keys must be **hashable**, so immutable types like strings, integers, and tuples can be keys, while lists and dictionaries cannot.
>
> Dictionaries are useful when I need to represent structured data, perform fast lookups, count frequencies, or map one value to another.

### Example — frequency counting

```python
numbers = [1, 2, 2, 3, 3, 3]

frequency = {}

for num in numbers:
    frequency[num] = frequency.get(num, 0) + 1

print(frequency)
# {1: 1, 2: 2, 3: 3}
```

### Important points to remember

* **Key-value pairs:** `{"name": "John"}`
* **Keys are unique**
* **Mutable**
* **Keys must be hashable**
* Lookup/insertion/deletion → **O(1) average**
* Python dictionaries preserve **insertion order** (guaranteed since Python 3.7)

**Likely follow-up:** *“Why can't a list be a dictionary key?”*

> Because a list is mutable and therefore **unhashable**. Dictionary keys need a stable hash value, so mutable objects like lists cannot be used as keys.
