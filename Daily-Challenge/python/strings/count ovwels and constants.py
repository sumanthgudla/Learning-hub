ovwels=('a','e','i','o','u')
s='Sumanth is a great person'
ovwels_count=0
const_count=0
for i in s:
    if i.lower() in ovwels:
        ovwels_count+=1
    elif i!=' ':
        const_count+=1
print(ovwels_count,' ',const_count)
