s = "A man, a plan1, a canal: Panama"
left=0
right=len(s)-1
while(left<right):
    while(not s[left].isalnum()):
          left+=1
    while(not s[right].isalnum()):
              right-=1
    if(s[left].lower()!=s[right].lower()):
           print("not palindrome")
           break
    left+=1
    right-=1
          