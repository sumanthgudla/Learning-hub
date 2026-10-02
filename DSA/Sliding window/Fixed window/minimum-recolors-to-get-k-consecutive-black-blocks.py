blocks = "WBWBBBW"
k = 2
start=0
minimum_recolors=float('inf')
recolors_count=0
for end in range(len(blocks)):
    if blocks[end]=='W':
        recolors_count+=1
    if end-start+1==k:
        minimum_recolors=min(recolors_count,minimum_recolors)
        if(blocks[start]=='W'):
            recolors_count-=1
        start+=1
print(minimum_recolors)

