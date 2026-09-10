nums=[1, 1, 0, 1, 1, 1]
max_1=0
max_nums=0
for num in nums:
    if num==1:
        max_1+=1
        max_nums=max(max_1,max_nums)
    else:
        max_1=0
print(max_nums)

