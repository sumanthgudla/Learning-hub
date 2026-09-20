s = "programming"
output=""
set_s=set()
for char in s:
    if char not in set_s:
        output=output+char
    set_s.add(char)
print(output)
