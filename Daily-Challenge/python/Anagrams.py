words = ["eat", "tea", "tan", "ate", "nat", "bat"]
dict_words={}

for word in words:
    sorted_word_list=sorted(word)
    sorted_word=''.join(sorted_word_list)
    dict_words.setdefault(sorted_word,[]).append(word)
print(dict_words)
word_tuples=tuple(dict_words.values())
print(word_tuples)