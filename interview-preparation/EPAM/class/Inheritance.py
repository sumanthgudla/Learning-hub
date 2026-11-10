class Person:
    def __init__(self,name,age):
        self.name=name
        self.age=age
    def __str__(self):
        return f"{self.name} {self.age}"

class Employee(Person):
    def __init__(self, name, age,salary):
        super().__init__(name, age)
        self.salary=salary
    def __str__(self):
        return f"{super().__str__()} {self.salary}"

e=Employee("Sumanth",25,50000)
print(e)


class Animal:
    def __init__(self,name):
        self.name=name

    def animal_sound(self):
        print("Animal sound")

class Dog(Animal):
    def __init__(self, name,sound="Meow"):
        super().__init__(name)
        self.sound=sound

    def animal_sound(self):
        super().animal_sound()
        print(self.sound)


D=Dog("chintu",'bark')
D.animal_sound()


class PythonSkills:
    def __init__(self):
        pass
    def python(self):
        print("learning python")


class AswSkills:
    def aws(self):
        print("aws learning")


class AIEngineer(AswSkills,PythonSkills):
    pass


A=AIEngineer()
A.aws()
A.python()

