def rateLimiter(max_calls):
    number_calls=0
    def decorator(func):
        def wrapper(*args,**kwargs):
            nonlocal number_calls
            if number_calls<max_calls:
                print(number_calls)
                number_calls+=1
                return func(*args,**kwargs)
            else :
                print("Limit exceeded")
        return wrapper
    return decorator





@rateLimiter(max_calls=3)
def PrintWord():
    print("hello")
    


if __name__ == '__main__':
    PrintWord()
    PrintWord()
    PrintWord()   
    PrintWord()