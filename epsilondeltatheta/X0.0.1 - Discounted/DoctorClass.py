# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:03:03 2015

@author: Martin Nguyen
"""
TimeToVFTest = 11
AgeNottoSurgery = 85
TimenotSideEffect = 2
from TreatmentBlock1Class import TreatmentBlock1
from TreatmentBlock2Class import TreatmentBlock2
from TreatmentBlock3Class import TreatmentBlock3
from ExaminationClass import Examination
from numpy import random 
GraphPlan = {'A':['B','E'],'B': ['C'],'C':['D','E'],'D':['E'],'E':['F','G'],'F':['G'],'G':'Terminal'}
LowerSever = -12.0
UpperMild = -6.0 
class Doctor(object):
    def __init__(self,Attribute,params,medicalRecords):
        self.PatientAttribute = Attribute
        self.params = params
        self.medicalRecords = medicalRecords
#Main Program instructions 
    def ReturnAllDoctorValues (self):
        self.IOPTargetSetting()
        self.IOPandSideEffectEvaluation()
        self.DoctorModule()
        
        
        
        
    def IOPTargetSetting(self):
        if self.params['VFCountdown'] > TimeToVFTest: 
            self.SetCorrectIOPTarget()
            self.medicalRecords['NumberVF'] +=1
        self.params['VFCountdown'] = self.params['VFCountdown'] + self.params['time_next_visit']
    def IOPandSideEffectEvaluation(self):
        if self.medicalRecords['MedicationIntake'] > TimenotSideEffect :
            self.params['SideEffect'] = 0
        if self.PatientAttribute['IOP'] > self.PatientAttribute['IOPTarget']:
            self.medicalRecords['TreatmentOverallStatus'] = 2
            self.medicalRecords['ContinueTreatment'] = True
        else:
            self.medicalRecords['ContinueTreatment'] =False
    def DoctorModule(self):
        self.InitializeCorrectTreatment()
        if self.medicalRecords['ExitCode'] == True:
            self.ChangeTreatmentPlan()
            self.InitializeCorrectTreatment()
            self.medicalRecords['ExitCode'] = False
        self.medicalRecords['PatientVisits'] += 1 
    
    
    
    
    #Deeper level of meaning     
    def SetCorrectIOPTarget(self):
        exam = Examination (self.PatientAttribute, self.medicalRecords)
        exam.Ophthalmology()
        if self.medicalRecords['Diagnosed'] == True :
            if self.params['Conversion'] == True:
                if self.PatientAttribute['MD'] > UpperMild :
                    self.PatientAttribute['IOPTarget'] = int(random.triangular(16,18,21))
                elif self.PatientAttribute['MD'] < LowerSever:
                    self.PatientAttribute['IOPTarget'] = int(random.triangular(10,12,14)) 
                else:
                    self.PatientAttribute['IOPTarget'] =  int(random.triangular(14,16,18))
            else: 
                self.PatientAttribute['IOPTarget'] =  int(random.triangular(18,22,24))
            if self.params['FirstProgression'] == 1 and self.PatientAttribute['CumulativeMDR'] > 2: 
                self.params['SecondProgression'] =1 
                self.PatientAttribute['CumulativeMDR'] = 0
            elif self.PatientAttribute['CumulativeMDR'] > 2:
                self.params['FirstProgression'] = 1
                self.PatientAttribute['CumulativeMDR'] = 0

#        
#        if self.params['FirstProgression'] == 1 and self.params['SecondProgression']  == 1:
#            self.PatientAttribute['IOPTarget'] = ThirdProgressionTarget
#        elif self.params['FirstProgression'] == 1:
#            self.PatientAttribute['IOPTarget'] = SecondProgressionTarget
#        else:
#            self.PatientAttribute['IOPTarget'] = FirstProgressionTarget
#            
        self.params['VFCountdown'] = 0
    
    def InitializeCorrectTreatment(self):
        if self.medicalRecords['TreatmentBlock'] == 'A': 
            block = TreatmentBlock1(self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'B':
            block = TreatmentBlock2(self.PatientAttribute,self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'C':
            block = TreatmentBlock1(self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'D':
            block = TreatmentBlock2(self.PatientAttribute,self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'E':
            block = TreatmentBlock1(self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'F': 
            block = TreatmentBlock3(self.PatientAttribute,self.params,self.medicalRecords)
            block.updateImplant()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'G':
            block = TreatmentBlock1(self.params,self.medicalRecords)
            block.update()
            del block
    def ChangeTreatmentPlan(self):
        key = self.medicalRecords['TreatmentBlock']
        if key == 'B' or key == 'D' or key == 'F':
            self.medicalRecords['TreatmentBlock'] = GraphPlan[key][0]
        elif key == 'C':
            if self.medicalRecords['TrabeculectomySuccess'] == True:
                self.medicalRecords['TreatmentBlock'] = GraphPlan[key][0]
            else:
                self.medicalRecords['TreatmentBlock'] = GraphPlan[key][1]
        else:
            if self.PatientAttribute['Age'] < AgeNottoSurgery: 
                self.medicalRecords['TreatmentBlock'] = GraphPlan[key][0]
            else:
                self.medicalRecords['TreatmentBlock'] = GraphPlan[key][1]