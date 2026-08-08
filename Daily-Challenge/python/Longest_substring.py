word='abcdeabcdf'
last_seen={}
max_length=0
left=0
for right,char in enumerate(word):
    if char in last_seen and last_seen[char]>=left:
        left=last_seen[char]+1
    max_length=max(max_length,right-left+1)
    last_seen[char]=right
    

print(max_length)

    
