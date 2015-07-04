# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 16:30:57 2015

@author: Martin Nguyen
"""
from numpy import random
UnreliableVFtest = 2.8/100
class Examination(object):
    def __init__(self,Attribute,medicalRecords):
        self.Attribute = Attribute
        self.medicalRecords = medicalRecords
    def Ophthalmology(self):
        if random.uniform(0,1) < UnreliableVFtest:
            self.medicalRecords['Diagnosed']=False
        else:
            self.medicalRecords['Diagnosed'] = True 
    