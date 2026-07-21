nums1=[5,9,13,45]
nums2=[1,3,6,8,9,15]
lower_index_1=0
higher_index_1=len(nums1)
lower_index_2=0
higher_index_2=len(nums2)
nums3=[]
idx=0
while(lower_index_1<higher_index_1 and lower_index_2<higher_index_2):
    if(nums1[lower_index_1]<nums2[lower_index_2]):
        nums3.append(nums1[lower_index_1])
        lower_index_1+=1
        print(lower_index_1)
    else:
        nums3.append(nums2[lower_index_2])
        lower_index_2+=1
        print(lower_index_2)
while(lower_index_1<higher_index_1):
    nums3.append(nums1[lower_index_1])
    lower_index_1+=1
    print(lower_index_1)
while(lower_index_2<higher_index_2):
    nums3.append(nums2[lower_index_2])
    lower_index_2+=1
    print(lower_index_2)
print(nums3)



