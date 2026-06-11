from typing import List


def replace_elements(arr: List[int]) -> List[int]:
    """Return a list where each element is replaced by the greatest element to its right."""
    result = [-1] * len(arr)
    max_right = -1

    for index in range(len(arr) - 1, -1, -1):
        result[index] = max_right
        if arr[index] > max_right:
            max_right = arr[index]

    return result


def replace_elements_in_place(arr: List[int]) -> List[int]:
    """Replace values in-place using a right-to-left scan."""
    max_right = -1

    for index in range(len(arr) - 1, -1, -1):
        current = arr[index]
        arr[index] = max_right

        if current > max_right:
            max_right = current

    return arr


class Solution:
    def replaceElements(self, arr: List[int]) -> List[int]:
        """LeetCode-style wrapper for replacing each value with the greatest value on its right."""
        return replace_elements_in_place(arr)


def main() -> None:
    test_cases = [
        ([17, 18, 5, 4, 6, 1], [18, 6, 6, 6, 1, -1]),
        ([400], [-1]),
        ([1, 2, 3, 4], [4, 4, 4, -1]),
        ([], []),
    ]

    for arr, expected in test_cases:
        result = replace_elements(arr)
        print(f"replace_elements({arr}) -> {result} (expected {expected})")

    for arr, expected in test_cases:
        result = replace_elements_in_place(arr[:])
        print(f"replace_elements_in_place({arr}) -> {result} (expected {expected})")


if __name__ == "__main__":
    main()

