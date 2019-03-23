#
# @lc app=leetcode id=205 lang=python3
#
# [205] Isomorphic Strings
#
# https://leetcode.com/problems/isomorphic-strings/description/
#
# algorithms
# Easy (36.83%)
# Total Accepted:    191.2K
# Total Submissions: 518.8K
# Testcase Example:  '"egg"\n"add"'
#
# Given two strings s and t, determine if they are isomorphic.
# 
# Two strings are isomorphic if the characters in s can be replaced to get t.
# 
# All occurrences of a character must be replaced with another character while
# preserving the order of characters. No two characters may map to the same
# character but a character may map to itself.
# 
# Example 1:
# 
# 
# Input: s = "egg", t = "add"
# Output: true
# 
# 
# Example 2:
# 
# 
# Input: s = "foo", t = "bar"
# Output: false
# 
# Example 3:
# 
# 
# Input: s = "paper", t = "title"
# Output: true
# 
# Note:
# You may assume both s and t have the same length.
# 
#
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        length = len(s)
        dict_s = {}
        dict_t = {}
        for i in range(length):
            if s[i] not in dict_s:
                dict_s[s[i]] = [i]
            else:
                dict_s[s[i]].append(i)
            if t[i] not in dict_t:
                dict_t[t[i]] = [i]
            else:
                dict_t[t[i]].append(i)
            if dict_s[s[i]] != dict_t[t[i]]:
                return False
        return True


        

