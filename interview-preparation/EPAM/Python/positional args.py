def total_tokens(*args):
    total = 0

    for token in args:
        if isinstance(token,list):
            total+=sum(token)
        else:
            total += token

    return total

print(total_tokens(100, 200, 300))       # 600
print(total_tokens([100, 200, 300]))     # Should be 600
print(total_tokens(100, [200, 300]))     # Should be 600