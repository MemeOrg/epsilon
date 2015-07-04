# -*- coding: utf-8 -*-
"""
Created on Sat May 16 18:03:03 2015

@author: Martin Nguyen
"""
##Overview: Evaluate patients' personal attributes and guide the modification of  
##          medical parameters and records
##Dependencies: MedicationBlockClass.py ; CataractClass.py
##Descriptions: Patient object keep 3 lists of personal (IOP,MD,Cataract,Age etc), 
##              medical parameters (IOPreduction) and medical records (PatientVisits, etc)

##              Patient object calls Doctor object to modify parameters and medical records  
##              Patient itself modify personal list acccording to these parameters and
##              medical records
##              
##              Monitor class (only one for each patient population) is attached to keep
##              track of patient statistics
TimeToVFTest = 11
FirstProgressionTarget = 21.0
SecondProgressionTarget = 18.0
ThirdProgressionTarget = 15.0
AgeNottoSurgery = 85
TimenotSideEffect = 2
from MedicationBlockClass import MedicationBlock
from TrabeculectomyBlockClass import TrabeculectomyBlock
from ImplantBlockClass import ImplantBlock

"""This is the graph plan for the next medication correspoinding to current treatment block"""
GraphPlan = {'A':['B','E'],'B': ['C'],'C':['D','E'],'D':['E'],
             'E':['F','G'],'F':['G'],'G':'Terminal'}
class Doctor(object):
    def __init__(self,name,monitor,Attribute,params,medicalRecords):
        self.PatientAttribute = Attribute
        self.params = params
        self.medicalRecords = medicalRecords
        self.monitor = monitor
        self.name = name
    def ReturnAllDoctorValues (self):
        """Main interface of the class
        1. Set IOP target, if the time for VF comes
        2. Evaluate IOP against target and (possibily) nullfify %side effect
        3. Go to meet doctor
        """
        self.IOPTargetSetting()
        self.IOPandSideEffectEvaluation()
        self.DoctorModule()
        
        
    def IOPTargetSetting(self):
        """Check whether its time for VF test. If yes, reevaluate IOP target"""
        
        if self.params['VFCountdown'] > TimeToVFTest: 
            self.monitor.UpdateVFCountdown(self.name,self.params)
            self.SetCorrectIOPTarget()
            self.medicalRecords['NumberVF'] +=1
    def IOPandSideEffectEvaluation(self):
        """ Compare IOP against target. Change patient overall status accordingly"""
        if self.medicalRecords['MedicationIntake'] > TimenotSideEffect :
            self.params['SideEffect'] = 0
        #If patient's IOP > IOP target, set overall status accordingly 
        #and continue treatment
        if self.PatientAttribute['IOP'] > self.PatientAttribute['IOPTarget']:
            self.medicalRecords['TreatmentOverallStatus'] = 'ExceedTarget'
            self.medicalRecords['ContinueTreatment'] = True
        else:
        #discontinue treatment
            self.medicalRecords['ContinueTreatment'] =False
    def DoctorModule(self):
        """Initialize and/or change treatment block"""
        self.InitializeCorrectTreatment()

        #ExitCode will be returned from one of treatment block.
        #ExitCode == True means either  
        #no more medication left (if in MedicationBlock)
        #or IOP > IOP target in surgeries Block (Trabeculectomy/Implant)
        if self.medicalRecords['ExitCode'] == True:
            self.ChangeTreatmentPlan()
            self.InitializeCorrectTreatment()
            self.medicalRecords['ExitCode'] = False            
        
        self.medicalRecords['PatientVisits'] += 1                 
        
        
        
    def SetCorrectIOPTarget(self):
        """Evaluate for MD progression. Reset IOP target accordingly"""
        #IOP target is reset stepwise if CumulativeMDR is > 2dB
            
        #if no conversion: IOP target = 24
        #conversion occurs: IOP target is set according to progression param
        if self.params['Conversion'] == True:
            if self.params['FirstProgression'] == 1 and self.PatientAttribute['CumulativeMDR'] > 2: 
                self.params['SecondProgression'] =1 
                #Need to reset CumulativeMDR to reflect van Gestel's definition
                self.PatientAttribute['CumulativeMDR'] = 0
            elif self.PatientAttribute['CumulativeMDR'] > 2:
                self.params['FirstProgression'] = 1
                self.PatientAttribute['CumulativeMDR'] = 0
                
            if self.params['FirstProgression'] == 1 and self.params['SecondProgression']  == 1:
                self.PatientAttribute['IOPTarget'] = ThirdProgressionTarget
            elif self.params['FirstProgression'] == 1:
                self.PatientAttribute['IOPTarget'] = SecondProgressionTarget
            else:
                self.PatientAttribute['IOPTarget'] = FirstProgressionTarget
        #Reset VF countdown. Wait till new VF measurement
        self.params['VFCountdown'] = 0
    def InitializeCorrectTreatment(self):
        """
        Initialize correct treatment block according to 
        letter block of self.medicalRecords['TreatmentBlock']
            A,C,E and G: medication blocks
            B and D: trabeculectomy blocks
            F : Implant block
        order: refer to appendix
        """
        if self.medicalRecords['TreatmentBlock'] == 'A': 
            block = MedicationBlock(self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'B':
            block = TrabeculectomyBlock(self.PatientAttribute,self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'C':
            block = MedicationBlock(self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'D':
            block = TrabeculectomyBlock(self.PatientAttribute,self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'E':
            block = MedicationBlock(self.params,self.medicalRecords)
            block.update()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'F': 
            block = ImplantBlock(self.PatientAttribute,self.params,self.medicalRecords)
            block.updateImplant()
            del block
        elif self.medicalRecords['TreatmentBlock'] == 'G':
            block = MedicationBlock(self.params,self.medicalRecords)
            block.update()
            del block
    def ChangeTreatmentPlan(self):
        """Change treatment block to the next treatment block once ExitCode is triggered"""
        """
        Logic: 
            if patient is currently on Surgeries, next treatment is medication
            if patient is currently on C(medication), next treatment is either 
                2nd trabeculectomy(block D) if 1st trabeluctomy succeeded
                or medication(block E) if 1st trabeculectomy failed
            if patient is on medication, surgeries (trabeculectomy or implant)
                only occur if self.PatientAttribute['Age'] < AgeNottoSurgery
                else, go to a different medication block
        """ 
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