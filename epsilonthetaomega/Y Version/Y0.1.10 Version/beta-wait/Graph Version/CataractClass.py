# -*- coding: utf-8 -*-
"""
Created on Mon Jun 15 15:39:36 2015

@author: Martin Nguyen
"""
##Overview: Cataract rate and incidence of the patient is initialized
##Dependencies: numpy
##Descriptions: This will first pass the cataract rate and then evaluate whether to remove cataract
##              if the patient is currently cataract-affected
from numpy import random
cataract_formation = [0.61,2.44,3.67,9.95,18.65,32.16,35.85,20.21]
cataract_formation_female = [1.67,3.01,4.82,14.62,22.46,33.16,35.78,22.14]
random.seed(123)
class Cataract (object):
    def __init__(self,Attribute,medicalRecords):
        self.Attribute = Attribute
        self.medicalRecords = medicalRecords
    def InitiateCataract(self):
        key = int((self.Attribute['Age'] -50)/5)
        cataractRisk = random.triangular(1.5,2.7,4.9)

        if self.medicalRecords['NumberTrabeculectomy'] == 0:
            if self.Attribute['Gender'] == 1:
                if key < 7:
                    RateCataract = (cataract_formation[key]/1000)
                else:
                    RateCataract = (cataract_formation[7]/1000)
            else:
                if key < 7:
                    RateCataract = (cataract_formation_female[key]/1000)
                else:
                    RateCataract = (cataract_formation_female[7]/1000)
        else:
            if self.Attribute['Gender'] == 1:
                if key < 7:
                    RateCataract = (cataract_formation[key]/1000)*cataractRisk
                else:
                    RateCataract = (cataract_formation[7]/1000)*cataractRisk
            else:
                if key < 7:
                    RateCataract = (cataract_formation_female[key]/1000)*cataractRisk
                else:
                    RateCataract = (cataract_formation_female[7]/1000)*cataractRisk
                

        if random.uniform(0,1) <RateCataract:
            self.medicalRecords['Cataract'] = True
        if random.uniform(0,1) < random.beta(123,109) and self.medicalRecords['Cataract'] == True:
            self.medicalRecords['SurgeryCataract'] = 1
            self.medicalRecords['Cataract'] = False
