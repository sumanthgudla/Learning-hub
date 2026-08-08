nums = [1, 2, 3, 4, 5,5]
set_nums=set()
unique_elements=True
for i in nums:
    if i in set_nums:
        unique_elements=False
    set_nums.add(i)
print(unique_elements)