students = [
    {"name": "Arjun",  "score": 85},
    {"name": "Priya",  "score": 42},
    {"name": "Ravi",   "score": 91},
    {"name": "Sneha",  "score": 38},
    {"name": "Kiran",  "score": 76},
    {"name": "Divya",  "score": 55},
    {"name": "Raj",    "score": 95},
]

# ── helper functions ──────────────────────────
def get_grade(score):
    if score >= 90: return "A"
    if score >= 80: return "B"
    if score >= 70: return "C"
    return "D"

def add_grade(student):
    return {**student, "grade": get_grade(student["score"])}

def sort_key(student):
    return (student["grade"], student["name"])


# ── pipeline ──────────────────────────────────
# Step 1 — filter
filtered = list(filter(lambda s: s["score"] >= 60, students))

# Step 2 — map
graded   = list(map(add_grade, filtered))

# Step 3 — sort
result   = sorted(graded, key=sort_key)

# ── print result ──────────────────────────────
for s in result:
    print(f"{s['grade']}  {s['name']:10}  {s['score']}")

# A  Raj         95
# A  Ravi        91
# B  Arjun       85
# C  Kiran       76