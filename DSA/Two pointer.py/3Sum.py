nums = [-1, 0, 1, 2, -1, -4]
nums=sorted(nums)
for idx,num in enumerate(nums):
    if (nums[idx]==nums[idx-1]):
        continue
    left=idx+1
    right=len(nums)-1
    while(left<right):
        current_sum=nums[left]+nums[right]+num
        if(current_sum==0):
            print("target found")
            print(num,nums[left],nums[right])
            left+=1
            right-=1
            while(left<right and nums[left]==nums[left-1]):
                left+=1
            while(left<right and nums[right]==nums[right-1]):
                right-=1
            
        elif current_sum<0:
            left+=1
        else:
            right-=1
        

