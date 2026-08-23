from collections import Counter
s = "anagram"
t = "nagaram"
if (sorted(s)==sorted(t)):
    print("valid anagram")
else:
    print("not valid one")
counter_s=Counter(s)
counter_t=Counter(t)
print(counter_s==counter_t)
c_s={}
c_t={}
for ch in s:
    c_s[ch]=c_s.get(ch,0)+1
for ch in t:
    c_t[ch]=c_t.get(ch,0)+1
print(c_s==c_t)
