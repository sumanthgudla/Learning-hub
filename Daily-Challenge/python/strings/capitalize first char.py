s=["apple", "banana", "cherry"]
s=[v[0].upper()+v[1:] for idx,v in enumerate(s)]
print(s)