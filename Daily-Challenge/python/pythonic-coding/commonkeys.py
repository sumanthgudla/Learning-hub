dict1={'a':1,'b':2,'c':3}
dict2={'a':5,'e':6,'c':90}
list_keys=[]
for key in dict1:
    if key in dict2:
        list_keys.append(key)
print(list_keys)
common_keys=dict1.keys() & dict2.keys()
print(common_keys)