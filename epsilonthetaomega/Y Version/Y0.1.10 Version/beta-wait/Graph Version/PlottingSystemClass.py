# -*- coding: utf-8 -*-
"""
Created on Sat May 23 18:05:45 2015

@author: Martin Nguyen
"""
##Overview: Plotting and tabulate statistics (QALY,Total med cost) for main
##Dependencies: none
##Descriptions: The class will receive the simulation system object and tabulate statistics
##              for plotting
##              It also tabulate average population (QALY, Total med cost) and returns to main
from __future__ import division
numberofPatients = 50
class PlottingSystem(object):
    def __init__(self,plt):
        self.plt = plt
        self.FinalMD = []
        self.InitialMD = []
        self.QALY = []
        self.FinalMedType = []
        self.NumTrabeculectomy = []
    def plot(self,SimulationSystem,order,iteration,masterList):
        """
        args: SimulationSystem(class): the current simulation object for processing results
              order(int):  current number of plotting grids
              iteration(int): current number of simulation populations
              masterList(list): output in format (QALY,Total med cost) to return to main
        descriptions:
              plot procedure/main class interface
        """
        for obj in SimulationSystem.monitor.initiallist:
            self.InitialMD.append(obj['MD'])

        TotalQALY = 0
        TotalCost = 0
        TotalMD = 0
        TotalConversionTime = 0
        TotalConvUnder5 = 0
        TotalConvUnder10 = 0
        TotalConvAbove10 = 0
        TotalnonConv = 0
        OccurenceTrabeculectomy = 0
        Occurence2ndTrabeculectomy = 0
        OccurenceCataractSurgery = 0
        totalSystemTime = 0
        TotalIOPfollow = 0
        nuPatientswithLife = 0
        field_names = "QALY,TotalCost,MD".split(",")
        for obj in SimulationSystem.patientlist:
            self.FinalMD.append(obj.Attribute['MD'])
            self.QALY.append(obj.QALY)
            self.FinalMedType.append(obj.medicalRecords['CurrentMedicationType'])
            self.NumTrabeculectomy.append(obj.medicalRecords['NumberTrabeculectomy'])
            TotalQALY += obj.QALY
            TotalMD += obj.Attribute['MD']
            totalSystemTime += obj.params['CurrentTime']
            TotalConversionTime += obj.params['TimetoConversion']
            if obj.params['TimetoConversion'] <>0 and obj.params['TimetoConversion'] < 5:
                TotalConvUnder5 += 1
            elif obj.params['TimetoConversion'] <>0 and obj.params['TimetoConversion'] < 10:
                TotalConvUnder10 += 1
            elif obj.params['TimetoConversion'] <>0:
                TotalConvAbove10 += 1
            if obj.params['Conversion'] == False:
                TotalnonConv += 1
            if obj.medicalRecords['NumberTrabeculectomy'] == 1:
                OccurenceTrabeculectomy += 1
            elif obj.medicalRecords['NumberTrabeculectomy'] == 2:
                Occurence2ndTrabeculectomy += 1
            if obj.medicalRecords['SurgeryCataract'] > 0:
                OccurenceCataractSurgery += 1 
        for i in SimulationSystem.monitor.TotalCost:
            TotalCost += i
        for i in SimulationSystem.monitor.IOP_list:
            if len(i) <> 0:
                TotalIOPfollow += sum(i)/len(i)
                nuPatientswithLife += 1
        inner_dict = dict(zip(field_names,[TotalQALY/nuPatientswithLife,TotalCost/nuPatientswithLife,TotalMD/nuPatientswithLife]))
        masterList.append(inner_dict)

        print ('CURRENT ITERATION: {}'.format(iteration))
        print ('Average QALY: {}'.format(TotalQALY/nuPatientswithLife))
        print('Average Medical Cost: {}'.format(TotalCost/nuPatientswithLife))
        print ('Average MD: {}'.format(TotalMD/nuPatientswithLife))
        print ('Average Conversion time: {}'.format(TotalConversionTime/nuPatientswithLife))
        print ('Average Under 5 conversion: {}'.format(TotalConvUnder5/nuPatientswithLife))
        print ('Average Under 10 conversion: {}'.format(TotalConvUnder10/nuPatientswithLife))
        print ('Average above 10 conversion: {}'.format(TotalConvAbove10/nuPatientswithLife))
        print ('Average non conv : {}'.format(TotalnonConv/nuPatientswithLife))
        print ('Average 1 trabeculectomy  occurence: {}'.format(OccurenceTrabeculectomy/nuPatientswithLife))
        print ('Average 2 trabeculectomy  occurence: {}'.format(float(Occurence2ndTrabeculectomy/nuPatientswithLife)))
        print ('Average life time: {}'.format(totalSystemTime/nuPatientswithLife))
        print('Average follow IOP: {}'.format(TotalIOPfollow/nuPatientswithLife))
        print ('Average cataract extraction occurence: {}'.format(OccurenceCataractSurgery/nuPatientswithLife))
        print (' ')




