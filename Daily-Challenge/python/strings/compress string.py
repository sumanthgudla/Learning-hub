s='aaabbc'
count=1
res=''
for idx in range(1,len(s)):
    if s[idx]!=s[idx-1]:
        res=res+s[idx-1]+str(count)
        count=1
    else:
        count+=1
res=res+s[len(s)-1]+str(count)
print(res)
