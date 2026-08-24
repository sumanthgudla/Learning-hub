dict1 = {"a": 10, "b": 20, "c": 30}
dict2 = {"b": 5, "c": 15, "d": 40}

dict3={}
for k,v in dict1.items():
    if k in dict2:
        dict3[k]=v+dict2[k]
    else:
        dict3[k]=v

for k,v in dict2.items():
    if k not in dict3:
        dict3[k]=v
print(dict3)
        