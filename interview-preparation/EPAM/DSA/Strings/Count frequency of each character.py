from collections import Counter
S='SUmanth'
StringCounter=Counter(S)
print(StringCounter)
StrC={}
for ch in S:
    StrC[ch]=StrC.get(ch,0)+1
print(StrC)