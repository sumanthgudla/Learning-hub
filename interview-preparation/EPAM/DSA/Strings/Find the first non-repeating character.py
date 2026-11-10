from collections import Counter
S='SUmanth'
StringCounter=Counter(S)
for ch in S:
    if StringCounter[ch]==1:
        print(ch)
        break