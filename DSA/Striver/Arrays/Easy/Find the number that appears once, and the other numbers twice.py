nums=[4,1,2,1,2]
nums_freq={}
for num in nums:
    nums_freq[num]=nums_freq.get(num,0)+1
for key,value in nums_freq.items():
    if value==1:
        print(key)

#this takes an extra space
xor=0
for num in nums:
    xor=xor^num
print(xor)
