s = "AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT"
start=0
k=10
sub_set=set()
res=[]
for end in range(len(s)):
    if end-start+1==k:
        sub_string=s[start:end+1]
        if sub_string in sub_set:
            res.append(sub_string)
        sub_set.add(sub_string)
        start+=1
print(res)

