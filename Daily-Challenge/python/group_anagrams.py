words=['abc','cab','ate','eat','tea']
anagrams={}
for i in words:
    sorted_word=''.join(sorted(i))
    anagrams.setdefault(sorted_word,[]).append(i)
print(anagrams)
