"""
Container With Most Water

Problem:
Given n non-negative integers representing the heights of vertical lines on
the x-axis, find two lines that together with the x-axis form a container,
such that the container contains the most water. Return the maximum amount of
water it can contain.


I'll create a visual explanation and then walk through the solution approach.

Brute force — try every pair, O(n²):
pythondef maxArea(heights):
    best = 0
    for i in range(len(heights)):
        for j in range(i+1, len(heights)):
            best = max(best, min(heights[i], heights[j]) * (j - i))
    return best
Optimal: two pointers, O(n)
Start with left = 0 and right = n-1 (maximum possible width). At each step:

Compute the area for the current pair.
Move the pointer pointing to the shorter bar inward.

Why this works: the width can only shrink as pointers move inward, so to have any chance of a larger area, 
you need a taller limiting wall. The shorter bar is the bottleneck — keeping it 
and moving the other pointer can never improve the area (width decreases, and the
 limiting height stays the same or gets worse). So you must move past the shorter
  bar to have any hope of increasing the result.

Time complexity: O(n)
Space complexity: O(1)

This file contains a concise implementation plus a small `main()` with
examples so you can run and verify results quickly.
"""

from typing import List


class Solution:
    def maxArea(self, heights: List[int]) -> int:
        """Compute max water container area using two-pointer technique."""
        left, right = 0, len(heights) - 1
        max_area = 0

        while left < right:
            height = min(heights[left], heights[right])
            width = right - left
            area = height * width
            if area > max_area:
                max_area = area

            # Move the pointer at the shorter line inward.
            if heights[left] < heights[right]:
                left += 1
            else:
                right -= 1

        return max_area


def main() -> None:
    solution = Solution()

    examples = [
        [1, 8, 6, 2, 5, 4, 8, 3, 7],  # expected 49 (8*7)
        [1, 1],                       # expected 1
        [4, 3, 2, 1, 4],              # expected 16 (4*4)
        [1, 2, 1],                    # expected 2
    ]

    for heights in examples:
        print(f"heights: {heights}")
        print(f"maxArea: {solution.maxArea(heights)}")
        print()


if __name__ == "__main__":
    main()
        

