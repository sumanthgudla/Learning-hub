from typing import List


def contains_duplicate(nums: List[int]) -> bool:
    """Return True if any number appears more than once in nums."""
    seen: set[int] = set()
    for num in nums:
        if num in seen:
            return True
        seen.add(num)
    return False


def contains_duplicate_fast(nums: List[int]) -> bool:
    """Return True if nums contains duplicates using set length comparison."""
    return len(set(nums)) != len(nums)


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:
        """LeetCode-style wrapper for duplicate detection."""
        return contains_duplicate(nums)


def main() -> None:
    test_cases = [
        ([1, 2, 3, 1], True),
        ([1, 2, 3, 4], False),
        ([], False),
        ([2, 2, 2, 2], True),
    ]

    for nums, expected in test_cases:
        result = contains_duplicate(nums)
        print(f"contains_duplicate({nums}) -> {result} (expected {expected})")


if __name__ == "__main__":
    main()
