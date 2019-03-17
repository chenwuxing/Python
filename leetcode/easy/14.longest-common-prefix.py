#
# @lc app=leetcode id=14 lang=python3
#
# [14] Longest Common Prefix
#
# https://leetcode.com/problems/longest-common-prefix/description/
#
# algorithms
# Easy (33.09%)
# Total Accepted:    421.6K
# Total Submissions: 1.3M
# Testcase Example:  '["flower","flow","flight"]'
#
# Write a function to find the longest common prefix string amongst an array of
# strings.
# 
# If there is no common prefix, return an empty string "".
# 
# Example 1:
# 
# 
# Input: ["flower","flow","flight"]
# Output: "fl"
# 
# 
# Example 2:
# 
# 
# Input: ["dog","racecar","car"]
# Output: ""
# Explanation: There is no common prefix among the input strings.
# 
# 
# Note:
# 
# All given inputs are in lowercase letters a-z.
# 
#
class Solution:
    def longestCommonPrefix(self, input):
        if len(input) == 0:
            return ''
        elif '' in input:
            return ''
        result  = ''
        data = []
        for i in input:
            data.append(len(i))
        str_len = min(data)
        for j in range(str_len):
            for k in range(1,len(input)):
                if input[k][j] != input[0][j]:
                    return result
            result += input[0][j]
        return result
"""
选定一个基准，让其他的字符串与基准进行比较
"""

        

