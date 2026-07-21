nums = [0, 0, 0]
k=0
count=0
nums_dict={}
sum_nums=0
nums_dict[0]=1
for idx,num in enumerate(nums):
    sum_nums=num+sum_nums
    nums_dict[sum_nums]=nums_dict.get(sum_nums,0)+1
    if sum_nums-k in nums_dict:
        count=count+nums_dict[sum_nums-k]

print(count)
print(nums_dict)