from typing import List

class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        """Return length of longest consecutive sequence in nums."""
        if not nums:
            return 0

        set_nums = set(nums)
        max_cons = 1

        for num in nums:
            if num - 1 in set_nums:
                continue

            current_num = num
            current_streak = 1

            while current_num + 1 in set_nums:
                current_num += 1
                current_streak += 1

            max_cons = max(max_cons, current_streak)

        return max_cons


def main() -> None:
    solution = Solution()

    examples = [
        [100, 4, 200, 1, 3, 2],
        [0, 3, 7, 2, 5, 8, 4, 6, 0, 1],
        [],
    ]

    for nums in examples:
        print(f"Input: {nums}")
        print(f"Longest consecutive sequence length: {solution.longestConsecutive(nums)}")
        print()


if __name__ == "__main__":
    main()

        