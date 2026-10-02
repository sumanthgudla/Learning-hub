arr=[1,5,4,2,9,9,9]
k=3
start=0
max_sum=0
window_sum=0
window_set={}
for i in range(len(arr)):
    window_sum=window_sum+arr[i]
    window_set[arr[i]]=window_set.get(arr[i],0)+1
    if(i-start+1>k):
        window_sum-=arr[start]
        if(window_set.get(arr[start])==1):
            window_set.pop(arr[start])
        else:
            window_set[arr[start]]=window_set.get(arr[start])-1
        start+=1
    if(len(window_set)==k):
        max_sum=max(max_sum,window_sum)
print(max_sum)

