arr = [1, 4, 2, 10, 23, 3, 1, 0, 20]
k=4
start=0
end=0
sum=0
max_sum=float('-inf')
while(end<len(arr)):
    sum+=arr[end]
    if(end>=k):
        sum-=arr[start]
        start+=1
    max_sum=max(max_sum,sum)
    end+=1
print(max_sum)



