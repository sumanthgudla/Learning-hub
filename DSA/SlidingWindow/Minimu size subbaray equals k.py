nums = [1, 1, 1]
k = 2
nums_set={}
nums_set[0]=0
sum=0
for idx,num in enumerate(nums):
    sum=sum+num
    nums_set[sum]=idx+1

print(nums_set)
min_len=len(nums)
for key,value in nums_set.items():
    if key-k in nums_set:
        print(nums_set[key-k],value)
        min_len=min(min_len,value-nums_set[key-k])
print(min_len)


