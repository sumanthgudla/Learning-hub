employees = {
    "Alice": 50000,
    "Bob": 75000,
    "Charlie": 65000,
    "David": 90000,
    "Eve": 85000
}
max_salary=0
name=''
for key,value in employees.items():
    if value>max_salary:
        max_salary=value
        name=key
print(name,max_salary)
        

max_salary=max(employees,key=employees.get)
print(max_salary)