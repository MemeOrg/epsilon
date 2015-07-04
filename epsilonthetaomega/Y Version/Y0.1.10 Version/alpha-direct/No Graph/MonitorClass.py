# -*- coding: utf-8 -*-
"""
Created on Wed May 20 16:32:17 2015

@author: Martin Nguyen
"""
from __future__ import division
import copy 
##Overview: This class is a utility 0bject to collecting statistics of Patient object
##Dependencies: copy ; math
##Descriptions: Contain several methods/procedures to collect the statistics of patients. 
##              called during the waiting event of patient
"""
Below are some medical cost parameters
"""
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
"""Rate for 3%"""
#rateDiscount = 0.24663/100
"""Rate for 4%"""
rateDiscount = 0.3273739782/100
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
        self.ConversionProb_list = [[0 for j in range(0)] for i in range(self.size)]
        self.Medication_amount = [[0,0,0,0,0] for i in range(self.size)]
        self.TotalCost = [0 for i in range(self.size)]
        self.Below15 = [[0,0] for i in range(self.size)]
        self.ProductiveLoss = [[0,0] for i in range(self.size)]
        self.initiallist = []
    def UpdateInitial(self,Attribute = None):
        """Update the initial attributes (IOP,MD,Age etc) of the patients"""
        self.initiallist.append(copy.deepcopy(Attribute))
    def UpdateIOPlist (self,name,Attribute = None):
        """Update the current IOP progress of the patients"""
        self.IOP_list[name].append(Attribute['IOP'])
    def UpdateMDlist (self,name,Attribute = None):
        """Update the current MD progress of the patients"""
        self.MD_list[name].append(Attribute['MD'])
    def UpdateIOPTargetlist (self,name,Attribute = None):
        """Update the current IOP target"""
        self.IOPTarget_list[name].append(Attribute['IOPTarget'])
    def UpdateCurrentMedicationType (self,name,Attribute = None):
        """Update current medication type"""
        self.CurrentMed_list[name].append(Attribute['CurrentMedicationType'])    
    def UpdateTimeNextVisit (self,name,Attribute = None):
        """Next visit update"""
        self.TimeNextVisit_list[name].append(Attribute['time_next_visit'])
    def UpdateSideEffect(self,name,Attribute = None):
        """Side effect update"""
        self.SideEffect_list[name].append(Attribute['SideEffect'])
    def UpdateMedicationIntake(self,name,Attribute = None):
        """Medication intake update"""
        self.MedicationIntake_list[name].append(Attribute['MedicationIntake'])
    def UpdateVFCountdown(self,name,Attribute = None):
        """VF countdown (counter to next VF measurement) update"""
        self.VFCoutdown_list[name].append(Attribute['VFCountdown'])
    def UpdateOverallStatus(self,name,Attribute = None):
        """Current status of patient update"""
        self.TreatmentStatus_list[name].append(Attribute['TreatmentOverallStatus'])
    def UpdateConversionProb(self,name,prob):
        self.ConversionProb_list[name].append(prob)
#########################################################        
    def Medication1Update(self,name,timevisit,currentTime):
        """First type of medication update and count to total costs"""
        self.Medication_amount[name][0] +=1
        self.TotalCost[name] += BBlockerPrice*self.DiscountRate(timevisit,currentTime)
    def Medication2Update(self,name,timevisit,currentTime):
        """Second type of medication update and count to total costs"""
        self.Medication_amount[name][1] += 1
        self.TotalCost[name] += ProstaPrice*self.DiscountRate(timevisit,currentTime)
    def Medication3Update(self,name,timevisit,currentTime):
        """Third type of medication update and count to total costs"""
        self.Medication_amount[name][2] += 1
        self.TotalCost[name] += CarboPrice*self.DiscountRate(timevisit,currentTime)
    def Medication4Update(self,name,timevisit,currentTime):
        """Fourth type of medication update and count to total costs"""
        self.Medication_amount[name][3] += 1
        self.TotalCost[name] += AdrePrice*self.DiscountRate(timevisit,currentTime)
    def Medication5Update(self,name,timevisit,currentTime):
        """LTP update and count to total costs"""
        self.Medication_amount[name][4] += 1
    def CumulativeCostfromMD (self,name,MD,Age,timevisit,currentTime):
        """Medical costs also depend on patients' current MD score"""
        if MD < -20:
            self.TotalCost[name] += (Retirementhome +Nursinghome)*self.DiscountRate(timevisit,currentTime)
            if self.Below15[name][0] == 0:
                self.Below15[name][0] = 1
                self.Below15[name][1] = currentTime
            if Age < 65:
                if self.ProductiveLoss[name][0] == 0:
                    self.ProductiveLoss[name][0] = 1
                    self.ProductiveLoss[name][1] = currentTime
        elif MD < -15:
            self.TotalCost[name] += (Familyhelp +Homecaregroom)*self.DiscountRate(timevisit,currentTime)
            if self.Below15[name][0] == 0:
                self.Below15[name][0] = 1
                self.Below15[name][1] = currentTime
            if Age < 65:
                if self.ProductiveLoss[name][0] == 0:
                    self.ProductiveLoss[name][0] = 1
                    self.ProductiveLoss[name][1] = currentTime
        elif MD < -10:
            self.TotalCost[name] += (Householdhelp+Homecarenurse)*self.DiscountRate(timevisit,currentTime)
        elif MD < -5:
            self.TotalCost[name] += (Informalcare)*self.DiscountRate(timevisit,currentTime)
    def finalCostPatient (self,name,Trabeculectomy,Visits,VF,Cataract):
        """final cost computation"""
        self.TotalCost[name] += self.Below15[name][0]*LowVisionAid *self.DiscountRate(1,self.Below15[name][1])
        self.TotalCost[name] += self.ProductiveLoss[name][0]*ProductiveLoss*self.DiscountRate(1,self.ProductiveLoss[name][1])        
        self.TotalCost[name] += (Trabeculectomy*CostTrabeculectomy + Visits*(6+2+65) )
        self.TotalCost[name] += (VF *VisualFieldTest)
        self.TotalCost[name] += (Cataract*CataractPrice)
    def DiscountRate(self,timevisit,currentTime):
        """Discount rate"""
        i = 2
        discountRate = 1
        discount = math.pow(1+rateDiscount,currentTime)
        while i < timevisit:            
            discountRate += 1/math.pow(1+rateDiscount,i)
            i += 1
        discountRate /= discount
        return discountRate