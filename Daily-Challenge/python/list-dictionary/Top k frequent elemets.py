nums=[1,1,1,1,2,2,2,2,2,2,2,3,3,3,3]
k=2
num_dict={}
for i in nums:
    num_dict[i]=num_dict.get(i,0)+1
print(num_dict)
for i in list(num_dict.keys())[:k]:
    print(i)