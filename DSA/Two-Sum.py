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
