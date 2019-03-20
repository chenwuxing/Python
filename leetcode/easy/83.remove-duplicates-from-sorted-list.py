#
# @lc app=leetcode id=83 lang=python3
#
# [83] Remove Duplicates from Sorted List
#
# https://leetcode.com/problems/remove-duplicates-from-sorted-list/description/
#
# algorithms
# Easy (42.02%)
# Total Accepted:    307.4K
# Total Submissions: 731.4K
# Testcase Example:  '[1,1,2]'
#
# Given a sorted linked list, delete all duplicates such that each element
# appear only once.
# 
# Example 1:
# 
# 
# Input: 1->1->2
# Output: 1->2
# 
# 
# Example 2:
# 
# 
# Input: 1->1->2->3->3
# Output: 1->2->3
# 
# 
#
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def deleteDuplicates(self, head):
        if head == None:
            return []
        data = []
        while head != None:
            data.append(head.val)
            head = head.next
        re_dup = set(data)
        re_dup = list(re_dup)
        re_dup = sorted(re_dup)
        first = ListNode(re_dup[0])
        b = first
        for i in range(1,len(re_dup)):
            c = ListNode(re_dup[i])
            first.next = c
            first = c
        return b
        

