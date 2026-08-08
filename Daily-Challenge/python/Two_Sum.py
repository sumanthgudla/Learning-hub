nums = [2,1,11,15,7]
target = 9
num_set={}
res=[]
for idx,i in enumerate(nums):
    if target-i in num_set:
        res.append(num_set[target-i])
        res.append(idx)
    num_set[i]=idx
print(res)

