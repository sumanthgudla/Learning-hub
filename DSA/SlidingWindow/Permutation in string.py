from collections import Counter
s1 = "ab"
s1_counter=Counter(s1)
s2 = "eidbabooo"
s2_counter={}
left=0
right=0
for i in range(len(s1)):
    s2_counter[s2[i]]=s2_counter.get(s2[i],0)+1
left=0
right=len(s1)
while(right<len(s2)):
    s2_counter[s2[right]] = s2_counter.get(s2[right], 0) + 1
    s2_counter[s2[left]]-=1
    if s2_counter[s2[left]]==0:
        del s2_counter[s2[left]]
    right+=1
    left+=1
    print(s2_counter,s1_counter)
    if(s2_counter==s1_counter):
        print("permutation found")
    



    

