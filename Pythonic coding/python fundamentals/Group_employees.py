from collections import defaultdict
employees = [
    {"name": "John", "department": "IT", "salary": 70000},
    {"name": "Alice", "department": "HR", "salary": 60000},
    {"name": "Bob", "department": "IT", "salary": 75000},
    {"name": "David", "department": "Finance", "salary": 65000},
    {"name": "Emma", "department": "HR", "salary": 62000},
]
it_dict=defaultdict(list)
for employee in employees:
    it_dict[employee['department']].append(employee)
print(it_dict)

