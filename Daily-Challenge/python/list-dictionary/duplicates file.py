files = [
    ("a.txt", "hello"),
    ("b.txt", "world"),
    ("c.txt", "hello"),
    ("d.txt", "python"),
    ("e.txt", "world"),
    ("f.txt", "hello")
]

files_content={}
for key,value in files:
    files_content.setdefault(value,[]).append(key)
print(files_content)