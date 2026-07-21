nums = [2,1,11,15,7]
target = 9
res=[]
dict_nums={}
for idx,num in enumerate(nums):
    index=dict_nums.get(target-num)
    print(index)
    if index is not None:
        res=[idx,dict_nums[target-num]]
    else:
        dict_nums[num]=idx
print(res)
