s='leetcodesasl'
char_count={}
for i in s:
    char_count[i]=char_count.setdefault(i,0)+1
print(char_count)

for ch in s:
    if char_count[ch]==1:
        print(ch)
        break