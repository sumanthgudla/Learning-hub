from typing import List

class Solution:
    def isPalindrome(self, s: str) -> bool:
        """Return True if s is a palindrome considering only alphanumeric characters."""
        start = 0
        end = len(s) - 1

        while start < end:
            while start < end and not s[start].isalnum():
                start += 1
            while start < end and not s[end].isalnum():
                end -= 1

            if s[start].lower() != s[end].lower():
                return False

            start += 1
            end -= 1

        return True


def main() -> None:
    solution = Solution()

    test_strings = [
        "A man, a plan, a canal: Panama",
        "race a car",
        "",
        "No lemon, no melon",
        "Was it a car or a cat I saw?",
    ]

    for text in test_strings:
        print(f"Input: {text}")
        print(f"Is palindrome: {solution.isPalindrome(text)}")
        print()


if __name__ == "__main__":
    main()

        