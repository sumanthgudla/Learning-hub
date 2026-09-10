arr = [4, 7, 1, 0]  
max=-float('inf')
for idx in range(len(arr)-1,-1,-1):
    if arr[idx]>max:
        print(arr[idx])
        max=arr[idx]
