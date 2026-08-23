height = [1, 8, 6, 2, 5, 4, 8, 3, 7]
max_water=0
left=0
right=len(height)-1
while(left<right):
    water_quantity=min(height[left],height[right])*(right-left)
    max_water=max(water_quantity,max_water)
    if(height[left]<height[right]):
        left+=1
    else:
        right-=1
print(max_water)
