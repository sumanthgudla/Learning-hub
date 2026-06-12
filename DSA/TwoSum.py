from typing import List

class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        """Two-pointer approach for sorted array.

        Returns 1-indexed positions of the two numbers that add up to target.
        """
        start = 0
        end = len(numbers) - 1

        while start < end:
            current_sum = numbers[start] + numbers[end]
            if current_sum == target:
                return [start + 1, end + 1]
            if current_sum < target:
                start += 1
            else:
                end -= 1

        return [-1, -1]

    def twoSumWithSet(self, numbers: List[int], target: int) -> List[int]:
        """Set-based approach for an unsorted array.

        Uses a dictionary to store seen values and their indices while
        checking complements in constant time.
        """
        seen = {}

        for index, value in enumerate(numbers):
            complement = target - value
            if complement in seen:
                return [seen[complement] + 1, index + 1]
            seen[value] = index

        return [-1, -1]


def main() -> None:
    solution = Solution()

    test_cases = [
        {
            "numbers": [2, 7, 11, 15],
            "target": 9,
            "description": "sorted array with two-pointer",
        },
        {
            "numbers": [3, 2, 4],
            "target": 6,
            "description": "unsorted array with set-based approach",
        },
    ]

    for case in test_cases:
        numbers = case["numbers"]
        target = case["target"]
        print(f"Input: {numbers}, target={target}")
        print("twoSum (two-pointer):", solution.twoSum(numbers, target))
        print("twoSumWithSet:", solution.twoSumWithSet(numbers, target))
        print()


if __name__ == "__main__":
    main()

        