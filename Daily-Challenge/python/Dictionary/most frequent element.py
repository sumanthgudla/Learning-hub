nums=[1, 3, 2, 1, 4, 1,2,3,2,2,2,2,2]
nums_dict={}
for i in nums:
    nums_dict[i]=nums_dict.get(i,0)+1
print(nums_dict)
max_num=0
max_element=0
for k,v in nums_dict.items():
    if v>max_num:
        max_num=v
        max_element=k
print(max_element)

