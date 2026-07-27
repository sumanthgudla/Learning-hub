nums=[1,0,9,0,8,8,7,0]
last_index=len(nums)-1
first_index=0
while(nums[last_index]==0):
    last_index-=1
    
while(first_index<last_index):
    if nums[first_index]==0:
        temp=nums[last_index]
        nums[last_index]=nums[first_index]
        nums[first_index]=temp
        while(nums[last_index]==0):
            last_index-=1
        last_index-=1
    first_index+=1
print(nums)
        
        
