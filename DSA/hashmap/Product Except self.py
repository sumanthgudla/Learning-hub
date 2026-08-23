nums = [1, 2, 3, 4]
prefix=[]
suffix=[]
prefix.append(1)
prod=1
for num in nums:
    prod=prod*num
    prefix.append(prod)
print(prefix)
prod=1
suffix.append(1)
for num in nums[:0:-1]:
    prod=prod*num
    suffix.append(prod)
suffix=suffix[::-1]
print(suffix)
for i in range(len(nums)):
    print(suffix[i]*prefix[i])
