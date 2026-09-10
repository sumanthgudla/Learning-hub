nums = [2, 3, 5, -2, 7, -4]  
sum=nums[0]
max_sum=nums[0]
for num in range(1,len(nums)):
    if sum<0:
        sum=num
    else:
        sum=sum+num
        max_sum=max(max_sum,sum)
print(max_sum)