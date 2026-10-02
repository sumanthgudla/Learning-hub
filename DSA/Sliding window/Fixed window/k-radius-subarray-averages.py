nums = [7,4,3,9,1,8,5,2,6]
k=3
res=[]
print(k)
start=0
windows_sum=0
for end in range(len(nums)):
    if(end-k>=0 and end+k<len(nums)):
        res.append(sum(nums[end-k:end+k+1])//(2*k+1))
    else:
        res.append(-1)
print(res)

