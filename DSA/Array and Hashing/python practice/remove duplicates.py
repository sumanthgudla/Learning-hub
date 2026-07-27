a = [1, 2, 2, 3, 1, 4, 3]
dict_keys=list(dict.fromkeys(a))
print(dict_keys)

seenn=set()
for i in a:
    if i not in seenn:
        seenn.add(i)
noduplicates=list(seenn)
print(noduplicates)