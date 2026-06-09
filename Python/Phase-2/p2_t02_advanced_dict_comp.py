'''Senior level — p2_t02_advanced_dict_comp.py
Given the list of students below, build a dictionary of only passing students (score ≥ 50), where the key is the name and the value is their letter grade. Do it in one dict comprehension.
'''

students = [
    {"name": "Arjun",  "score": 85},
    {"name": "Priya",  "score": 42},
    {"name": "Ravi",   "score": 91},
    {"name": "Sneha",  "score": 38},
    {"name": "Kiran",  "score": 76},
    {"name": "Divya",  "score": 55},
]


grades={student["name"]: "A" if student["score"]>90 else "B" if student["score"]>85 else "C"  for student in students }
print(grades)