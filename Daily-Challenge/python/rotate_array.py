nums=[1,2,3,4,5,6]
k=3
'''for i in range(k):
    nums.insert(0,nums[-1])
    nums.pop()
print(nums)
'''
nums=nums[k-1::-1]+nums[len(nums):k-1:-1]
nums=nums[::-1]
print(nums)


