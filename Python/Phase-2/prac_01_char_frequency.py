text = "hello world python programming"
list_char=list(text)
print(list_char)
count_by_char = {ch: sum(1 for j in list_char if j == ch) for ch in set(list_char)}
dict_char = dict(sorted(count_by_char.items()))
print(dict_char)