nums=[1,2,3,4,5,6]
product=1
prefix_sum=[]
suffix_sum=[]
for num in nums:
    prefix_sum.append(product)
    product=product*num
product=1
for num in nums[::-1]:
    suffix_sum.append(product)
    product=product*num
suffix_sum=suffix_sum[::-1]
res=[]
for prefix,suffix in zip(prefix_sum,suffix_sum):
    res.append(prefix*suffix)
print(res)
