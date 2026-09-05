nums = [1, 2, 3,41, 4, 5]
is_sorted=True
for i in range(1,len(nums)):
    if nums[i-1]>nums[i]:
        is_sorted=False
        break
print(is_sorted)
