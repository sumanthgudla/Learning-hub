S="hello"
ovwels=('a','e','i','o','u')
ovwel_count=0
for ch in S:
    if ch in ovwels:
        ovwel_count+=1
print(ovwel_count)