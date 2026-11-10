#1. Create a dictionary of numbers and their squares    
Input=[1, 2, 3, 4, 5]
squares={num:num*num for num in Input}
print(squares)

#2. Create a dictionary containing only even numbers
Input=[1, 2, 3, 4, 5, 6]
even={num:num*num for num in Input if num%2==0}
print(even)

#3. Convert two lists into a dictionary
keys = ['name', 'age', 'city']; values = ['Sam', 26, 'Hyderabad']
dict_values={k:v for k,v in zip(keys,values)}
print(dict_values)

#44. Reverse a dictionary
Input={'a': 1, 'b': 2, 'c': 3}
reverse={v:k for k,v in Input.items()}
print(reverse)

#6. Filter employees earning more than 50,000
Input={'John': 40000, 'Sam': 60000, 'Alex': 80000}
employees={k:v for k,v in Input.items() if v>50000}
print(employees)
#8. Create a dictionary of even/odd classifications
Input=[1, 2, 3, 4, 5]
even_odd={num:'even' if num%2==0 else 'odd'  for num in Input}
print(even_odd)
