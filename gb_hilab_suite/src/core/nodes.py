# -*- coding: utf-8 -*-
# @Author: 2022 spring interns
# @Date:   2022-2-12
# @Last Modified by:   Muhammad Umair
# @Last Modified time: 2022-08-24 12:07:34

# Standard imports
from typing import List, Any, Dict
#import re, random
#from copy import deepcopy
#from math import floor
from dataclasses import dataclass
#from sympy import N

# Local imports
from gailbot.plugins.plugin import Plugin, Methods, Utt

@dataclass
class Word:
    startTime: int
    endTime: int
    sLabel: str
    text: str


class Node:
    def __init__(self, startTime, endTime, speakerLable, text):
        self.val = Word(startTime, endTime, speakerLable, text)
        self.left = None
        self.right = None

    def inorder(self, vals):
        """
        Appends text of utterance to a list of utterances

        Args:
            vals (List[]): empty list to be populated

        Returns:
            List[Word] in chronological order
        """
        if self.left is not None:
            self.left.inorder(vals)
        if self.val.startTime is not None:
            vals.append(self.val)
        if self.right is not None:
            self.right.inorder(vals)
        return vals

    def inorderChange(self, varDict):
        """
        Traverse the tree using an inorder traversal. Change the marker text
        to the user-desired format.

        Args:
            varDict(Dict[str, str]): contains new text for output
        """
        if self.left is not None:
            self.left.inorderChange(varDict)
        if (self.val.sLabel in varDict.keys()):
            self.val.text = varDict[self.val.sLabel]
        if self.right is not None:
            self.right.inorderChange(varDict)

    def insert(self, root, startTime, endTime, speakerLabel, text) -> None:
        """
        Inserts a node into the BST by its unique start time

        Args:
            root (Node):
            startTime (int): unique start time for node identifier
            endTime (int): end time
            speakerLabel (str): speaker label
            text (str): text

        Returns:
            Node: void, insert the node at the correct position
        """
        if root is None:
            return Node(startTime, endTime, speakerLabel, text)
        else:
            if root.val.startTime == startTime:
                # insert to the right is start time is the same
                newNode = Node(startTime, endTime, speakerLabel, text)
                newNode.left = root.left
                root.left = newNode
            elif root.val.startTime < startTime:
                root.right = self.insert(root.right, startTime, endTime, speakerLabel, text)
            else:
                root.left = self.insert(root.left, startTime, endTime, speakerLabel, text)
        return root

    def search(self, curr, s) -> Word:
        """
        Searches for a word based on its start time

        Args:
            curr (Node): current node of tree
            s (int): unique start time for node identifier

        Returns:
            Word: the Word object in the corresponding/found Node
        """

        if curr is None:
            return None
        else:
            if curr.val.startTime == s:
                return curr.val
            elif curr.val.startTime < s:
                return self.search(curr.right, s)
            else:
                return self.search(curr.left, s)

    def deleteNode(self, root, key):
        """
        Given a binary search tree and a key, this function delete the key
        and returns the new root

        Args:
            root (Node): current node of tree
            key (int): unique start time for node identifier

        Returns:
            root

        sourse: https://www.geeksforgeeks.org/binary-search-tree-set-2-delete/
        """

        # Base Case
        if root is None:
            return root

        # If the key to be deleted
        # is smaller than the root's
        # key then it lies in  left subtree
        if key < root.val.startTime:
            root.left = self.deleteNode(root.left, key)

        # If the kye to be delete
        # is greater than the root's key
        # then it lies in right subtree
        elif(key > root.val.startTime):
            root.right = self.deleteNode(root.right, key)

        # If key is same as root's key, then this is the node
        # to be deleted
        else:
            # Node with only one child or no child
            if root.left is None:
                temp = root.right
                root = None
                return temp

            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Node with two children:
            # Get the inorder successor
            # (smallest in the right subtree)
            temp = self.__minValueNode(root.right)

            # Copy the inorder successor's
            # content to this node
            root.val = temp.val

            # Delete the inorder successor
            root.right = self.deleteNode(root.right, temp.val.startTime)

        return root

    def __minValueNode(self, node):
        """
        Return the node of a given tree with the minimum
        key value found in that tree. Note that the entire
        tree does not need to be searched.

        Credit: https://www.geeksforgeeks.org/binary-search-tree-set-2-delete/

        Args:
            node (Node): current node of tree

        Returns:
            Node: the tree's node with the minimum key value
        """
        current = node

        # loop down to find the leftmost leaf
        while(current.left is not None):
            current = current.left

        return current