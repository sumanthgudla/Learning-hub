nums = [10, 5, 2, 7, 1, 9]
nums_dict={}
max_subbaray=0
k=15
nums_dict[0]=0
sum=0
for idx,num in enumerate(nums):
    sum=sum+num
    nums_dict[sum]=nums_dict.get(sum,idx+1)
    if(sum-k in nums_dict):
        max_subbaray=max(max_subbaray,idx+1-nums_dict[sum-k])

print(max_subbaray)