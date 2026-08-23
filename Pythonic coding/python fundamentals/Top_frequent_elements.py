from collections import defaultdict
numbers = [
    1, 3, 2, 1, 4, 3, 1, 2, 3, 5, 2, 3
]

n = 2
frequency=defaultdict(int)
for number in numbers:
    frequency[number]=frequency[number]+1
freq=dict(frequency)
sorted_freq=sorted(freq.items(),key=lambda x: x[1],reverse=True)
for k,v in sorted_freq[:n]:
    print(k)

    