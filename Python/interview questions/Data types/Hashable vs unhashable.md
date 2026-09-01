### Hashable vs Unhashable in Python

This is important because **dictionary keys and set elements must be hashable**.

### 1. What is hashable?

An object is **hashable** if Python can calculate a hash value for it that remains stable during its lifetime.

```python
hash("hello")
hash(10)
hash((1, 2, 3))
```

These work.

Common hashable types:

* `int`
* `float`
* `str`
* `bool`
* `tuple` **if all its elements are hashable**
* `frozenset`
* `None`

---

### 2. What is unhashable?

An object is **unhashable** when it cannot be used as a dictionary key or set element.

Common examples:

* `list`
* `dict`
* `set`

For example:

```python
my_list = [1, 2, 3]

hash(my_list)
```

You get:

```text
TypeError: unhashable type: 'list'
```

---

### Why are lists unhashable?

The main reason is that lists are **mutable**.

```python
my_list = [1, 2, 3]

my_list.append(4)
```

The contents can change.

Imagine using a list as a dictionary key:

```python
data = {
    [1, 2, 3]: "hello"
}
```

Python needs a stable hash to find that key later.

But if the list could change from:

```text
[1, 2, 3]
```

to:

```text
[1, 2, 3, 4]
```

its hash would need to change, which would break the dictionary's ability to locate the key.

Therefore, mutable objects like lists are unhashable.

---

### Why is a tuple hashable?

A tuple itself is immutable:

```python
t = (1, 2, 3)

print(hash(t))
```

Works.

So you can do:

```python
data = {
    (1, 2): "point"
}
```

But there's an important exception:

```python
t = ([1, 2], 3)

hash(t)
```

❌ This fails because the tuple contains a **list**, which is unhashable.

So the rule is:

> **A tuple is hashable only when all of its elements are hashable.**

---

### Connection to dictionaries and sets

This is why:

```python
my_dict = {
    "name": "Sumanth",
    10: "age"
}
```

works.

But:

```python
my_dict = {
    [1, 2]: "value"
}
```

❌ doesn't work.

Similarly:

```python
my_set = {1, 2, 3}
```

works.

But:

```python
my_set = {[1, 2]}
```

❌ doesn't work.

---

### ⭐ Interview answer

> **Hashable objects have a stable hash value and can be used as dictionary keys or set elements. Immutable types like strings, integers, and tuples containing only hashable elements are generally hashable. Mutable types like lists, dictionaries, and sets are unhashable because their contents can change.**

### Quick memory trick

**Immutable → generally hashable**
**Mutable → generally unhashable**

But remember the **tuple exception**: a tuple is hashable only if everything inside it is hashable.
