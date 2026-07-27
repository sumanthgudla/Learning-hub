def deep_merge(dict1,dict2,ans=None):
    if ans is None:
        ans={}
    for k,v in dict1.items():
        if k in dict2:
            if type(v) is dict and type(dict2.get(k)) is dict:
                new_ans={}
                deep_merge(v,dict2.get(k),new_ans)
                ans[k]=new_ans
            else:
                ans[k]=dict2[k]
        else:
            ans[k]=v
    for k,v in dict2.items():
        if k not in dict1:
            ans[k]=dict2.get(k)
    return ans

            



if __name__=='__main__':
    dict1 = {
    "a": 1,
    "b": {"x": 10, "y": 20}
    }

    dict2 = {
        "b": {"y": 30, "z": 40},
        "c": 5
    }
    final_ans=deep_merge(dict1,dict2,{})
    print(final_ans)