paranthesis='{{([])}}['
stack=[]
is_valid_paranthesis=True
matching_conditions={
    '}':'{',
    ']':'[',
    ')':'('
}
for char in paranthesis:
    if char in matching_conditions.values():
        stack.append(char)
    elif stack and matching_conditions[char]!=stack.pop():
        is_valid_paranthesis=False
        break
    else:
        is_valid_paranthesis=False
        break

if not stack:
    print(is_valid_paranthesis)
else:
    print(False)
