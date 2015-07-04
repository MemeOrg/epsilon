# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 17:31:19 2015

@author: Martin Nguyen
"""
from numpy import random 
LowerSever = -12.0
UpperMild = -6.0 
class StableIOP(object):
    def __init__(self,Attribute,params):
        self.Attribute = Attribute
        self.params = params
    def StableSetting (self):
        if self.Attribute['MD'] > UpperMild :
            self.params['time_next_visit'] = int(random.triangular(6,7,12))
        elif self.Attribute['MD'] < LowerSever:
            self.params['time_next_visit'] = int(random.triangular(1,1,4)) 
            
        else:
            self.params['time_next_visit'] =  int(random.triangular(4,4.5,6))
            