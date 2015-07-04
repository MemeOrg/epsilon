# -*- coding: utf-8 -*-
"""
Created on Sun May 17 16:57:24 2015

@author: Martin Nguyen
"""

class node(object):
    def __init__(self,value, down = None,right = None):
        self.value = value
        self.down = down
        self.right = right