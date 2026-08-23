nums = [2, 7, 11, 15]
target = 9
nums_set={}
for idx,num in enumerate(nums):
    if target-num in nums_set:
        print(num)
        print(idx,nums_set[target-num])
        break
    nums_set[num]=idx
