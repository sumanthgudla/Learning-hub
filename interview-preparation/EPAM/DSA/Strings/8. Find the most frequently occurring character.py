from collections import Counter
input1='success'
input1=dict(Counter(input1))
sorted_input1=sorted(input1.items(),key=lambda x: x[1],reverse=True)
print(sorted_input1[0][0])