# -*- coding: utf-8 -*-
"""
Created on Tue May 19 12:16:36 2015

@author: Martin Nguyen
"""
##Overview: Treatment block to do trabeculectomy
##Dependencies: numpy
##Descriptions: Patient IOP will be reassigned once trabeculectomy is indicated in that visit
##              
##              Subsequently, patients will be reevaluated based on IOP target. 
##              If IOP > IOP target, Exit
##              else, continue with no medication
from numpy import random
random.seed(123)
class TrabeculectomyBlock (object):
    def __init__ (self,Attribute,params,medicalRecords):
        self.Attribute = Attribute
        self.params = params
        self.medicalRecords = medicalRecords
    def update(self):
        """
        Interface: 
        After trabeculectomy is done, nothing is done besides set number of visit
        until IOP > IOP target
        """
        if self.medicalRecords['OnTrabeculectomy'] == False:
            self.SurgeryTE()
        else:
            self.SetNumberofVisits()
        #Check whether IOP > IOP target yet. Then evaluate whether to leave the block    
        self.DeterminetoExitTEblock()
    def SurgeryTE(self):
        #reassign the IOP based on the normal distribution reported by van Gestel
        self.Attribute['IOP'] = random.normal(12.5,0.3)
        self.medicalRecords['ContinueTreatment'] = False
        self.medicalRecords['OnTrabeculectomy'] = True
        self.medicalRecords['MedicationIntake'] = 0
        self.medicalRecords['NumberTrabeculectomy'] +=1
        self.medicalRecords['CurrentMedicationType'] = 30
        self.medicalRecords['TreatmentOverallStatus'] = 'Normal'
        #nullify any side effect left as patients no longer on medication
        self.params['SideEffect'] = 0
    def SetNumberofVisits(self):
        """Evaluate the time to next visits based on look-up table """
        if self.medicalRecords['MedicationIntake'] == 0 or self.medicalRecords['MedicationIntake'] == 1 or self.medicalRecords['MedicationIntake'] == 2 or self.medicalRecords['MedicationIntake'] == 3:
            self.params['time_next_visit'] = 0.1
        elif self.medicalRecords['MedicationIntake'] == 4 or self.medicalRecords['MedicationIntake'] == 5 or self.medicalRecords['MedicationIntake'] == 6:
            self.params['time_next_visit'] = 0.25
        elif self.medicalRecords['MedicationIntake'] == 7 or self.medicalRecords['MedicationIntake'] == 8:
            self.params['time_next_visit'] = 0.5
        elif self.medicalRecords['MedicationIntake'] == 9:
            self.params['time_next_visit'] = 1
        else:
            self.params['time_next_visit'] = 6
    def DeterminetoExitTEblock (self):
        """Check whether patient should leave the trabeculectomy because IOP > IOP target"""
        if self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget' :            
            #if immediate failure after 3 months (< 9 intake)
            if  self.medicalRecords['MedicationIntake'] < 9:
                #Fail trabeculectomy
                self.medicalRecords['TrabeculectomySuccess'] = False
                self.medicalRecords['OnTrabeculectomy'] = False
                self.medicalRecords['ExitCode'] = True
                self.medicalRecords['MedicationIntake'] = 0
            else:
                #Exit without failure/
                self.medicalRecords['OnTrabeculectomy'] = False
                self.medicalRecords['ExitCode'] = True
                self.medicalRecords['MedicationIntake'] = 0