from collections import Counter
S="programming"
counter_s=Counter(S)
for key,value in counter_s.items():
    if(value>1):
        print(key)
