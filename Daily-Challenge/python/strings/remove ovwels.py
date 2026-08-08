s='Sumanth is a good boy'
str_list=[]
ovwel={'a','e','i','o','u'}
for i in s:
    if i not in ovwel:
        str_list.append(i)

print(''.join(str_list))

