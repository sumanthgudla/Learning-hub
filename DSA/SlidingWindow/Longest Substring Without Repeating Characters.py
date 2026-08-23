s = "abcbcbb"
word_set=set()
max_length=0
length=0
left=0
right=0
for i in range(len(s)):
    if s[i] not in word_set:
        word_set.add(s[i])
        right+=1
        max_length=max(max_length,right-left)
    else:
        while(s[i]!=s[left]):
            word_set.remove(s[left])
            left+=1
print(max_length)

