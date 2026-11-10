class Employee:
    def __init__(self,name,salary):
        self.name=name
        self.salary=salary
    def __str__(self):
        return f"{self.name} {self.salary}"

    def __repr__(self):
        return f"{self.name} + {self.salary}"

    def __add__(self,other):
        return self.salary+other.salary

    def __lt__(self, other):
        return self.salary<other.salary


e=Employee("Sumanth",5000)
e2=Employee("Sumanth",51000)

print(e<e2)