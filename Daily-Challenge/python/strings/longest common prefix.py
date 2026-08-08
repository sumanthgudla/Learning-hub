s=["ABC","ABC","ABC"]
first_string=s[0]
res=''
mismatch=False
lagrest_prefix=''
for i in first_string:
    res=res+i
    for j in s:
        if not j.startswith(res):
            lagrest_prefix=res[:len(res)-1]
            mismatch=True
            break
    if mismatch:
        break

if not mismatch:
    print(res)
else:
    print(lagrest_prefix)
