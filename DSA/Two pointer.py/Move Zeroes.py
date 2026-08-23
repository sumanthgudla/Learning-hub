nums = [1, 0, 1, 0, 3, 12]
left=0
right=1
while(right<len(nums)):
    while(nums[left]!=0):
        left+=1
    while(nums[right]==0 and right<len(nums)):
        right+=1
    print(nums[left],nums[right])
    nums[left],nums[right]=nums[right],nums[left]
print(nums)