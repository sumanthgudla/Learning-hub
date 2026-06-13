'''Given an array of integers nums and an integer target, return the indices i and j such that nums[i] + nums[j] == target and i != j.

You may assume that every input has exactly one pair of indices i and j that satisfy the condition.

Return the answer with the smaller index first.

brute force approach:

1.check for every item if there is any available elements which meets target
then return true else false

2. to have this fixed need an additional space
while looping check in set if there is an element which has target-currennt element
uf present then two sum is posssible
return the indice

'''
from typing import List

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        """Return indices of the two numbers that add up to target."""
        seen = {}
        for i, value in enumerate(nums):
            complement = target - value
            if complement in seen:
                return [seen[complement], i]
            seen[value] = i
        raise ValueError("No two sum solution")


def main() -> None:
    sample_nums = [2, 7, 11, 15]
    sample_target = 9
    solution = Solution()
    result = solution.twoSum(sample_nums, sample_target)
    print(f"nums={sample_nums}, target={sample_target} -> indices={result}")


if __name__ == "__main__":
    main()
