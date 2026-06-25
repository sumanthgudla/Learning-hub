def uppercase(func):
    def wrapper(*args,**kwargs):
        print(args[0].upper())
        return func(*args,**kwargs)
    return wrapper



@uppercase
def greetName(Message="Hell0"):
    print(Message)


if __name__=='__main__':
    greetName("Hi")