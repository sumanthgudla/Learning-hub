def TraversalJson(json):
    res=[]
    if isinstance(json,dict):
        for key,value in json.items():
            if not isinstance(value,dict):
                print(key,end=':')
            TraversalJson(value) 
    elif isinstance(json,list):
        for value in json:
            TraversalJson(value)
    else:
        print(json)
    
    return res

import json
with open('Nested json.json','r') as f:
    samplejson=json.load(f)
res=TraversalJson(samplejson)
print(res)