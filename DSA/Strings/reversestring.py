Input="AI Engineer"
for i in range(len(Input)-1,-1,-1):
    print(Input[i],end="")

def reverseString(Input):
    Output=""
    for i in range(len(Input)-1,-1,-1):
        Output=Output+Input[i]
    return(Output)
print()
print(reverseString(Input))


low=0
high=len(Input)-1
while(low<high):
    temp=Input[low]
    Input[low]=Input[high]
    Input[high]=temp
    low+=1
    high-=1
print(Input)