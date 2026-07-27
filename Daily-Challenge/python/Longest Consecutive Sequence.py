nums = [100, 4, 200, 1, 3, 2]
set_nums=set(nums)
max_count=0
print(set_nums)
for num in set_nums:
    if num-1 not in set_nums:
        count=1
        while(num+1 in set_nums):
            count+=1
            num=num+1
        max_count=max(max_count,count)
print(max_count)