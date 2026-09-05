nums=[2, 5, 1, 3, 0]
max=float('-inf')
second_max=float('-inf')
for num in nums:
    if num>max:
        second_max=max
        max=num

    elif num>second_max and num<max:
        second_max=num
print(second_max)