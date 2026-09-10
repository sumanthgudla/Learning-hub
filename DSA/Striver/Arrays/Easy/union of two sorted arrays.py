nums1=[1,2,3,4,5]
nums2=[2,3,4,4,5,6]
res=set(nums1) | set(nums2)
print(res)

#this takes extra space
res=[]
i=0
j=0
while(i<len(nums1) and j<len(nums2)):
    if i > 0 and nums1[i] == nums1[i - 1]:
            i += 1
            continue
        
        # Skip duplicates in arr2
    if j > 0 and nums2[j] == nums2[j - 1]:
            j += 1
            continue
    if(nums1[i]==nums2[j]):
        res.append(nums1[i])
        i+=1
        j+=1
    elif(nums1[i]<nums2[j]):
        res.append(nums1[i])
        i+=1
    else:
        res.append(nums2[j])
        j+=1

while(i<len(nums1)):
     if i > 0 and nums1[i] == nums1[i - 1]:
        i += 1
        continue
     res.append(nums1[i])
     i+=1
while(j<len(nums2)):
     if j>0 and nums2[j]==nums2[j-1]:
        j+=1
        continue
     res.append(nums2[j])
     j+=1
print(res)
