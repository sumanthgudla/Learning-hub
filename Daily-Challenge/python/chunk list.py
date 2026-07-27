sentence='Sumanth is a greay person who is working in ps 1'
k=3
list_sentence=list(sentence.split(' '))
n=len(list_sentence)//k
print(n)
for i in range(0,len(list_sentence),n):
    print(list_sentence[i:i+n])
