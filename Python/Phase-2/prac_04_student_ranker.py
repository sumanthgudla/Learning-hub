'''prac_04_student_ranker.py
Given a list of students, build a dict of name → rank (1 = highest score). Rank them without using enumerate on a pre-sorted list — use comprehension + sorting.
'''

students = [
    {"name": "Arjun",  "score": 85},
    {"name": "Priya",  "score": 92},
    {"name": "Ravi",   "score": 78},
    {"name": "Sneha",  "score": 92},
    {"name": "Kiran",  "score": 65},
]
# expected: {'Priya': 1, 'Sneha': 1, 'Arjun': 3, 'Ravi': 4, 'Kiran': 5}
# tied scores get same ran

sorted_scores= sorted({s['score'] for s in students}, reverse=True)
rank_score={s['name'] : sorted_scores.index(s['score'])+1 for s in students}
print(sorted_scores)
print(rank_score)

