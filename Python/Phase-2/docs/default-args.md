Here's Phase 2 — Topic 4: Default args / *args / **kwargs in notes-friendly format:
Phase 2 — Topic 4: Default Args / *args / **kwargs
What is it?
Python functions can accept arguments in flexible ways. Default args give parameters a fallback value. *args lets a function accept any number of positional arguments. **kwargs lets a function accept any number of keyword arguments. Senior devs use these to write flexible, reusable APIs.
1. Default Arguments
# Without default — must always pass all arguments
def greet(name, message):
    print(f"{message}, {name}!")

greet("Arjun", "Hello")      # Hello, Arjun!
greet("Arjun")               # ❌ TypeError — message missing


# With default — argument becomes optional
def greet(name, message="Hello"):
    print(f"{message}, {name}!")

greet("Arjun")               # Hello, Arjun!   ← uses default
greet("Arjun", "Welcome")    # Welcome, Arjun! ← overrides default


# Multiple defaults
def create_user(name, role="user", active=True):
    return {"name": name, "role": role, "active": active}

create_user("Arjun")                        # {'name':'Arjun','role':'user','active':True}
create_user("Priya", role="admin")          # {'name':'Priya','role':'admin','active':True}
create_user("Ravi",  role="admin", active=False)  # all overridden
2. Default Argument Trap — Mutable Default
# THE MOST COMMON SENIOR INTERVIEW TRAP

# WRONG — mutable default argument
def add_item(item, basket=[]):    # ❌ list created ONCE at definition
    basket.append(item)
    return basket

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['apple', 'banana']  ← WRONG! should be ['banana']
print(add_item("cherry"))  # ['apple', 'banana', 'cherry']  ← keeps growing!

# WHY — default list is created once when function is defined
# same list object is reused every call


# CORRECT — use None as default, create inside function
def add_item(item, basket=None):   # ✅
    if basket is None:
        basket = []                # new list created every call
    basket.append(item)
    return basket

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['banana']  ← correct!
3. *args — Variable Positional Arguments
# * collects all extra positional args into a TUPLE

def add(*args):
    print(type(args))   # <class 'tuple'>
    print(args)         # (1, 2, 3, 4, 5)
    return sum(args)

print(add(1, 2))           # 3
print(add(1, 2, 3, 4, 5))  # 15
print(add())               # 0  ← empty tuple, sum=0


# Mix with regular args — regular args FIRST
def greet(greeting, *names):
    for name in names:
        print(f"{greeting}, {name}!")

greet("Hello", "Arjun", "Priya", "Ravi")
# Hello, Arjun!
# Hello, Priya!
# Hello, Ravi!


# Unpacking a list into *args
numbers = [1, 2, 3, 4, 5]
print(add(*numbers))   # 15  ← * unpacks list into positional args
4. **kwargs — Variable Keyword Arguments
# ** collects all extra keyword args into a DICT

def show_info(**kwargs):
    print(type(kwargs))   # <class 'dict'>
    print(kwargs)

show_info(name="Arjun", age=22, city="Vijayawada")
# {'name': 'Arjun', 'age': 22, 'city': 'Vijayawada'}


# Loop through kwargs
def display(**kwargs):
    for key, value in kwargs.items():
        print(f"{key:10} : {value}")

display(name="Arjun", age=22, city="Vijayawada")
# name       : Arjun
# age        : 22
# city       : Vijayawada


# Unpacking a dict into **kwargs
data = {"name": "Arjun", "age": 22}
display(**data)   # ** unpacks dict into keyword args
5. Combining All Four — Correct Order
# ORDER RULE — always this sequence:
# def func(regular, default, *args, **kwargs)

def func(a, b=10, *args, **kwargs):
    print(f"a      = {a}")
    print(f"b      = {b}")
    print(f"args   = {args}")
    print(f"kwargs = {kwargs}")

func(1, 2, 3, 4, 5, x=10, y=20)
# a      = 1
# b      = 2
# args   = (3, 4, 5)
# kwargs = {'x': 10, 'y': 20}


# Real world example — database query builder
def query(table, limit=10, *filters, **conditions):
    print(f"SELECT * FROM {table}")
    print(f"LIMIT  : {limit}")
    print(f"FILTERS: {filters}")
    print(f"WHERE  : {conditions}")

query("users", 5, "active", "verified", age=22, city="Vijayawada")
# SELECT * FROM users
# LIMIT  : 5
# FILTERS: ('active', 'verified')
# WHERE  : {'age': 22, 'city': 'Vijayawada'}
6. Keyword-Only Arguments — * alone
# * forces everything after it to be keyword-only
def create_user(name, *, role="user", active=True):
    #                  ↑
    #            bare * — no variable name
    #            everything after MUST be passed as keyword
    return {"name": name, "role": role, "active": active}

create_user("Arjun")                    # ✅
create_user("Arjun", "admin")           # ❌ TypeError
create_user("Arjun", role="admin")      # ✅ must use keyword
Interview Questions They Actually Ask
Q1: What is the mutable default argument trap?
Default arguments are evaluated once at function definition time, not each call. So a mutable default like [] or {} is shared across all calls. Always use None as default and create the mutable object inside the function.
Q2: What's the difference between *args and **kwargs?
*args collects extra positional arguments into a tuple. **kwargs collects extra keyword arguments into a dict. Together they allow a function to accept any combination of arguments.
Q3: What does ** do when calling a function?
def add(a, b, c):
    return a + b + c

nums = {"a": 1, "b": 2, "c": 3}
add(**nums)   # unpacks dict → add(a=1, b=2, c=3)
# 6
Q4: What is the correct order of parameters?
def func(positional, default=val, *args, **kwargs):
#         ↑              ↑          ↑        ↑
#       required       optional   extra    extra
#                                 pos     keyword
Q5: Can you have **kwargs without *args?
def func(a, **kwargs):   # ✅ perfectly fine
    pass
# *args is not required before **kwargs
Practice Problems
Beginner — p2_t04_flexible_greeting.py Write a function greet that takes a name, an optional title (default "Mr/Ms"), and any number of extra traits as *args. Print a greeting using all of them.
greet("Arjun")
# Hello Mr/Ms Arjun!

greet("Priya", "Dr", "brilliant", "experienced")
# Hello Dr Priya! Known for: brilliant, experienced
Senior level — p2_t04_config_builder.py Write a function build_config that:
Takes a required app_name
Has defaults: version="1.0", debug=False
Accepts any number of plugin names via *args
Accepts any number of settings via **kwargs
Returns a fully built config dict
config = build_config(
    "MyApp",
    "2.0",
    True,
    "auth", "logging", "cache",
    db_host="localhost",
    db_port=5432,
    max_connections=100
)

# expected:
{
    "app_name"  : "MyApp",
    "version"   : "2.0",
    "debug"     : True,
    "plugins"   : ("auth", "logging", "cache"),
    "settings"  : {
        "db_host"        : "localhost",
        "db_port"        : 5432,
        "max_connections": 100
    }
}
Common Mistakes & Senior Traps
Mutable default argument — never use [], {}, or set() as default. Always use None and create inside.
Wrong order — def func(*args, a) causes TypeError. Regular args always come before *args.
*args is a tuple not a list — you can't append to it. Convert with list(args) if needed.
Confusing * in definition vs call — in definition *args collects, in call *list unpacks. Opposite directions.
Overusing **kwargs — if your function always needs specific keys, name them explicitly. **kwargs hides what the function actually needs — bad for readability.
Say next for Topic 5: Lambda, map, filter!