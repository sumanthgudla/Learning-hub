class Employee:
    total=0
    company=''
    def employee_bonus(self):
        return self.salary*1.1
    def __str__(self):
        return f"{self.name} ,{self.salary}"
    @classmethod
    def total_objects(cls):
        cls.total=cls.total+1
        return cls.total
    @classmethod
    def UpdateCompany(cls,company):
        cls.company=company
    @staticmethod
    def validAge(age):
        if age>18:
            return "valid"
        else:
            return "invalid"

e1=Employee("sumanth",10)
e2=Employee("Bharath",12)
e3=Employee("Shkar",23)
print(Employee.total)
e1.UpdateCompany("pega")
print(e2.company)
print(e1.employee_bonus())
print(e1)
print(Employee.validAge(25))
