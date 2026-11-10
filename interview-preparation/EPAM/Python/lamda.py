#1. Square every number in a list

Input=[1, 2, 3, 4, 5]
square=list(map(lambda x:x*x,Input))
print(square)

#2. Filter numbers greater than 10
Input= [5, 12, 8, 20, 15]
above10=list(filter(lambda x :x>10,Input))
print(above10)

#3. Find even numbers
Input= [1, 2, 3, 4, 5, 6]
Even=filter(lambda x : x%2==0,Input)
print(list(Even))

#4. Sort words by their length
Input=['apple', 'kiwi', 'banana', 'fig']
sorted_words=sorted(Input,key=lambda x : len(x),reverse=True)
print(list(sorted_words))

#5. Sort employees by salary
Input= [('John', 50000), ('Sam', 30000), ('Alex', 70000)]
employees=sorted(Input,key=lambda x : x[1],reverse=True)
print(list(employees))

#6. Find the maximum number
Input= [10, 50, 20, 90, 30]
max_number=max(Input)
print(max_number)