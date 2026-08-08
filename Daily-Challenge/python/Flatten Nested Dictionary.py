def flatten_nested_dict(dictionary,res={},carry_forward_key=''):
    for k,v in dictionary.items():
        if type(v) is dict:
            carry_forward_key=carry_forward_key+k+'.'
            flatten_nested_dict(v,res,carry_forward_key)
            carry_forward_key=carry_forward_key.rstrip(k)
        else:
            carry_forward_key=carry_forward_key+k
            res[carry_forward_key]=v
    return res


if __name__=='__main__':
    dict_values={
    "a": 1,
    "b": {
        "c": 2,
        "d": {
            "e": 3
        }
    }
    }
    res=flatten_nested_dict(dict_values)
    print(res)

