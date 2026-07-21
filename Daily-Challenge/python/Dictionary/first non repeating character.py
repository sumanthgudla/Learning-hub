s='abbca'
dict_s={}
for i in s:
    dict_s[i]=dict_s.get(i,0)+1

for i in s:
    if dict_s[i]==1:
        print(i)
