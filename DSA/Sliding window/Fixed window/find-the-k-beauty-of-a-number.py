num = 430043
nums_str=str(num)
k=2
nums_list=[]
start=0
count=0
for end in range(len(nums_str)):
    if end-start+1==k:
        divisor_num=int(nums_str[start:end+1])
        if(divisor_num!=0 and num%divisor_num==0):
            count+=1
        print(divisor_num)
        start+=1

print(count)
