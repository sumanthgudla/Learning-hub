prices = [7,6,4,10,13]
lowest_value=prices[0]
max_profit=0
for num in prices:
    if num<lowest_value:
        lowest_value=num
    max_profit=max(max_profit,num-lowest_value)



print(max_profit)
