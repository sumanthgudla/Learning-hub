nums = [1,1,1,2,2,3]
k = 2
num_dict={}
for num in nums:
    num_dict[num]=num_dict.get(num,0)+1
num_dict=dict(sorted(num_dict.items(),key=lambda x:x[1],reverse=True))
res=[k for k in num_dict.keys()][:k]
print(res)

