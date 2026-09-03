## 3. Instance Variables

An **instance variable is a variable that belongs to a particular object**.

The most common way to create one is using `self` inside `__init__`.

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
```

Here:

```python
self.name
self.salary
```

are **instance variables**.

---

### Why are they called "instance" variables?

Because every **instance/object gets its own copy/reference** of those attributes.

```python
emp1 = Employee("John", 50000)
emp2 = Employee("Alice", 60000)
```

Think of it as:

```text
emp1
 ├── name   → "John"
 └── salary → 50000

emp2
 ├── name   → "Alice"
 └── salary → 60000
```

Changing `emp1` doesn't change `emp2`:

```python
emp1.salary = 70000

print(emp1.salary)   # 70000
print(emp2.salary)   # 60000
```

That's the key property of instance variables.

---

## Where does `self` come from?

Suppose:

```python
emp1 = Employee("John", 50000)
```

Python effectively does something like:

```python
Employee.__init__(emp1, "John", 50000)
```

Inside:

```python
self.name = name
```

`self` is `emp1`.

So this becomes conceptually:

```python
emp1.name = "John"
```

For:

```python
emp2 = Employee("Alice", 60000)
```

`self` is now `emp2`.

So:

```python
emp2.name = "Alice"
```

---

## Instance variables don't have to be created in `__init__`

You can technically create them later:

```python
class Employee:
    def __init__(self, name):
        self.name = name

    def set_salary(self, salary):
        self.salary = salary
```

Then:

```python
emp = Employee("John")

emp.set_salary(50000)
```

Now `emp` has:

```text
name
salary
```

But normally, attributes that an object needs are initialized in `__init__`.

---

## Instance variable vs normal local variable

This is important:

```python
class Employee:
    def __init__(self, name):
        self.name = name
        age = 30
```

Here:

```python
self.name
```

is an **instance variable**.

But:

```python
age
```

is just a **local variable** inside `__init__`.

After `__init__` finishes:

```python
emp.age
```

will not exist.

---

## Interview question

**Q: What is an instance variable?**

Good answer:

> "An instance variable is an attribute associated with a particular object. Each object can have its own value for that variable. In Python, instance variables are commonly created using `self`, usually inside `__init__`."

Example:

```python
class Employee:
    def __init__(self, name):
        self.name = name
```

`self.name` is an instance variable.

---

### Don't confuse this with the next topic

```python
self.name = name
```

→ **Instance variable**

```python
Employee.company = "ABC"
```

→ **Class variable**

That's our **next topic: Class Variables**.