#==============================================================================
        """
            Plotting graphs procedures
            Name of graphs are indicated in the self.plt.title
        """
        self.plt.figure(order)
        self.plt.hist(self.InitialMD)
        self.plt.title("Iteration {} :Bar Chart for initial MD values".format(iteration))
        self.plt.xlabel("MD")
        self.plt.ylabel("Number (Counts)")
        order = order + 1
        self.plt.figure(order)
        self.plt.hist(self.FinalMD)
        self.plt.title("Iteration {}: Bar Chart for final MD values".format(iteration))
        self.plt.xlabel("MD")
        self.plt.ylabel("Number (Counts)")
        order = order + 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.IOP_list[i])
        self.plt.title("Iteration {}: IOP Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("IOP level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.MD_list[i])
        self.plt.title("Iteration {}: MD Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("MD level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.IOPTarget_list[i])
        self.plt.title("Iteration {}: IOP Target Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("IOP Target level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.CurrentMed_list[i])
#            print ("Patient {}: List of Medication Progression is {}".format(i,SimulationSystem.monitor.CurrentMed_list[i]))
#            print("Patient {}: List of Final Medication Amount is {}".format(i,SimulationSystem.monitor.Medication_amount[i]))
        self.plt.title("Iteration {}: Current Medication Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Current Medication Number")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.TimeNextVisit_list[i])
        self.plt.title("Iteration {}: Time to Next Visit Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.SideEffect_list[i])
        self.plt.title("Iteration {}: Side Effect Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.MedicationIntake_list[i])
        self.plt.title("Iteration {}: Medication Intake Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Current Medication Amount")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.VFCoutdown_list[i])
        self.plt.title("Iteration {}: VF Countdown Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.ConversionProb_list[i])
        self.plt.title("Iteration {}: Conversion Probability".format(iteration))
        self.plt.xlabel("Year(s)")
        self.plt.ylabel("Probability")
        order = order+1
        self.plt.figure(order)
        self.plt.hist(self.QALY)
        self.plt.title("Iteration {}: QALY distribution".format(iteration))
        self.plt.xlabel("QALY")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(SimulationSystem.monitor.TotalCost)
        self.plt.title("Iteration {}: Distribution of Medical Cost".format(iteration))
        self.plt.xlabel("Dollars")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(self.FinalMedType)
        self.plt.title("Iteration {}: Distribution of Final Medication Type".format(iteration))
        self.plt.xlabel("Final Medication Type")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(self.NumTrabeculectomy)
        self.plt.title("Iteration {}: Distribution of Number of Trabeculectomy".format(iteration))
        self.plt.xlabel("Number of Trabeculectomy")
        self.plt.ylabel("Counts")
        del self.FinalMD[:]
        del self.InitialMD[:]
        del self.QALY[:]
        del self.FinalMedType[:]
        del self.NumTrabeculectomy[:]
#==============================================================================
