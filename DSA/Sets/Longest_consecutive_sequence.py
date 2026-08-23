nums = [100, 4, 200, 1, 3, 2]
max_length=1
set_nums=set(nums)
for i in range(len(nums)):
    if(nums[i]-1 not in set_nums):
        length=1
        k=nums[i]
        while(k+1 in set_nums):
            length+=1
            k+=1
        max_length=max(max_length,length)
print(max_length)
