nums = [1, 2, 2, 3, 1, 1, 4]
dict_nums={}
for i in nums:
    dict_nums[i]=dict_nums.get(i,0)+1
print(dict_nums)