nums = [2, 3, 4, 5, 3]
target=3
for idx,num in enumerate(nums):
    if target==num:
        print(idx)
        break