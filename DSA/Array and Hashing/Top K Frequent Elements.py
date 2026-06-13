'''Given an integer array nums and an integer k, return the k most frequent elements within the array.

The test cases are generated such that the answer is always unique.

You may return the output in any order.

Example 1:

Input: nums = [1,2,2,3,3,3], k = 2

Output: [2,3]
Example 2:

Input: nums = [7,7], k = 1

Output: [7]

approach 1:

calcualte the frequency of elements
use sorting to get the top k most freq elements


'''


class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        nums_set={}
        for i in nums:
            nums_set[i]=nums_set.get(i,0)+1
        nums_set=sorted(nums_set,key=lambda x:nums_set[x],reverse=True)
        res=[]
        for i in range(k):
            res.append(nums_set[i])
        return res

