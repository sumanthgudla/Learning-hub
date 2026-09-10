nums=[1 ,0 ,2 ,3 ,0 ,4 ,0 ,1]
zeropos=0
for idx,num in enumerate(nums):
    if num!=0:
        nums[zeropos],nums[idx]=nums[idx],nums[zeropos]
        zeropos+=1
print(nums)

        