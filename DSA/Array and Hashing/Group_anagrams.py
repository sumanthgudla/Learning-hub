'''
1. loop through each of them in a array
check if the current element is same as sorted of the element that we are checking
to not have the same one again keep the visited array

'''

from collections import defaultdict
from typing import List

class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        """Group anagrams together from the input list."""
        groups = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            groups[key].append(s)
        return list(groups.values())


def main() -> None:
    sample_strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
    solution = Solution()
    grouped = solution.groupAnagrams(sample_strs)
    print(f"input={sample_strs}\noutput={grouped}")


if __name__ == "__main__":
    main()
            
