s='Sumanth is a good boy'
str_list=s.split(' ')
max_num=float('-inf')
max_word=str_list[0]
for i in str_list:
    if len(i)>max_num:
        max_num=len(i)
        max_word=i

print(max_word)