'''
Given two strings s and t, return true if the two strings are anagrams of each other, otherwise return false.

An anagram is a string that contains the exact same characters as another string, but the order of the characters can be different.

brute force approach

1. sort both of them and check in linear fashion both are same
if same return true 
else false


2. to have the frequency of tyhe values using a dictionary or hashet and solve the problem

'''
def is_anagram(s: str, t: str) -> bool:
    """Return True if t is an anagram of s."""
    return sorted(s) == sorted(t)


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """LeetCode-style method signature for anagram checking."""
        return is_anagram(s, t)

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        sol_s={}
        for i,v in enumerate(s):
            if (sol_s.get(v) is None):
                sol_s.setdefault(v,1)
            else:
                sol_s[v]=sol_s.get(v)+1
        sol_t={}
        for i,v in enumerate(t):
            if (sol_t.get(v) is None):
                sol_t.setdefault(v,1)
            else:
                sol_t[v]=sol_t.get(v)+1
        return sol_s==sol_t
        
def main() -> None:
    test_cases = [
        ("anagram", "nagaram", True),
        ("rat", "car", False),
        ("", "", True),
        ("a", "ab", False),
    ]

    for s, t, expected in test_cases:
        result = is_anagram(s, t)
        print(f"is_anagram({s!r}, {t!r}) -> {result} (expected {expected})")


if __name__ == "__main__":
    main()
    