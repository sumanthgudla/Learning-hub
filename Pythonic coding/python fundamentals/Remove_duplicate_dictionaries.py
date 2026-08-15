employees = [
    {"id": 101, "name": "John", "department": "IT"},
    {"id": 102, "name": "Alice", "department": "HR"},
    {"id": 101, "name": "John", "department": "IT"},
    {"id": 103, "name": "Bob", "department": "Finance"},
    {"id": 102, "name": "Alice", "department": "HR"},
]
unique_dictionaries=[]
unique_keys=set()
for dictionary in employees:
    if dictionary['id'] not in unique_keys:
        unique_dictionaries.append(dictionary)
    unique_keys.add(dictionary['id'])
print(unique_dictionaries)