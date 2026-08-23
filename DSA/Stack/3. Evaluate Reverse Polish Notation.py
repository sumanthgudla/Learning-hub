tokens = ["2", "1", "+", "3", "*"]
stack1=[]
operators='+-*/'
for token in tokens:
    print(stack1)
    if token not in operators:
        stack1.append(token)
    else:
        if len(stack1)<2:
            print("invalid expression")
            break
        a=int(stack1.pop())
        b=int(stack1.pop())
        if token=='+':
            stack1.append(a+b)
        elif token=='-':
            stack1.append(a-b)
        elif token=='*':
            stack1.append(a*b)
        else:
            stack1.append(a/b)
if(len(stack1)==1):
    print(stack1.pop())
    

