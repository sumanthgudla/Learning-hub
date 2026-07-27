original_list=[41, 32, 31, 24, 23, 22, 21, 13, 12, 11, 3, 1]
k=2
k=k%len(original_list)
print(k)
res=[]
for i in range(len(original_list)-2,len(original_list)):
    res.append(original_list[i])
for i in range(len(original_list)-2):
    res.append(original_list[i])
print(res)

res=original_list[len(original_list)-k:len(original_list)]
res.extend(original_list[:len(original_list)-k])
print(res)