nums = [2, 4, 6, 8, 10]
sum_nums=0
num_dict={}
num_dict[0]=0
for idx,num in enumerate(nums):
    sum_nums=sum_nums+num
    num_dict[idx+1]=sum_nums
print(num_dict)


list_tuples=[(1,3),(0,4)]
for j,k in list_tuples:
    print(num_dict[k+1]-num_dict[j])
        