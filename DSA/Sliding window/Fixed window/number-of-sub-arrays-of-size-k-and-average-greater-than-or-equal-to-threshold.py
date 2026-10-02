nums=[2,2,2,2,5,5,5,8]
window_sum=0
k=3
threshold=4
start=0
number=0
for end in range(len(nums)):
    window_sum=window_sum+nums[end]
    if(end-start+1==k):
        window_sum-=nums[start]
        start+=1
        if(window_sum/k>=threshold):
            print(window_sum)
            number+=1
print(number)
