Yes. Before OOP became common, programs were often written in a **procedural style**: data and functions were kept separately, and the program executed functions step-by-step.

For example, instead of:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def display(self):
        print(self.name, self.salary)

emp1 = Employee("John", 50000)
emp2 = Employee("Alice", 60000)

emp1.display()
emp2.display()
```

You could write it procedurally:

```python
def display_employee(name, salary):
    print(name, salary)


name1 = "John"
salary1 = 50000

name2 = "Alice"
salary2 = 60000

display_employee(name1, salary1)
display_employee(name2, salary2)
```

### What changes?

With OOP:

```text
Employee object
   ├── name
   ├── salary
   └── display()
```

The **data and behavior are grouped together**.

With procedural programming:

```text
name1 ──────┐
salary1 ────┼──> display_employee()
             │
name2 ──────┤
salary2 ────┘
```

The data is separate, and functions operate on that data.

---

### As the application grows

Imagine you have 10,000 employees.

Procedural code can start becoming messy:

```python
employee_names = [...]
employee_salaries = [...]
employee_departments = [...]

def calculate_salary(...):
    ...

def display_employee(...):
    ...

def promote_employee(...):
    ...

def change_department(...):
    ...
```

You have to keep track of **which data belongs to which employee**.

With OOP:

```python
emp1.calculate_salary()
emp1.promote()
emp1.change_department()
```

The employee's data and operations are bundled into the same object.

### So why did OOP become popular?

The main idea is:

> **As software becomes larger and more complex, grouping related data and behavior together makes the code easier to organize, reuse, maintain, and extend.**

But one important point for your interview:

**Procedural programming isn't "old" or bad.** Python itself supports both procedural and OOP styles. For small scripts, procedural code can actually be simpler.

### Interview answer

If they ask:

> **Why do we need classes and objects when we can just use functions and variables?**

A strong answer is:

> "For small programs, functions and variables may be sufficient. But as applications grow, we need to manage related data and behavior together. Classes allow us to encapsulate that data and behavior into objects, which improves organization, reusability, maintainability, and makes concepts like inheritance and polymorphism possible."

Next, we can go into **constructor (`__init__`)**, including **what actually happens in memory when `Employee("John", 50000)` executes**.
