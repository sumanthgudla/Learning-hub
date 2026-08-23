nums = [1, 2, 3, 1]
num_set=set()
for num in nums:
    if num in num_set:
        print("duplicate found")
        break
    num_set.add(num)