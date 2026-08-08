nums=[1,2,3,4,5,6,7]
Target=9
for i in range(len(nums)):
    for j in range(i+1,len(nums)):
        if nums[i]+nums[j]==Target:
            print(nums[i],nums[j])

set_nums=set()
for i in nums:
    if Target-i in set_nums:
        print(i,Target-i)
    set_nums.add(i)
