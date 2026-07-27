nums=[3, 2, 1, 5, 4]
largest=second=float('-inf')
for num in nums:
    if num>largest:
        second=largest
        largest=num
    elif second<num<<largest:
        second=num
if second==float('-inf'):
    print("no second largest number available")
else:
    print(largest," ",second)