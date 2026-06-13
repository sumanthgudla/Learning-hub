from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        """Return array where each element is the product of all other elements."""
        n = len(nums)
        if n == 0:
            return []

        prefix = [1] * n
        suffix = [1] * n

        for i in range(1, n):
            prefix[i] = prefix[i - 1] * nums[i - 1]

        for i in range(n - 2, -1, -1):
            suffix[i] = suffix[i + 1] * nums[i + 1]

        return [prefix[i] * suffix[i] for i in range(n)]


def main() -> None:
    solution = Solution()

    test_cases = [
        [1, 2, 3, 4],
        [4, 5, 1, 8, 2],
        [0, 1, 2, 3],
        [],
    ]

    for nums in test_cases:
        print(f"Input: {nums}")
        print(f"Output: {solution.productExceptSelf(nums)}")
        print()


if __name__ == "__main__":
    main()

        