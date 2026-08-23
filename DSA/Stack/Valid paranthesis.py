s='([{}])'
stack1=[]
open='({['
isvalidParanethesis=True
for ch in s:
    print(stack1)
    if ch in open:
        stack1.append(ch)
    elif ch==')':
        if(stack1.pop()!='('):
            isvalidParanethesis=False
            break
    elif ch==']':
        if(stack1.pop()!='['):
            isvalidParanethesis=False
            break
    elif ch=='}':
        if(stack1.pop()!='{'):
            isvalidParanethesis=False
            break
    else:
        isvalidParanethesis=False
print(stack1)
if(len(stack1)==0 and isvalidParanethesis):
    print(isvalidParanethesis)
else:
    print(isvalidParanethesis)

