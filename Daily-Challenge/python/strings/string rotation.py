s1='sumantha'
s2='manthsu'
if len(s1)==len(s2) and s2 in s1+s1:
    print(True)
else:
    print(False)
    


first_matching_char=s1[0]
index=0
index_1=0
for j in range(0,len(s2)):
    if first_matching_char==s2[j]:
        index=j
        index_1=j
        break
is_string_rotation=True
i=0
print(index)
while(index<len(s2)):
    print(s1[i]," ",s2[index])
    if s1[i]!=s2[index]:
        is_string_rotation=False
        break
    i+=1
    index+=1

for j in range(0,index_1):
    print(s1[i]," ",s2[j])
    if s1[i]!=s2[j]:
        is_string_rotation=False
        break
    i+=1
if (len(s1)!=len(s2)):
    print(False)
else:
    print(is_string_rotation)


