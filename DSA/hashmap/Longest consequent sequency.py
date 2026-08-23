nums = [100, 4, 200, 1, 3, 2]
max_length=1
num_set=set(nums)
for num in nums:
    if num-1 not in num_set:
        length=1
        while(num+1 in num_set):
            length+=1
            num+=1
        max_length=max(max_length,length)

print(max_length)
        

