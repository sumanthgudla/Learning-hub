nums_set=[3,2,1,4,5,6,7]

def merge_sort(low,high,nums_set):
    if(low>=high):
        return nums_set
    mid=(low+high)//2
    merge_sort(low,mid,nums_set)
    merge_sort(mid+1,high,nums_set)
    merge_arrays(low,mid,high,nums_set)
    return nums_set

def merge_arrays(low,mid,high,nums_set):
    left=low
    res=[]
    upper_mid=mid+1
    while(low<=mid and upper_mid<=high):
        if(nums_set[low]<nums_set[upper_mid]):
            res.append(nums_set[low])
            low+=1
        else:
            res.append(nums_set[upper_mid])
            upper_mid+=1
    while(low<=mid):
        res.append(nums_set[low])
        low+=1
    while(upper_mid<=high):
        res.append(nums_set[upper_mid])
        upper_mid+=1
    
    for i in range(len(res)):
        nums_set[left+i] = res[i]

    print(nums_set)

res=merge_sort(0,len(nums_set)-1,nums_set)
print(res)