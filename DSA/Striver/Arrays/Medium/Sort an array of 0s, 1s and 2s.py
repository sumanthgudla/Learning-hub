nums = [1, 0, 2, 1, 0]
zeros=0
ones=0
twos=0
for num in nums:
    if num ==0:
        zeros+=1
    elif num==1:
        ones+=1
    else:
        twos+=1

nums[0:zeros]=zeros*[0]
nums[zeros:zeros+ones]=ones*[1]
nums[zeros+ones:]=twos*[2]

print(nums)