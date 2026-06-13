from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """Return all unique triplets that sum to zero."""
        nums.sort()
        result = []
        n = len(nums)

        for i in range(n - 2):
            if nums[i] > 0:
                break

            if i > 0 and nums[i] == nums[i - 1]:
                continue

            start = i + 1
            end = n - 1

            while start < end:
                triplet_sum = nums[i] + nums[start] + nums[end]

                if triplet_sum == 0:
                    result.append([nums[i], nums[start], nums[end]])

                    while start < end and nums[start] == nums[start + 1]:
                        start += 1
                    while start < end and nums[end] == nums[end - 1]:
                        end -= 1

                    start += 1
                    end -= 1

                elif triplet_sum < 0:
                    start += 1
                else:
                    end -= 1

        return result


def main() -> None:
    solution = Solution()

    test_cases = [
        [-1, 0, 1, 2, -1, -4],
        [0, 0, 0, 0],
        [-1, -1, 0, 1],
        [-4, -1, 0, 1, 2, 3],
    ]

    for nums in test_cases:
        print(f"Input: {nums}")
        print(f"3Sum result: {solution.threeSum(nums)}")
        print()


if __name__ == "__main__":
    main()
            

        