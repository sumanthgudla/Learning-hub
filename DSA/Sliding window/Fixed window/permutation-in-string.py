from collections import Counter
s1='ab'
s2='eidbbaoo'
s1_counter=dict(Counter(s1))
print(s1_counter)
k=len(s1)
s2_counter={}
start=0
for end in range(len(s2)):
    s2_counter[s2[end]]=s2_counter.get(s2[end],0)+1
    if end-start+1==k:
        if(s1_counter==s2_counter):
            print(True)
            break
        if(s2_counter.get(s2[start])==1):
            s2_counter.pop(s2[start])
        else:
            s2_counter[s2[start]]=s2_counter.get(s2[start])-1
        start+=1


