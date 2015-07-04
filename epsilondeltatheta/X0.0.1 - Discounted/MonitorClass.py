# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:32:17 2015

@author: Martin Nguyen
"""
from __future__ import division
import copy 


###This class contains major amount of update procedures and economic calculations

BBlockerPrice = 6.0
ProstaPrice = 20.20
CarboPrice = 13.90
AdrePrice = 14.0
Retirementhome = 80.0
Nursinghome = 130.0
Familyhelp = 56.0
Homecaregroom = 103.0
Householdhelp = 37.0
Homecarenurse = 159.0
Informalcare = 20.0
CostTrabeculectomy =1214.0
LowVisionAid = 325.0
ProductiveLoss = 3029.0
VisualFieldTest = 150.0
CataractPrice = 1400
rateDiscount = 0.24663/100
import math
class Monitor(object):
    def __init__(self, size):
        self.size = size
        #self.medicalRecords = [{} for i in range(self.size)]
        self.IOP_list = [[0 for j in range(0)] for i in range(self.size)]
        self.MD_list  = [[0 for j in range(0)] for i in range(self.size)]
        self.IOPTarget_list = [[0 for j in range(0)] for i in range(self.size)]
        self.CurrentMed_list = [[0 for j in range(0)] for i in range(self.size)]
        self.TimeNextVisit_list =[[0 for j in range(0)] for i in range(self.size)]
        self.SideEffect_list = [[0 for j in range(0)] for i in range(self.size)]
        self.MedicationIntake_list = [[0 for j in range(0)] for i in range(self.size)]
        self.VFCoutdown_list = [[0 for j in range(0)] for i in range(self.size)]
        self.TreatmentStatus_list = [[0 for j in range(0)] for i in range(self.size)]        
        self.Medication_amount = [[0,0,0,0,0] for i in range(self.size)]
        self.TotalCost = [0 for i in range(self.size)]
        self.Below15 = [0 for i in range(self.size)]
        self.ProductiveLoss = [0 for i in range(self.size)]
        self.initiallist = []
    def UpdateInitial(self,Attribute = None):
        self.initiallist.append(copy.deepcopy(Attribute))
    def UpdateIOPlist (self,name,Attribute = None):
        self.IOP_list[name].append(Attribute['IOP'])
    def UpdateMDlist (self,name,Attribute = None):
        self.MD_list[name].append(Attribute['MD'])
    def UpdateIOPTargetlist (self,name,Attribute = None):
        self.IOPTarget_list[name].append(Attribute['IOPTarget'])
    def UpdateCurrentMedicationType (self,name,Attribute = None):
        self.CurrentMed_list[name].append(Attribute['CurrentMedicationType'])    
    def UpdateTimeNextVisit (self,name,Attribute = None):
        self.TimeNextVisit_list[name].append(Attribute['time_next_visit'])
    def UpdateSideEffect(self,name,Attribute = None):
        self.SideEffect_list[name].append(Attribute['SideEffect'])
    def UpdateMedicationIntake(self,name,Attribute = None):
        self.MedicationIntake_list[name].append(Attribute['MedicationIntake'])
    def UpdateVFCountdown(self,name,Attribute = None):
        self.VFCoutdown_list[name].append(Attribute['VFCountdown'])
    def UpdateOverallStatus(self,name,Attribute = None):
        self.TreatmentStatus_list[name].append(Attribute['TreatmentOverallStatus'])
#########################################################        
    def Medication1Update(self,name,timevisit):
        self.Medication_amount[name][0] +=1
        self.TotalCost[name] += BBlockerPrice*timevisit
    def Medication2Update(self,name,timevisit):
        self.Medication_amount[name][1] += 1
        self.TotalCost[name] += ProstaPrice*timevisit
    def Medication3Update(self,name,timevisit):
        self.Medication_amount[name][2] += 1
        self.TotalCost[name] += CarboPrice*timevisit
    def Medication4Update(self,name,timevisit):
        self.Medication_amount[name][3] += 1
        self.TotalCost[name] += AdrePrice*timevisit
    def Medication5Update(self,name,timevisit):
        self.Medication_amount[name][4] += 1
    def CumulativeCostfromMD (self,name,MD,Age,timevisit,currentTime):
        if MD < -20:
            self.TotalCost[name] += (Retirementhome +Nursinghome)*self.DiscountRate(timevisit,currentTime)
            self.Below15[name] = 1
            if Age < 65:
                self.ProductiveLoss[name] =1
        elif MD < -15:
            self.TotalCost[name] += (Familyhelp +Homecaregroom)*self.DiscountRate(timevisit,currentTime)
            self.Below15[name] = 1
            if Age < 65:
                self.ProductiveLoss[name] =1
        elif MD < -10:
            self.TotalCost[name] += (Householdhelp+Homecarenurse)*self.DiscountRate(timevisit,currentTime)
        elif MD < -5:
            self.TotalCost[name] += (Informalcare)*self.DiscountRate(timevisit,currentTime)
    def finalCostPatient (self,name,Trabeculectomy,Visits,VF,Cataract):
        self.TotalCost[name] += (Trabeculectomy*CostTrabeculectomy + Visits*(6+2+65) +self.Below15[name]*LowVisionAid +self.ProductiveLoss[name]*ProductiveLoss)
        self.TotalCost[name] += (VF *VisualFieldTest)
        self.TotalCost[name] += (Cataract*CataractPrice)
    def DiscountRate(self,timevisit,currentTime):
        i = 2
        discountRate = 1
        discount = math.pow(1+rateDiscount,currentTime)
        while i < timevisit:            
            discountRate += 1/math.pow(1+rateDiscount,i)
            i += 1
        discountRate /= discount
        return discountRate