s = "egg"
t = "aed"
is_isomorphic=True
mapping_s={}
mapping_t={}
for idx in range(len(s)):
    if s[idx] in mapping_s:
        if(mapping_s[s[idx]]!=t[idx]):
            is_isomorphic=False
    else:
        mapping_s[s[idx]]=t[idx]
    if t[idx] in mapping_t:
        if mapping_t[t[idx]]!=s[idx]:
            is_isomorphic=False
    else:
        mapping_t[t[idx]]=s[idx]
print(is_isomorphic)
            

