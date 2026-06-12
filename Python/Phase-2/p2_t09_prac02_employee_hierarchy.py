class Employee():
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_salary(self):
        return self.base_salary


class Developer(Employee):
    def __init__(self, name, base_salary, overtime_hours=0, overtime_rate=200):
        super().__init__(name, base_salary)
        self.overtime_hours = overtime_hours
        self.overtime_rate = overtime_rate

    def calculate_salary(self):
        return super().calculate_salary() + (self.overtime_hours * self.overtime_rate)


class Manager(Employee):
    def __init__(self, name, base_salary, bonus=0):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_salary(self):
        return super().calculate_salary() + self.bonus


class TeamLead(Developer, Manager):
    def __init__(self, name, base_salary, overtime_hours=0, overtime_rate=200, bonus=0):
        Employee.__init__(self, name, base_salary)
        self.overtime_hours = overtime_hours
        self.overtime_rate = overtime_rate
        self.bonus = bonus

    def calculate_salary(self):
        return self.base_salary + (self.overtime_hours * self.overtime_rate) + self.bonus


if __name__ == '__main__':
    tl = TeamLead("Arjun", base_salary=50000, overtime_hours=10, overtime_rate=200, bonus=5000)
    print(tl.calculate_salary())
