Topic 5: Lambda, map, filter
What is it?
Lambda is a way to write a small anonymous function in one line. map() applies a function to every item in an iterable. filter() keeps only items where a function returns True. Together these are the foundation of functional programming in Python — a style senior devs must know deeply.
1. Lambda — Anonymous Function
# Regular function
def square(x):
    return x ** 2

# Same thing as lambda
square = lambda x: x ** 2

# Both work identically
print(square(5))    # 25


# Lambda syntax
lambda arguments : expression
#  ↑                  ↑
# input(s)         single expression (auto returned)


# Multiple arguments
add  = lambda x, y: x + y
print(add(3, 4))        # 7

# With condition (ternary)
grade = lambda score: "pass" if score >= 50 else "fail"
print(grade(75))        # pass
print(grade(30))        # fail

# No arguments
greet = lambda: "Hello World"
print(greet())          # Hello World
2. Lambda vs Regular Function
# Lambda — use for simple one-line logic
square = lambda x: x ** 2

# Regular function — use for complex logic
def square(x):
    return x ** 2

# These are identical BUT:
# lambda — no name in traceback, harder to debug
# def    — has a name, easier to debug, can have docstring

# Senior rule:
# lambda → only as argument to another function (map, filter, sorted)
# def    → anything you'll reuse or that has complex logic
3. map() — Apply Function to Every Item
# map(function, iterable)
# applies function to EVERY item
# returns a MAP OBJECT — must convert to list

numbers = [1, 2, 3, 4, 5]

# Without map — using loop
result = []
for n in numbers:
    result.append(n ** 2)

# With map — cleaner
result = list(map(lambda x: x ** 2, numbers))
print(result)   # [1, 4, 9, 16, 25]


# map with regular function
def double(x):
    return x * 2

result = list(map(double, numbers))
print(result)   # [2, 4, 6, 8, 10]


# map with strings
names = ["arjun", "priya", "ravi"]
result = list(map(str.upper, names))
print(result)   # ['ARJUN', 'PRIYA', 'RAVI']
#                            ↑
#               str.upper is a function — no () needed


# map with multiple iterables
a = [1, 2, 3]
b = [4, 5, 6]
result = list(map(lambda x, y: x + y, a, b))
print(result)   # [5, 7, 9]  ← adds corresponding elements


# map is LAZY — doesn't compute until consumed
m = map(lambda x: x**2, range(1000000))
# nothing computed yet — just a recipe
print(next(m))   # 0  ← computes one at a time
4. filter() — Keep Items That Pass a Test
# filter(function, iterable)
# keeps items where function returns TRUE
# returns a FILTER OBJECT — must convert to list

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Keep only even numbers
result = list(filter(lambda x: x % 2 == 0, numbers))
print(result)   # [2, 4, 6, 8, 10]

# Keep only odd numbers
result = list(filter(lambda x: x % 2 != 0, numbers))
print(result)   # [1, 3, 5, 7, 9]

# Filter strings
names = ["Arjun", "", "Priya", None, "Ravi", ""]
# Remove empty/None values
result = list(filter(None, names))
#                     ↑
#              None as function → keeps only TRUTHY values
print(result)   # ['Arjun', 'Priya', 'Ravi']

# Filter with regular function
def is_adult(age):
    return age >= 18

ages = [15, 22, 17, 25, 13, 30]
result = list(filter(is_adult, ages))
print(result)   # [22, 25, 30]
5. Combining map + filter
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Filter evens THEN square them
result = list(map(
    lambda x: x ** 2,
    filter(lambda x: x % 2 == 0, numbers)
))
print(result)   # [4, 16, 36, 64, 100]

# Read inside out:
# filter(lambda x: x%2==0, numbers) → [2,4,6,8,10]
# map(lambda x: x**2, [2,4,6,8,10]) → [4,16,36,64,100]


