nums1=[5,9,13,45]
nums2=[1,3,6,8,9,15]
low_array1=0
low_array2=0
high_array1=len(nums1)
high_array2=len(nums2)
res=[]
while(low_array1<high_array1 and low_array2<high_array2):
    if(nums1[low_array1]<nums2[low_array2]):
        res.append(nums1[low_array1])
        low_array1+=1
    else:
        res.append(nums2[low_array2])
        low_array2+=1
while(low_array1<high_array1):
    res.append(nums1[low_array1])
    low_array1+=1

while(low_array2<high_array2):
    res.append(nums2[low_array2])
    low_array2+=1
print(res)


