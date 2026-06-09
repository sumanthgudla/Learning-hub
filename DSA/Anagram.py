def is_anagram(s: str, t: str) -> bool:
    """Return True if t is an anagram of s."""
    return sorted(s) == sorted(t)


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        """LeetCode-style method signature for anagram checking."""
        return is_anagram(s, t)


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
    