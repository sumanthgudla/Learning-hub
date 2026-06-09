'''Beginner — p2_t03_string_cleaner.py
Given the messy list of names below, clean each one — strip spaces, fix to title case, and join them all into a single comma-separated string.
'''
names = ["  arjun ", "PRIYA  ", " ravi", "  SNEHA  "]
# expected: "Arjun, Priya, Ravi, Sneha"

cleaned_names = [name.strip().title() for name in names]
print(", ".join(cleaned_names))
