from collections import Counter
s= "listen"
t = "silent"
counter_s={}
counter_t={}

for idx,char in enumerate(s):
    counter_s[char]=counter_s.get(char,0)+1
for idx,char in enumerate(t):
    counter_t[char]=counter_t.get(char,0)+1

print(counter_s,counter_t)
if(counter_s==counter_t):
    print("Valid anagram")
else:
    print("Not valid anagram")
print(Counter(s))