# Same thing with list comprehension — more readable
result = [x**2 for x in numbers if x % 2 == 0]
print(result)   # [4, 16, 36, 64, 100]
6. Lambda With sorted() — Most Common Interview Use
students = [
    {"name": "Arjun",  "score": 85, "age": 22},
    {"name": "Priya",  "score": 92, "age": 20},
    {"name": "Ravi",   "score": 85, "age": 25},
    {"name": "Sneha",  "score": 78, "age": 21},
]

# Sort by score
sorted(students, key=lambda s: s["score"])

# Sort by score DESC
sorted(students, key=lambda s: -s["score"])

# Sort by score DESC, then name alphabetically for ties
sorted(students, key=lambda s: (-s["score"], s["name"]))
# Arjun and Ravi both have 85 → Arjun comes first

# Sort by multiple fields
sorted(students, key=lambda s: (s["score"], s["age"]))
7. map vs filter vs List Comprehension
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Transform every item
list(map(lambda x: x*2, numbers))      # map
[x*2 for x in numbers]                 # comprehension ← more Pythonic

# Filter items
list(filter(lambda x: x>5, numbers))   # filter
[x for x in numbers if x > 5]          # comprehension ← more Pythonic

# Filter + Transform
list(map(lambda x: x*2,
    filter(lambda x: x>5, numbers)))   # map + filter — hard to read
[x*2 for x in numbers if x > 5]        # comprehension ← clearly better
Interview Questions They Actually Ask
Q1: What does map() return in Python 3?
A lazy map object — not a list. It computes values on demand. You must wrap with list() to get all values at once, or iterate over it directly.
Q2: When would you use map/filter over list comprehension?
When passing an existing named function — map(str.upper, names) is cleaner than [n.upper() for n in names]. Also when working in a functional pipeline where you chain operations. For most other cases, list comprehensions are more Pythonic.
Q3: What does filter(None, iterable) do?
Passing None as the function tells filter to use the truthiness of each item. It removes all falsy values — None, "", 0, [], False.
Q4: Can lambda have multiple lines?
No — lambda is limited to a single expression. If you need multiple lines or statements, use a regular def function.
Q5: What's the difference between map and list comprehension performance?
For simple operations with existing functions (str.upper, int, abs), map is slightly faster because it avoids the overhead of the comprehension loop. For lambda expressions, list comprehensions are usually faster because lambda has call overhead.
Practice Problems
Beginner — p2_t05_prac01_basic_map_filter.py Given a list of numbers, use map to square all numbers and filter to keep only those greater than 20. Print both results.
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# map result:    [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
# filter result: [25, 36, 49, 64, 81, 100]
Senior level — p2_t05_prac02_student_pipeline.py Given the students list below, use filter, map, sorted, and lambda to:
Filter students with score ≥ 60
Add a grade key to each using map
Sort by grade then name alphabetically
Print final result — no list comprehensions allowed
students = [
    {"name": "Arjun",  "score": 85},
    {"name": "Priya",  "score": 42},
    {"name": "Ravi",   "score": 91},
    {"name": "Sneha",  "score": 38},
    {"name": "Kiran",  "score": 76},
    {"name": "Divya",  "score": 55},
    {"name": "Raj",    "score": 95},
]
# Grade: 90+=A, 80-89=B, 70-79=C, 60-69=D
Common Mistakes & Senior Traps
Forgetting list() — map() and filter() return lazy objects, not lists. print(map(...)) prints <map object at 0x...> not the values.
Lambda with statements — lambda x: x=x+1 is a SyntaxError. Lambda only takes expressions, not statements like assignment.
map with None — map(None, [1,2,3]) raises TypeError in Python 3. Use filter(None, ...) for truthiness filtering.
Exhausted map/filter object — like generators, once consumed they're empty. Convert to list if you need to use the result more than once.
Overusing lambda — PEP8 says never assign lambda to a variable. Use def instead. Lambda belongs as an inline argument only.
# PEP8 violation — don't do this
square = lambda x: x**2    # ❌ assign lambda to variable

# Do this instead
def square(x):             # ✅ proper function
    return x**2
Say next for Topic 6: Scope & Closures!