nums = [1,12,-5,-6,50,3]
k=4
start=0
max_sum=float('-inf')
window_sum=0
max_average=0
for i in range(len(nums)):
    window_sum+=nums[i]
    if(i-start+1>k):
        window_sum-=nums[start]
        start+=1
    if(i-start+1==k):
        max_average=max(max_average,window_sum/k)
print(max_average)
