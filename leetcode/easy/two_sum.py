class Solution(object):
    def twoSum(self, nums, target):
        nums_dict = {}
        for i, num in enumerate(nums):
            if num in nums_dict:
                return [nums_dict[num], i]
            else:
                nums_dict[target - num] = i

"""
使用字典存储结果，键为数字，值为数字对应的索引，
时间复杂度为O(n)
"""