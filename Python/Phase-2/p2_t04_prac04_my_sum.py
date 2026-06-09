def sum(*args,multiply=False):
    t_sum=0
    
    if(not multiply):
        for i in args:
            t_sum=t_sum+i
        print(t_sum)
    else:
        multiply=1
        for i in args:
            multiply=multiply*i
        print(multiply)


sum(1,2,3,4,multiply=True)