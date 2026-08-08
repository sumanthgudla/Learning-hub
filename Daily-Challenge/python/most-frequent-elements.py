nums = [1,1,1,2,2,3]
k = 2
freq={}
for num in nums:
    freq[num]=freq.get(num,0)+1
freq=sorted(freq.items(),key=lambda x : x[1],reverse=True)
for key,value in freq[:k]:
    print(key,' ',value)

