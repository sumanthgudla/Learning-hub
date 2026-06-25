import time
def retry(max):

    def decorator(func):
        
        def wrapper(*args,**kwargs):
            wait_time=1
            for i in range(max):
                try:
                    return func(*args,**kwargs)
                except Exception as e:
                    wait_time*=2
                    print("attempt failed")
                    print(wait_time)
                    time.sleep(wait_time)

        return wrapper

    return decorator




@retry(max=3)
def LLM_API():
    raise ValueError("Exception")


if __name__ =="__main__":
    LLM_API()