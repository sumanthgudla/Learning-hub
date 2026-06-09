What is it?
Dict comprehensions build a dictionary in a single line — just like list comprehensions but with key-value pairs instead of single values. They're faster than manually calling dict[key] = value in a loop because Python pre-allocates the dictionary internally. Senior devs use these constantly for transforming, inverting, and filtering dictionaries cleanly.
Syntax Pattern
{key_expr : value_expr  for  item  in  iterable  if  condition}
#    ↑            ↑                                      ↑
#  the key     the value                          optional filter
Code Example — All Levels
# 1. Basic — number to its square
squares = {x: x**2 for x in range(1, 6)}
print(squares)
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}


# 2. From a list — word to its length
words = ["python", "senior", "developer"]
lengths = {word: len(word) for word in words}
print(lengths)
# {'python': 6, 'senior': 6, 'developer': 9}


# 3. With condition — filter out short words
long_words = {word: len(word) for word in words if len(word) > 6}
print(long_words)
# {'developer': 9}


# 4. Invert a dictionary — swap keys and values
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)
# {1: 'a', 2: 'b', 3: 'c'}


# 5. Transform values — uppercase all values
config = {"host": "localhost", "db": "postgres", "user": "admin"}
upper_config = {k: v.upper() for k, v in config.items()}
print(upper_config)
# {'host': 'LOCALHOST', 'db': 'POSTGRES', 'user': 'ADMIN'}


# 6. From two lists using zip()
keys   = ["name", "age", "city"]
values = ["Arjun", 22, "Vijayawada"]
person = {k: v for k, v in zip(keys, values)}
print(person)
# {'name': 'Arjun', 'age': 22, 'city': 'Vijayawada'}


# 7. Nested dict comprehension — multiplication table
table = {x: {y: x * y for y in range(1, 4)} for x in range(1, 4)}
print(table)
# {1: {1:1, 2:2, 3:3}, 2: {1:2, 2:4, 3:6}, 3: {1:3, 2:6, 3:9}}


# 8. Filtering a dict — keep only passing scores
scores = {"Arjun": 85, "Priya": 42, "Ravi": 91, "Sneha": 38}
passed = {name: score for name, score in scores.items() if score >= 50}
print(passed)
# {'Arjun': 85, 'Ravi': 91}
Dict Comprehension vs Regular Loop
# Regular loop — verbose
result = {}
for k, v in scores.items():
    if v >= 50:
        result[k] = v

# Dict comprehension — clean, faster
result = {k: v for k, v in scores.items() if v >= 50}
Key Methods You Must Know With Dict Comprehensions
d = {"a": 1, "b": 2, "c": 3}

d.items()   # → [('a',1), ('b',2), ('c',3)]  — loop key+value
d.keys()    # → ['a', 'b', 'c']              — loop keys only
d.values()  # → [1, 2, 3]                    — loop values only

# These are view objects — they reflect live changes to the dict
Interview Questions They Actually Ask
Q1: What happens if there are duplicate keys in a dict comprehension?
data = [("a", 1), ("b", 2), ("a", 3)]
result = {k: v for k, v in data}
print(result)   # {'a': 3, 'b': 2}
The last value wins — later keys silently overwrite earlier ones. This is a classic interview trap. Always validate for duplicate keys when inverting or building from raw data.
Q2: How do you safely invert a dict when values might not be unique?
# Unsafe — duplicates cause silent data loss
original = {"a": 1, "b": 1, "c": 2}
inverted = {v: k for k, v in original.items()}
print(inverted)   # {1: 'b', 2: 'c'}  — 'a' is lost!

# Safe — group keys by value
from collections import defaultdict
safe = defaultdict(list)
for k, v in original.items():
    safe[v].append(k)
print(dict(safe))   # {1: ['a', 'b'], 2: ['c']}
Q3: What's the difference between dict.items() and dict.keys()?
.items() returns key-value tuples — use when you need both. .keys() returns only keys. Both return view objects, not lists — they are memory-efficient and reflect real-time changes to the dict.
Q4: Can dict comprehensions replace dict(zip(keys, values))?
keys   = ["a", "b", "c"]
values = [1, 2, 3]

# These are equivalent:
d1 = dict(zip(keys, values))
d2 = {k: v for k, v in zip(keys, values)}

# dict(zip()) is faster and more readable for simple cases
# dict comprehension wins when you need to transform or filter
Practice Problems
Beginner — p2_t02_basic_dict_comp.py Given a list of words, create a dictionary where each word is the key and the number of vowels in that word is the value.
words = ["python", "developer", "interview", "comprehension"]
# expected: {'python': 1, 'developer': 4, 'interview': 4, 'comprehension': 5}
Senior level — p2_t02_advanced_dict_comp.py Given the list of students below, build a dictionary of only passing students (score ≥ 50), where the key is the name and the value is their letter grade. Do it in one dict comprehension.
students = [
    {"name": "Arjun",  "score": 85},
    {"name": "Priya",  "score": 42},
    {"name": "Ravi",   "score": 91},
    {"name": "Sneha",  "score": 38},
    {"name": "Kiran",  "score": 76},
    {"name": "Divya",  "score": 55},
]
# Grade logic: 90+ = 'A', 80-89 = 'B', 70-79 = 'C', 50-69 = 'D'
# expected: {'Arjun': 'B', 'Ravi': 'A', 'Kiran': 'C', 'Divya': 'D'}
Common Mistakes & Senior Traps
Silent key overwrite — duplicate keys don't raise errors, last value silently wins. Always be aware when source data might have duplicates.
Inverting non-unique values — swapping keys and values when values aren't unique causes data loss. Use defaultdict(list) for safe inversion.
Mutating the dict while iterating — never modify a dict inside a comprehension that's iterating over it. It raises RuntimeError: dictionary changed size during iteration.
Using a list where a dict is better — if you find yourself doing list.index() to look things up, you probably want a dict instead. O(1) lookup vs O(n).
Forgetting .items() — looping for k in d gives only keys. You need for k, v in d.items() to get both.
Say next for Topic 3: Strings in Depth!