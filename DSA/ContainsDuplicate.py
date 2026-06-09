from typing import List


class Solution:
    def hasDuplicate(self, nums: List[int]) -> bool:
        nums_set = set()
        for i in nums:
            if i not in nums_set:
                nums_set.add(i)
            else:
                return True
        return False


if __name__ == "__main__":
    sample_nums = [1, 2, 3, 1]
    result = Solution().hasDuplicate(sample_nums)
    print(result)