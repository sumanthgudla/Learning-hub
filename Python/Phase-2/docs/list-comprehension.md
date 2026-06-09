
List Comprehensions
What is it?
A list comprehension is a concise, single-line way to build a list. Internally Python optimizes it — it runs faster than an equivalent for loop because it avoids repeated append() calls. Senior devs are expected to know not just the syntax but when to use it and when not to.
Syntax Pattern
[expression  for  item  in  iterable  if  condition]
#     ↑               ↑                      ↑
#  what to keep    loop var            optional filter
Code Example — All Levels
# 1. Basic — square numbers
squares = [x**2 for x in range(1, 6)]
print(squares)            # [1, 4, 9, 16, 25]

# 2. With condition — even numbers only
evens = [x for x in range(10) if x % 2 == 0]
print(evens)              # [0, 2, 4, 6, 8]

# 3. Transform strings
names = ["alice", "bob", "charlie"]
upper = [name.upper() for name in names]
print(upper)              # ['ALICE', 'BOB', 'CHARLIE']

# 4. Filter + transform together
scores = [45, 82, 90, 33, 76]
passed = [s for s in scores if s >= 50]
print(passed)             # [82, 90, 76]

# 5. Nested list comprehension — flatten a 2D list
matrix = [[1, 2], [3, 4], [5, 6]]
flat = [num for row in matrix for num in row]
print(flat)               # [1, 2, 3, 4, 5, 6]

# 6. With function call inside
def double(x): return x * 2
doubled = [double(x) for x in range(5)]
print(doubled)            # [0, 2, 4, 6, 8]

# 7. Conditional expression (ternary) inside
labels = ["pass" if s >= 50 else "fail" for s in scores]
print(labels)             # ['fail', 'pass', 'pass', 'fail', 'pass']
List Comprehension vs For Loop — Performance
import time

# For loop
result = []
for i in range(1_000_000):
    result.append(i * 2)

# List comprehension — faster, more Pythonic
result = [i * 2 for i in range(1_000_000)]

# Generator expression — most memory efficient (lazy)
result = (i * 2 for i in range(1_000_000))  # note: () not []
Interview Questions They Actually Ask
Q1: What's the difference between a list comprehension and a generator expression?
List comprehension [...] builds the entire list in memory at once. Generator expression (...) is lazy — it yields one item at a time, using almost no memory. Use generators when dealing with large datasets.
Q2: When would you NOT use a list comprehension?
When the logic is complex enough to need multiple lines, nested conditions, or side effects — a regular for loop is more readable. Senior rule: clarity beats cleverness.
Q3: What does this output?
result = [x * y for x in range(3) for y in range(3) if x != y]
print(result)
[0, 0, 2, 0, 3, 6] — nested loops with a filter. Interviewers test if you can trace nested comprehensions mentally.
Practice Problems
Beginner — p2_t01_basic_comp.py Using a list comprehension, create a list of all numbers from 1 to 50 that are divisible by 3 but not by 9. Print the result.
Senior level — p2_t01_advanced_comp.py Given a list of sentences, use a list comprehension to extract all unique words longer than 4 characters, lowercased, sorted alphabetically. Do it in one line.
sentences = [
    "Python is a powerful programming language",
    "Senior developers write clean readable code",
    "Programming requires practice and patience"
]
# expected: all unique words > 4 chars, lowercased, sorted
Common Mistakes & Senior Traps
Nesting too deep — more than 2 levels of nesting kills readability. Break it into a function.
Side effects in comprehensions — never use a comprehension just to call a function for its side effect (like print). Use a for loop for that.
Memory trap — [x for x in range(10_000_000)] creates 10M items in RAM instantly. Use a generator (x for x in ...) if you only need to iterate once.
Variable leaking myth — in Python 3, the loop variable in a comprehension does NOT leak into the outer scope (unlike Python 2). This is a common interview trick question.
x = 10
result = [x for x in range(5)]
print(x)   # still 10 in Python 3 — comprehension has its own scope
Say next for Topic 2: Dict Comprehensions!