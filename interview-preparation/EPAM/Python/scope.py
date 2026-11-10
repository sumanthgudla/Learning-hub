#Create a function with a local variable and access it.
def calcualte():
    x=20
    print(x)
calcualte()

#Modify a global variable inside a function.
x=20
def calcualte():
    global x
    x=x+20
    print(x)
calcualte()
#Create two nested functions and access the outer variable.
def outer():
    x=20
    def inner():
        print(x)
    inner()
outer()
#Modify an outer function variable inside an inner function.
def outer():
    x=20
    def inner():
        nonlocal x
        x=x+10
        print(x)
    inner()

outer()
#Create a counter using closures.

def outer():
    x=20
    def inner():
        nonlocal x
        x=x+10
        print("op",x)
        return x
    return inner

x=outer()
print(x())
print(x())


#Create a multiplier function using closures.

def outer():
    x=5
    def inner():
        nonlocal x
        x=x*2
        return x
    return inner

output=outer()
print(output())
print(output())