nums = [1,2,3,4,5,6,7]
sum_nums=0

num_dict={}
num_dict[0]=0
max_num=-1
k=15
for idx,num in enumerate(nums):
    sum_nums=sum_nums+num
    if sum_nums-k in num_dict:
        max_num=max(max_num,idx+1-num_dict[sum_nums-k])
    if sum_nums not in num_dict:
        num_dict[sum_nums] = idx+1
print(num_dict)
print(max_num)



