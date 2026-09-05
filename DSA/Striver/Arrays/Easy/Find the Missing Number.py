nums=[8, 2, 4, 5, 3, 7, 1]
for i in range(1,len(nums)+1):
    if i not in nums:
        print(i)

#this has a time complexity of o(n2)
set_nums=set(nums)
for i in range(1,len(nums)+1):
    if i not in set_nums:
        print(i)

#this has extra space
sum=0
sum1=0
for i in range(1,len(nums)+2):
    sum1=sum1+i

for i in nums:
    sum=sum+i
print(sum1-sum)