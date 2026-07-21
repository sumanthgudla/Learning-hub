nums=[1,2,3,4,5,7,8,9]
for i in range(1,len(nums)+1):
    if i!=nums[i-1]:
        print(i)
        break



