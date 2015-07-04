# -*- coding: utf-8 -*-
"""
Created on Wed May 20 15:58:54 2015

@author: Martin Nguyen
"""
##Overview: Run this file for the simulation of the project
##Dependencies: PlottingSystemClass.py ; SimulationSystemClass.py
##Descriptions: The program will first pass the correct file name of the records of patients'
##              initial parameters from folder: PatientList. Then it will pass these parameters
##              to sysSimulation (object) to actually run the simulation. plottingsystem is used
##              to receive outputs from the simulation to plot graphs
import csv
import matplotlib.pyplot as plt
#Number of populations for each run
numberPatientPopulation = 1
#Number of graphs plotted for one population
numberofGraphs = 14

def csv_dict_writer(path, fieldnames, data):
    """
    args: path (string): Name of output file
          fieldnames(string): Name of output fields
          data(list): list of outputs from the simulation
    description: output the results in  (QALY,Total Medical Cost) format to path as a .csv file
    """
    with open(path, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
masterListforReplications = []
field_names = "QALY,TotalCost".split(",")


from PlottingSystemClass import PlottingSystem
from SimulationSystemClass import SimulationSystem
if __name__ == "__main__":
    """ Run the simulation for numberPatientPopulation records"""
    plottingsystem = PlottingSystem(plt)
    #order variable is to keep track of the number of plot grids that
    #our system is drawing on
    order = 1
    for i in range(numberPatientPopulation):
        sysSimulation = SimulationSystem(3000,"PatientList/Patients_list_{}.csv".format(i))
        sysSimulation.SystemSimulation()
        plottingsystem.plot(sysSimulation,order,i,masterListforReplications)
        order += (numberofGraphs*1)
        del sysSimulation
    print order
    csv_dict_writer("MList.csv",field_names,masterListforReplications)