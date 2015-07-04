# -*- coding: utf-8 -*-
"""
Created on Sun May 31 17:16:26 2015

@author: Martin Nguyen
"""
##Overview: Treatment block to do implant
##Dependencies: numpy; TrabeculectomyClass.py
##Descriptions: Patient IOP will be reassigned once trabeculectomy is indicated in that visit
##              
##              Subsequently, patients will be reevaluated based on IOP target. 
##              If IOP > IOP target, Exit
##              else, continue with no medication
from numpy import random
from TrabeculectomyBlockClass import TrabeculectomyBlock
random.seed(123)
class ImplantBlock(TrabeculectomyBlock):
    def __init__ (self,Attribute,params,medicalRecords):
        self.__init__(self, Attribute,params,medicalRecords)
    def updateImplant(self):
        """
        Interface: 
        After implant is done, nothing is done besides set number of visit
        until IOP > IOP target
        """
        if self.medicalRecords['OnImplant'] == False:
            self.SurgeryImplant()
        else:
            self.SetNumberofVisits()
        #Check whether IOP > IOP target yet. Then evaluate whether to leave the block    
        self.DeterminetoExitImplantblock()
    def SurgeryImplant(self):
        #reassign the IOP based on the normal distribution reported by van Gestel        
        self.Attribute['IOP'] = random.normal(15,0.37)
        self.medicalRecords['ContinueTreatment'] = False
        self.medicalRecords['OnImplant'] = True
        self.medicalRecords['MedicationIntake'] = 0
        self.medicalRecords['CurrentMedicationType'] = 31
        self.medicalRecords['TreatmentOverallStatus'] = 'Normal'
        #nullify any side effect left as patients no longer on medication
        self.params['SideEffect'] = 0
    def DeterminetoExitImplantblock (self):
        if self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget' :
            
            if  self.medicalRecords['MedicationIntake'] < 9:
                self.medicalRecords['ImplantSuccess'] = False
                self.medicalRecords['OnImplant'] = False
                self.medicalRecords['ExitCode'] = True
            else:
                #self.medicalRecords['TreatmentBlock']  = 3
                self.medicalRecords['OnImplant'] = False
                self.medicalRecords['ExitCode'] = True