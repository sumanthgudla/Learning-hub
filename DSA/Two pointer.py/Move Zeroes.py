nums = [1, 0, 1, 0, 3, 12]
left=0
right=1
for right in range(len(nums)):
    while(left==0 and left<len(nums)):
        left+=1
    
    nums[left],nums[right]=nums[right],nums[left]