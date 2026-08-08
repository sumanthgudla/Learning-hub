dict1 = {"a": 40, "b": 20, "c": 30}

dict1=dict(sorted(dict1.items(),key=lambda x :x[1]))
print(dict1)