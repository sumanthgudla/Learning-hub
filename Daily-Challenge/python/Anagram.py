s = "anagram"
t = "nagaram"
w1={}
w2={}
for ch in s:
    w1[ch]=w1.setdefault(ch,0)+1
for ch in t:
    w2[ch]=w2.setdefault(ch,0)+1

if(w1==w2):
    print('anagram')
else:
    print('not anagram')


