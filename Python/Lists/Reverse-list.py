#Reverse a list in-place without using reverse() or slicing.

nums_list=[9,8,7,6,5,4,3,2,2]
reverse_list=nums_list[::-1]
print(f"reverse_list {reverse_list}")

#Remove duplicates while preserving order.

nums_set=set()
for i in nums_list:
    nums_set.add(i)
print(f"after removing duplicates. {nums_set}")


#Flatten an arbitrarily nested list (recursive + iterative).



