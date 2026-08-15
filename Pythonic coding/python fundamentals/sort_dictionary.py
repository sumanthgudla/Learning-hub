employees = [
    {"name": "John", "department": "IT", "salary": 70000},
    {"name": "Alice", "department": "HR", "salary": 60000},
    {"name": "Bob", "department": "IT", "salary": 75000},
    {"name": "David", "department": "Finance", "salary": 65000},
    {"name": "Emma", "department": "HR", "salary": 62000},
    {"name": "Charlie", "department": "IT", "salary": 75000},
]

sorted_employyes=sorted(employees,key=lambda x: (x['department'],-x['salary'],x['name']))
print(sorted_employyes)