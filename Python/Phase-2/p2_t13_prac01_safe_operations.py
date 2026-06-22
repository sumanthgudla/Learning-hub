def safe_divide(a,b):
        try:
            ans=a/b
        except Exception as e:
            print("error")        
if __name__=='__main__':
    safe_divide(1,0)

    