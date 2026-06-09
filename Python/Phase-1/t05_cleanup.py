'''Given the messy string below, strip the spaces, convert to lowercase, and replace "bad" with "good". Print the final result.
python'''
text = "  This is a BAD day.  "
print(text.upper())
modified_text=text.replace("BAD","GOOD")
print(modified_text)