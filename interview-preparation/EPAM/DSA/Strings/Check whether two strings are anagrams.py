from collections import Counter
Input1='listen'
Input2='silent'
ip1_ch=Counter(Input1)
ip2_ch=Counter(Input2)
if(ip1_ch==ip2_ch):
    print("valid anagrams")
else:
    print(False)