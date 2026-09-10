nums=[2, 5, 1, 3, 0]
print(max(nums))
max=float('-inf')

for num in nums:
    if num>max:
        max=num
print(max)