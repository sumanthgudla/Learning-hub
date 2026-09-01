Here’s a **quick interview-ready summary of everything we covered about HashMap / Python `dict`**.

## 1. What is a HashMap?

A HashMap stores **key-value pairs** using a hash table.

```python
d = {
    "Alice": 100,
    "Bob": 200
}
```

Conceptually:

```text
Key → Hash → Table position → Value
```

---

## 2. How does lookup work?

For:

```python
d["Alice"]
```

Python roughly does:

```text
"Alice"
   ↓
hash("Alice")
   ↓
calculate table position
   ↓
check candidate slot
   ↓
compare key
   ↓
return 100
```

It **doesn't scan every element**.

That's why dictionary lookup is **O(1) on average**.

---

## 3. Why doesn't storing data in a table make lookup O(n)?

Because Python doesn't search the entire table.

For example:

```text
1,000,000 entries

[ ][ ][ ][ ][ ][ ][ ][ ][ ] ... [ ]
                  ↑
            calculated position
```

The hash helps Python jump directly to the relevant area.

So:

```text
Scanning everything → O(n)
Hash-based lookup  → O(1) average
```

---

## 4. What is a collision?

A collision occurs when **different keys map to the same table position**.

For example:

```text
hash("Alice") → slot 5
hash("Bob")   → slot 5
```

Both want slot 5.

---

## 5. How does Python handle collisions?

Python's dictionary uses **open addressing**.

If the calculated slot is occupied:

```text
hash("Alice")
      ↓
   slot 5
      ↓
   occupied
      ↓
find another slot
      ↓
   slot 7
      ↓
   store Alice
```

So Alice may not physically be stored in her initial hash-derived slot.

---

## 6. How does `get` find a key that was moved to another slot?

This is the important part.

Python uses the **same probing sequence during lookup** that it used during insertion.

Suppose:

```text
Alice → initial slot 5 → occupied → slot 7 → stored
```

Later:

```python
d["Alice"]
```

Python does:

```text
hash("Alice")
      ↓
   slot 5
      ↓
occupied / not Alice
      ↓
continue same probe sequence
      ↓
   slot 7
      ↓
Alice found
      ↓
return value
```

It doesn't randomly search.

---

## 7. Why does Python check equality as well as the hash?

Because **hash values aren't guaranteed to uniquely identify objects**.

Conceptually:

```text
hash(key)
   ↓
find candidate position
   ↓
compare actual key using equality
   ↓
correct key?
   ↓
return value
```

So hashing finds the **candidate**, while equality confirms the **actual key**.

---

## 8. `__hash__()` and `__eq__()`

Python objects used as dictionary keys need appropriate hashing/equality behavior.

Important rule:

> If two objects are equal, they must have the same hash.

```python
a == b
```

should imply:

```python
hash(a) == hash(b)
```

The reverse isn't necessarily true.

Two objects can have the same hash but still not be equal.

---

## 9. Why can't a list be a dictionary key?

Because dictionary keys must be **hashable**.

A list is mutable:

```python
my_list = [1, 2, 3]
```

So:

```python
d[my_list] = "value"
```

gives a `TypeError`.

A tuple can be used if its contents are hashable:

```python
d[(1, 2)] = "value"
```

---

## 10. What happens when the dictionary gets full?

The hash table can **resize**.

Conceptually:

```text
Small table

[ ][A][ ][B][ ][C]

       ↓ resize

Larger table

[ ][ ][A][ ][ ][B][ ][ ][C][ ]
```

Because the table size changes, entries may need to be redistributed.

An individual resize can be expensive, but resizing happens occasionally.

Therefore dictionary insertion is generally considered:

```text
Average / amortized → O(1)
```

---

## 11. Complexity

| Operation         |            Average |
| ----------------- | -----------------: |
| Lookup            |           **O(1)** |
| Insert            | **O(1)** amortized |
| Delete            |   **O(1)** average |
| Search all values |           **O(n)** |

Worst-case lookup can degrade toward **O(n)** in pathological collision situations.

---

# ⭐ Best interview answer

If EPAM asks:

**"Explain how Python dictionary works internally."**

Say:

> "Python's dictionary is implemented using a hash table. When we insert a key-value pair, Python calculates the hash of the key and uses it to determine a candidate position in the internal table. During lookup, it calculates the hash again and follows the same probing sequence to locate the key. If there is a collision, Python uses open addressing to find another suitable slot. It also checks key equality to make sure the candidate is actually the requested key. Because hashing lets us go directly to the relevant area rather than scanning all entries, dictionary lookup is O(1) on average. The table can also resize as it grows to maintain efficient operations."

### The mental model to remember

```text
             DICTIONARY

                 Key
                  ↓
             hash(key)
                  ↓
          initial table slot
                  ↓
           ┌──── occupied? ────┐
           │                   │
          No                  Yes
           ↓                   ↓
         Store          probe another slot
                               ↓
                         find candidate
                               ↓
                         key equality?
                               ↓
                         return value
```

If you understand **this flow**, you can answer most HashMap/dictionary internal questions in a Python interview.
