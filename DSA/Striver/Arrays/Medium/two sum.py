
nums = [1, 6, 2, 10, 3]
target= 7
#this has a time complexity of o(n2)
for num in nums:
    if target-num in nums:
        print(num,target-num)
        break

#we can do using o(n) but need a extra space using set
nums_set=set()
for num in nums:
    nums_set.add(num)
    if target-num in nums_set:
        print(num,target-num)
        break

