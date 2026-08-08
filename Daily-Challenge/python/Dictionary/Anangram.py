word1='eata'
word2='ate'
dict1={}
dict2={}
for w in word1:
    dict1[w]=dict1.get(w,0)+1
for w in word2:
    dict2[w]=dict2.get(w,0)+1
if dict1==dict2:
    print(True)
else:
    print(False)
