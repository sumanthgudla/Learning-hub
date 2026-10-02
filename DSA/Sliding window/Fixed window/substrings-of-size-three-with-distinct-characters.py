s = "xyzzazc"
start=0
substring_list=[]
for i in range(len(s)):
    if(i-start+1>=3):
        first=s[start]
        second=s[start+1]
        last=s[i]
        start+=1
        if(first!=second and second!=last and last!=first):
            substring_list.append(first+second+last)
print(substring_list)


