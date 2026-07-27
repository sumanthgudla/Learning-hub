words = ["eat", "tea", "tan", "ate", "nat", "bat"]
dict_words={}
for i in words:
    sorted_word_l=sorted(i)
    sorted_word=''.join(sorted_word_l)
    print(sorted_word)
    dict_words.get(sorted_word,[]).append(i)
print(dict_words)