input=[100, 4, 200, 1, 3, 2]
nums=set(input)
max_count=1
for i in nums:
    count=1
    if i-1 not in nums:
        while(i+1 in nums):
            count+=1
            max_count=max(max_count,count)
            i+=1
print(max_count)
