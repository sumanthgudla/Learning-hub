cardPoints = [1,2,3,4,5,6,1]
k=3
total_cardpoint=sum(cardPoints)
new_k=len(cardPoints)-k
print(new_k)
sum_cardpoints=0
start=0
min_sum=float('inf')
for end in range(len(cardPoints)):
    sum_cardpoints+=cardPoints[end]
    if end-start+1==new_k:
        min_sum=min(min_sum,sum_cardpoints)
        sum_cardpoints-=cardPoints[start]
        start+=1
print(total_cardpoint-min_sum)

