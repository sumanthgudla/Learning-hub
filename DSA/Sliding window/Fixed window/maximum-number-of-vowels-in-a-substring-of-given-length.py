s='abciiidef'
k=5
start=0
ovwels=('a','e','i','o','u')
max_length=float('-inf')
ovwel_list=[]
for end in range(len(s)):
    if(s[end] in ovwels):
        ovwel_list.append(s[end])
    if(end-start+1==k):
        print(s[start])
        max_length=max(max_length,len(ovwel_list))
        if s[start] in ovwels:
            ovwel_list.remove(s[start])
        start+=1
        
print(max_length)
    