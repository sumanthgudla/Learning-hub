S='aaaabbbccc'
dict_s={}
for i in S:
    dict_s[i]=dict_s.setdefault(i,0)+1
print(dict_s)