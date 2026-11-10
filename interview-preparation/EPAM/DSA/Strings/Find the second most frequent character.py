from collections import Counter
S='aabbccc'
Counter_s=Counter(S)
max_count=0
max_key=''
second_max=0
second_max_key=''
print(Counter_s)
for key,value in dict(Counter_s).items():
    if(int(value)>max_count):
        second_max=max_count
        second_max_key=max_key
        max_count=value
        max_key=key
    elif(int(value)>second_max):
        second_max_key=key
        second_max=value
print(second_max_key)
