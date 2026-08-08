nums = [1, 2, 3, -2, 2]
k=3
number_sum=0
window=[]
for i in nums:
    window.append(i)
    
    if(sum(window)>k):
        while(sum(window)>k):
            if(sum(window)==k):
                print(window)
            window.pop(0)
    if(sum(window)==k):
        print(window)
prefix_sum={}
prefix_sum[0]=0
sum_num=0
for idx,i in enumerate(nums):
    sum_num=sum_num+i
    if sum_num-k in prefix_sum:
        first_index=nums[k-sum_num]-1
        print(nums[first_index:idx+1])
    prefix_sum[sum_num]=idx+1

print(prefix_sum)
    






