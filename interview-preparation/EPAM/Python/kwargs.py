def create_llm_config(**kwargs):
    keys=['model','temperature','max_tokens']
    res={}
    for key in keys:
        if key in kwargs:
            res[key]=kwargs[key]
    return(res)

res=create_llm_config(model='gpt4',temp=3,max_tokens=700)
print(res)
