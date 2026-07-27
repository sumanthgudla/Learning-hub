nums=[3, 2, 1, 5, 4]
k=2
for i in range(k):
    last=nums[-1]
    for idx in range(len(nums)-1,0,-1):
        nums[idx]=nums[idx-1]
    nums[0]=last
print(nums)
nums=[3, 2, 1, 5, 4]
snum=nums[-k:]+nums[:-k]
print(snum)
  
