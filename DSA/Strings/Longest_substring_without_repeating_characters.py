s='aabcdefffghg'
max_length=0
'''
for i in range(len(s)):
    for j in range(i,len(s)):
        word=s[i:j+1]
        if(len(word)==len(set(word))):
            max_length=max(len(word),max_length)
print(max_length)
'''
j=0
i=0
seen=set()
while(j>=i and j<len(s)):
    while(s[j] in seen):
        seen.remove(s[i])
        i+=1
    max_length=max(max_length,j-i+1)
    seen.add(s[j])
    j+=1
print(max_length)





