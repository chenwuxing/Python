#
# @lc app=leetcode id=21 lang=python3
#
# [21] Merge Two Sorted Lists
#
# https://leetcode.com/problems/merge-two-sorted-lists/description/
#
# algorithms
# Easy (46.13%)
# Total Accepted:    527.3K
# Total Submissions: 1.1M
# Testcase Example:  '[1,2,4]\n[1,3,4]'
#
# Merge two sorted linked lists and return it as a new list. The new list
# should be made by splicing together the nodes of the first two lists.
# 
# Example:
# 
# Input: 1->2->4, 1->3->4
# Output: 1->1->2->3->4->4
# 
# 
#
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

"""
主要是三个指针，p指针不断移动确定下一个元素，在l1和l2中也分别移动虚拟指针比较大小
当一个链表为空时剩下的一个链表就是大的部分
"""

class Solution:
    def mergeTwoLists(self, l1, l2):
        result = ListNode(0)
        p = result
        if not l1 and not l2:
            return None
        while l1 and l2:
            if l1.val < l2.val:
                p.next = l1
                l1 = l1.next
            else:
                p.next = l2
                l2 = l2.next
            p = p.next
        p.next = l1 or l2
        return result.next
    

        

