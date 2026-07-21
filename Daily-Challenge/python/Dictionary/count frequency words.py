sentence='is is a a a great person great'
list_s=sentence.split(' ')
dict_s={}
for i in list_s:
    dict_s[i]=dict_s.setdefault(i,0)+1
print(dict_s)
