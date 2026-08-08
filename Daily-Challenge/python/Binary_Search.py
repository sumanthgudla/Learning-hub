nums=[1, 3, 5, 6, 8, 9, 9, 13, 15, 45]
low=0
target=5
index=0
high=len(nums)
flag=False
while(low<high):
    print(low,' ',high)
    mid=(low+high)//2
    if (nums[mid]==target):
        flag=True
        index=mid
        print(mid)
        break
    elif (nums[mid]<target):
        low=mid+1
    else:
        high=mid-1
if(flag):
    print(index)
else:
    print("Not found")

