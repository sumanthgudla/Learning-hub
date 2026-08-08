students = [
    ("Alice", "A"),
    ("Bob", "B"),
    ("Charlie", "A"),
    ("David", "C"),
    ("Eve", "B"),
    ("Frank", "A")
]

grade={}

for key, value in students:
    grade.setdefault(value,[]).append(key)
print(grade)

