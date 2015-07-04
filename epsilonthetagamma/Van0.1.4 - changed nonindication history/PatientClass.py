# -*- coding: utf-8 -*-
"""
Created on Wed May 20 01:19:20 2015

@author: Martin Nguyen
"""
##Overview: Individual patient is simulated. Update personal attributes (IOP,MD,Cataract)  
##          according to medical-related attributes
##Dependencies: DoctorClass.py ; CataractClass.py
##Descriptions: Patient object keep 3 lists of personal (IOP,MD,Cataract,Age etc), 
##              medical parameters (IOPreduction) and medical records (PatientVisits, etc)

##              Patient object calls Doctor object to modify parameters and medical records  
##              Patient itself modify personal list acccording to these parameters and
##              medical records
##              
##              Monitor class (only one for each patient population) is attached to keep
##              track of patient statistics

from __future__ import division
from numpy import random
random.seed = 123
from DoctorClass import Doctor
from CataractClass import Cataract
import math
rateDiscount = 0.124/100

class Patient(object):
    def __init__(self,env,name,monitor,Attribute):
        """
        args: env(simpy object): the simulation environment
              name(string): order (ID) of the patient 
              monitor(object): to collect statistics (one for each population)
              Attribute: Patient personal list containing IOP,MD,Age etc. 
                         This list is initialized outside of the class 
        """
        random.seed = 123
        self.name = name
        self.env = env
        self.monitor = monitor
        
        """
        The 3 lists of patients: 
                 self.Attribute: personal list containing IOP,MD,Age etc
                 self.params: medical parameters 
                 self.medicalRecords: medical related records
        """
        self.Attribute = Attribute
        self.params = {'IOPReduction':0,'time_next_visit': 0,'FirstProgression':0,
                       'SecondProgression':0,'VFCountdown':0,
                       'SideEffect':0,
                       'CurrentTime' : 0, 'Conversion': False,'CurrentMonth':0}
        self.medicalRecords = {'PatientVisits': 0, 'MedicationIntake': 0,
                               'MedicationCombination':[0,0,0,0,0],
                               'CurrentMedicationType':0,'TreatmentOverallStatus': 'Normal',
                               'TreatmentBlock': 'A', 'MedicationPath': ['stop','stop','stop','stop','stop'],
                               'IncidenceReaction':[],
                               'ContinueTreatment':True,
                               'NumberVF':0, 
                               'ExitCode': False,
                               'NumberTrabeculectomy':0, 'TrabeculectomySuccess': True,
                               'OnTrabeculectomy': False,
                               'ImplantSuccess': True, 'OnImplant':False,
                               'Cataract' :False,'SurgeryCataract':0,
                               'Diagnosed' : False}
                               
                               
        self.QALY = 0
        #call monitor to keep track of initial attributes 
        monitor.UpdateInitial(self.Attribute)
        #schedule the simpy and prepare to run 
        self.action = env.process(self.runSimulation())
    def  runSimulation (self):
        """
        While patient is still alive: 
            1. Update Current attributes (either monthly or by visit)
            2. Visit doctor
            3. From the current medication, incur side effect
            4. Calculate current cumulative medical costs incurred
            5. Update patient's personal attributes (IOP,MD) from the current medication
            6. Time out(delay)
            7. Check for conversion and cataract
        """
        while (self.Attribute['Age'] < self.Attribute['Death']):
        #1. 
            self.VisitUpdate()
            for i in range(int(float(self.params['time_next_visit']))):
                self.MonthlyUpdate()
        #2. 
            doctor = Doctor(self.Attribute,self.params,self.medicalRecords)
            doctor.ReturnAllDoctorValues()
        #3.
            self.inCurredSideEffect(doctor)
        #4.
            self.monitor.CumulativeCostfromMD(self.name,self.Attribute['MD'],self.Attribute['Age'],self.params['time_next_visit'],self.params['CurrentMonth'])
            self.params['CurrentTime'] += self.params['time_next_visit']/12
            self.params['CurrentMonth'] += self.params['time_next_visit']
        #5.
            self.params_update()
        #6.
            yield self.env.timeout(self.params['time_next_visit'])
        #7.
            self.EvaluateConversion()
            cataract = Cataract(self.Attribute,self.medicalRecords)
            cataract.InitiateCataract()
            del doctor
    def MonthlyUpdate (self):
        """Call monitor to update current attributes by month"""
        self.monitor.UpdateIOPlist(self.name,self.Attribute)
        self.monitor.UpdateMDlist(self.name,self.Attribute)
        self.monitor.UpdateIOPTargetlist(self.name,self.Attribute)
        self.monitor.UpdateVFCountdown(self.name,self.params)
        self.monitor.UpdateSideEffect(self.name,self.params)
        self.monitor.UpdateOverallStatus(self.name,self.medicalRecords)
    def VisitUpdate(self):
        """ Call monitor to update current attributes by visit"""
        self.monitor.UpdateCurrentMedicationType(self.name,self.medicalRecords)
        self.monitor.UpdateMedicationIntake(self.name,self.medicalRecords)
        self.monitor.UpdateTimeNextVisit(self.name,self.params)
    def inCurredSideEffect(self,doctor):
        """Check for Side effect. If yes, immediate visit doctor to change treatment"""
        SideEffect = 0            
        if random.uniform(0,1) < self.params['SideEffect']:
            self.medicalRecords['TreatmentOverallStatus'] = 'SEorIneffective'
            self.medicalRecords['ContinueTreatment'] = True
            #Just call the doctor, no need to check for IOP target
            doctor.DoctorModule()
            self.monitor.UpdateCurrentMedicationType(self.name,self.medicalRecords)
            self.monitor.UpdateOverallStatus(self.name,self.medicalRecords)
            SideEffect = 1
        """ Update current QALY according to side effect"""
        self.QALY += (0.88 - 0.101*SideEffect + 0.011*self.Attribute['MD'] - 0.065*self.medicalRecords['Cataract'])*(self.DiscountRate()/12)
    def params_update(self):
        """Update current IOP and MD based on medical records"""
        #Update MD 
        #If there is conversion, then check whether....
        if self.params['Conversion'] == True:
            #If IOP > 13, then start to decrease MD
            if self.Attribute['IOP'] > 13:
                difference = self.Attribute['MDR'] *(1.13**(self.Attribute['IOP'] - 15.5))*(self.params['time_next_visit'])
            else:
                difference = 0
            #Cumulative MD reduction. To see whether any progression occurred 
            self.Attribute['CumulativeMDR'] = self.Attribute['CumulativeMDR'] + difference
            self.Attribute['MD'] = self.Attribute['MD'] - difference
        self.Attribute['Age'] = self.Attribute['Age'] + self.params['time_next_visit']/12
        #Update IOP based on medication/treatment 
        if  self.medicalRecords['ContinueTreatment'] == False or self.params['IOPReduction'] < 0.001:
            self.onNoMedicationOrTrabeculectomy()
        if self.medicalRecords['ContinueTreatment'] == True :
            self.onMedication()
        #If patient is on LTP only, reduce the effective IOP reduction % overtime 
        if self.medicalRecords['CurrentMedicationType'] == 5 and self.params['IOPReduction'] > 0:
            self.params['IOPReduction'] -= self.params['IOPReduction']*(self.params['time_next_visit']/12)
    def EvaluateConversion (self):
        """Evaluate survival probability to conversion from OHT to POAG"""
        h = (1.26**((self.Attribute['Age']-55)/10))*(1.09**(self.Attribute['IOP'] - 24))*0.02
        prob = 1 - math.exp(-h*self.params['CurrentTime'])
        if random.uniform(0,1) < prob:
            self.params['Conversion'] = True

            
            
            
    
    def onNoMedicationOrTrabeculectomy(self):
        """Update IOP if patient either on no medication or on trabeculectomy"""
        self.params['SideEffect'] = 0
            #IOP is supposed to increase 0.5% annually, without medication
        if  self.medicalRecords['OnTrabeculectomy'] == True or self.medicalRecords['OnImplant'] == True:
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (1.5/100)*(self.params['time_next_visit']/12))
            self.medicalRecords['MedicationIntake'] += 1 
        else:
            self.Attribute['IOP'] = self.Attribute['IOP'] *(1 + (0.5/100)*(self.params['time_next_visit']/12))
        if self.medicalRecords['MedicationIntake'] == 0:
            self.medicalRecords['MedicationIntake'] += 1
    def onMedication(self):
        """Update IOP if patient is on medication"""
        self.medicalRecords['MedicationIntake'] += 1 
        self.Attribute['IOP'] = self.Attribute['IOP'] *(1-self.params['IOPReduction']*(self.params['time_next_visit']/12))
        self.UpdateMedicationCombination()
    
    def UpdateMedicationCombination(self):
        """Check for medication combination (medication block) and udpdate accordingly"""
        if self.medicalRecords['MedicationCombination'][0] == 1:
            self.monitor.Medication1Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][1] == 1:
            self.monitor.Medication2Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][2] == 1:
            self.monitor.Medication3Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][3] == 1:
            self.monitor.Medication4Update(self.name,self.params['time_next_visit'])
        if self.medicalRecords['MedicationCombination'][4] == 1:
            self.monitor.Medication5Update(self.name,self.params['time_next_visit'])
            
            
            
    def DiscountRate(self):
        """Calculate current rate of discount for QALY"""
        i = 2
        discountRate = 1
        while i < self.params['time_next_visit']:            
            discountRate += 1/math.pow(1+rateDiscount,i)
            i += 1
        discount = math.pow(1+rateDiscount,self.params['CurrentMonth'])
        discountRate /= discount
        return discountRate