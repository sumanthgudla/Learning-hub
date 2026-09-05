nums = [1, 2, 3, 4, 5]
k=3
for i in range(k-1):
    temp=nums[0]
    nums.remove(temp)
    nums.append(temp)
print(nums)
nums = [1, 2, 3, 4, 5]
#this takes n*k time complexity


nums=nums[:k-1][::-1]+nums[k-1:][::-1]
nums=nums[::-1]
print(nums)

#using slicing takes extra space for rverse

nums[:k]=reversed(nums[:k])
nums[k:]=reversed(nums[k:])
nums[:]=reversed(nums)
print(nums)



