nums1=[1,1,2,3,3,3,3]
num_dict={}
for num in nums1:
    num_dict[num]=num_dict.get(num,0)+1
num_dict=dict(sorted(num_dict.items(),key=lambda x:x[1],reverse=True))
print(num_dict)
candidate=nums1[0]
count=0
for num in nums1:
    if num==candidate:
        count+=1
    else:
        if count>0:
            count-=1
        else:
            candidate=num

print(candidate)
