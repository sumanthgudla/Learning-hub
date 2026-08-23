nums=[1,2,-1,-8,9,-9]
i=0
j=0
res=[]
pos=0
while(i<len(nums) or j<len(nums)):
    pos=pos+1

    if pos%2==0:
        while(i<len(nums)):
            if(nums[i]>0):
                break
            i=i+1
        res.append(nums[i])
        i=i+1
    else:
        while(j<len(nums)):
            if(nums[j]<0):
                break
            j=j+1
        res.append(nums[j])
        if(j<len(nums)):
            j=j+1
print(res)




