
## `zip()` in Python

`zip()` is used to **combine elements from two or more iterables based on their positions**.

### Basic example

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 28]

result = zip(names, ages)

print(list(result))
```

Output:

```text
[('Alice', 25), ('Bob', 30), ('Charlie', 28)]
```

It pairs:

```text
Alice   → 25
Bob     → 30
Charlie → 28
```

### Very common interview use

Create a dictionary from two lists:

```python
names = ["Alice", "Bob", "Charlie"]
salaries = [50000, 70000, 60000]

employees = dict(zip(names, salaries))

print(employees)
```

Output:

```python
{
    "Alice": 50000,
    "Bob": 70000,
    "Charlie": 60000
}
```

### What if lengths are different?

`zip()` stops when the **shortest iterable is exhausted**.

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30]

print(list(zip(names, ages)))
```

Output:

```text
[('Alice', 25), ('Bob', 30)]
```

`Charlie` is ignored.

### Can `zip()` handle more than 2?

Yes.

```python
names = ["Alice", "Bob"]
ages = [25, 30]
cities = ["Hyderabad", "Vizag"]

print(list(zip(names, ages, cities)))
```

Output:

```text
[
    ("Alice", 25, "Hyderabad"),
    ("Bob", 30, "Vizag")
]
```

### `zip()` returns an iterator

In Python 3:

```python
result = zip(names, ages)

print(result)
```

You need:

```python
list(result)
```

if you want to see/store all pairs as a list.

### Important interview question: Can we unzip?

Yes, using `*`.

```python
data = [("Alice", 25), ("Bob", 30)]

names, ages = zip(*data)

print(names)
print(ages)
```

Output:

```text
('Alice', 'Bob')
(25, 30)
```

### Interview answer

> **`zip()` combines multiple iterables element-by-element based on their position and returns an iterator of tuples. By default, it stops when the shortest iterable is exhausted.**

**Easy memory trick:**

```text
zip([1,2,3], ["a","b","c"])

↓

[(1,"a"), (2,"b"), (3,"c")]
```

Think of it as **zipping two rows together column-by-column**.



If you **don't convert `zip()` into a list or dict**, Python gives you a **zip object**, which is an iterator.

```python
names = ["Alice", "Bob", "Charlie"]
ages = [25, 30, 28]

result = zip(names, ages)

print(result)
```

Output will look something like:

```text
<zip object at 0x10AB1234>
```

It **doesn't directly display the actual pairs**.

### But you can iterate over it

```python
for item in result:
    print(item)
```

Output:

```text
('Alice', 25)
('Bob', 30)
('Charlie', 28)
```

### Why?

`zip()` returns a **lazy iterator**. It generates the pairs when you ask for them rather than creating the entire list immediately.

```python
result = zip(names, ages)

print(type(result))
```

Output:

```text
<class 'zip'>
```

### Important interview point ⚠️

Because it's an iterator, once you consume it:

```python
result = zip(names, ages)

print(list(result))
print(list(result))
```

Output:

```text
[('Alice', 25), ('Bob', 30), ('Charlie', 28)]
[]
```

The second time it's empty because the iterator has already been consumed.

**So:**

```text
zip()              → zip object / iterator
list(zip(...))     → list of tuples
dict(zip(...))     → dictionary
```

You don't *have* to convert it. You convert it when you specifically need a list/dictionary or want to reuse the resulting collection.
