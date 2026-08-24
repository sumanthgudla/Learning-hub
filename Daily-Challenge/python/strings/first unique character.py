s='aaabcdsssed'
for i in range(len(s)):
    is_char_found=False
    for j in range(len(s)):
        if i != j and s[i] == s[j]:
            is_char_found=True
            break
    if(is_char_found==False):
        print(s[i])
        break
dict_string={}
for i in s:
    dict_string[i]=dict_string.get(i,0)+1
for i in s:
    if dict_string[i]==1:
        print(i)   
        break