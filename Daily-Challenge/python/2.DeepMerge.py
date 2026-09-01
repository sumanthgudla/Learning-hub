def deep_merge(dict1,dict2):
    res=dict1.copy()
    for k,v in dict2.items():
        if k in dict1 and isinstance(v,dict) and isinstance(dict1[k],dict):
            res[k]=deep_merge(dict1[k],v)
        else:
            res[k]=v
    return res
    
            



if __name__=='__main__':
    dict1 = {
    "a": 1,
    "b": {"x": 10, "y": 20}
    }

    dict2 = {
        "b": {"y": 30, "z": 40},
        "c": 5
    }
    final_ans=deep_merge(dict1,dict2)
    print(final_ans)