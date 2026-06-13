'''
Contains Duplicate

Easy
Topics
Company Tags

Hints
Given an integer array nums, return true if any value appears more than once in the array, otherwise return false.
fix 1 by using set , add the elements in a sequence wise and check if any time a element is
found in set then return true
else false if in all iterations element is not found

fix 2 simple logic 
check set_nums=set(list)
check for both set length and nums length if both are same then it does not contain
duplicate else contains duplicate

fix 3 brute force approch 
iterate through element in array and check if that element is present in list 
if found contains duplicate
else does not contain duplicates
'''
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
