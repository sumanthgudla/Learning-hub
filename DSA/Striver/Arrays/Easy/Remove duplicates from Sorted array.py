nums=[1,1,2,2,2,3,3]
nums_set=list(set(nums))
print(nums_set)
#this will not be in order because it is set
res=[]
for num in nums:
    if num not in res:
        res.append(num)
print(res)

# this has time complexity of o(n2) because num not in res: does o(n)
res=[]
set_nums=set()
for num in nums:
    if num not in set_nums:
        set_nums.add(num)
        res.append(num)
print(res)