from collections import Counter
nums = [1, 1, 1, 2, 2, 3]
k = 2
Counter_nums=Counter(nums)
sorted_nums=sorted(Counter_nums.items(), key=lambda x : x[1],reverse=True)
for num,v in sorted_nums[:k]:
    print(num)