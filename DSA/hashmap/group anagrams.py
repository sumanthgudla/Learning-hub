strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
group_anagrams={}
for word in strs:
    sorted_word=''.join(sorted(word))
    group_anagrams.setdefault(sorted_word,[]).append(word)
print(group_anagrams)
anagram_list=list(group_anagrams.values())
print(anagram_list)
