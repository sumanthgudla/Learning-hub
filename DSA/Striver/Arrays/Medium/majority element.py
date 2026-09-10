nums = [7, 0, 0, 1, 7, 7, 2, 7, 7]  
majority_element=nums[0]
majority_count=1
for num in nums:
    if num!=majority_element:
        majority_count-=1
        if majority_count==0:
            majority_element=num
            majority_count=1
    else:
        majority_count+=1
print(majority_element)
