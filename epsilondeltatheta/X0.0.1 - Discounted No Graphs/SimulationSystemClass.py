# -*- coding: utf-8 -*-
"""
Created on Sat May 23 14:54:43 2015

@author: Martin Nguyen
"""
from __future__ import division
import simpy
import csv
from MonitorClass import Monitor
from PatientClass import Patient
simulationTime = 500
class SimulationSystem(object):
    def __init__ (self,size,file_name):
        self.size = size
        self.file_name = file_name
        self.list_IOP = []
        self.list_MD = []
        self.list_MDR = []
        self.list_Age = []
        self.list_Death = []
        self.list_Gender = []
        self.patientlist = []
        self.monitor = Monitor (self.size)
    def csv_dict_reader(self,file_obj):
        reader = csv.DictReader(file_obj, delimiter=',')
        for line in reader:
            self.list_IOP.append(float(line["IOP"]))
            self.list_MD.append(float(line["MD"]))
            self.list_MDR.append(float(line["MDR"]))
            self.list_Age.append(float(line["Age"]))
            self.list_Death.append(float(line["DeathAge"]))
            self.list_Gender.append(float(line["Gender"]))
    def final_cost_calculate(self):
        i = 0
        for obj in self.patientlist:
            self.monitor.finalCostPatient(i,obj.medicalRecords['NumberTrabeculectomy'],obj.medicalRecords['PatientVisits'],obj.medicalRecords['NumberVF'],obj.medicalRecords['SurgeryCataract'])
            i += 1
    def SystemSimulation (self):
        
        with open(self.file_name) as f_obj:
            self.csv_dict_reader(f_obj)
        env = simpy.Environment()   
        
        for i in range(self.size):
            self.patientlist.append( Patient(env,i,self.monitor,{'IOP':self.list_IOP[i],'MD': self.list_MD[i],'MDR':self.list_MDR[i],'CumulativeMDR': 0,'IOPTarget': 24,'Age':self.list_Age[i], 
            'TrabeculectomyIOP': 0,'Death':self.list_Death[i],'Gender': self.list_Gender[i]}))
        env.run(until = simulationTime)
        self.final_cost_calculate ()

