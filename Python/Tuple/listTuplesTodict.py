skills=[
    ('sumanth','python'),
    ('Bharath','java'),
    ('sumanth','genai')
]
dict_skills={}
role='sumanth'
for key,value in skills:
    if key in dict_skills:
        dict_skills[key].append(value)
    else:
        dict_skills[key]=[value]
print(dict_skills)