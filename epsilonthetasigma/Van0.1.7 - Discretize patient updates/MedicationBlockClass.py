# -*- coding: utf-8 -*-
"""
Created on Sun May 17 14:51:48 2015

@author: Martin Nguyen
"""
##Overview: Assign correct parameters for patients on medication block
##Dependencies: NodeClass.py ; numpy
##
##Parameters: Each patient has a .medicalRecords['MedicationPath'] to indicate his medication
##              history/path
##            The block has a TreatmentTree binary tree of a general form
##              node (value,down = node(value,....),right = node(value,....))
##              that represents the treatment plan for medication in van Gestel's paper
##              node.value is the list of all the correct parameters for this medication block
## Actions:             
##            When patient enters the block, either initialize the first medication 
##              (if not on one yet); or trace to the current medication that he is on
##              by following the path to go down or right on the tree plan
##              
##            Next, based on the .medicalRecords['TreatmentOverallStatus'] 
##              (which is ), patient then
##              directed to the node down or right of his/her current node
##              self.operations(...) is called to assign correct parameters of this current node



#### addition: using a priority queue - in order to add in patients in the correct order 
"""
node.value is of the form
[[parameters of medication IOP reduction], current med type, [parameters side effect] ,[medication combination] ]
"""
from NodeClass import node

from numpy import random
TreatmentTree = node ([ [511,1381] ,1, [10,109] , [1,0,0,0,0] ],
                      node([ [589,1407] ,2, [22,258] , [0,1,0,0,0] ],    
                           node([ [294,1231] ,3, [2,12] ,[0,0,1,0,0] ],
                               node([ [148,559] ,4, [5,17] , [0,0,0,1,0]],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,23,[5,17],[0,0,0,1,1] ])),
                               node([ [148,559] ,21,[5,17] ,  [0,0,1,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,22,[5,17],[0,0,1,1,1] ]))),
                               
                           node([ [294,1231] , 16 , [2,12] , [0,1,0,1,0] ],
                               node([ [148,559] ,17,[5,17] , [0,1,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),  
                                   node([ [763,1480] ,20,[5,17],[0,1,0,1,1] ])),
                               node([ [148,559] ,18,[5,17] , [0,1,1,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,19,[5,17],[0,1,1,1,1] ])))
                           ),
                      node([ [589,1407] , 6 , [22,258] , [1,1,0,0,0] ],
                           node([ [294,1231] , 7 , [2,12] , [1,0,1,0,0] ],
                               node([ [148,559] ,12,[5,17] , [1,0,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,15,[5,17],[1,0,0,1,1] ])),
                               node([ [148,559] ,13,[5,17] , [0,1,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,14,[5,17],[1,0,1,1,1] ]))),
                           node([ [294,1231] , 8 , [2,12] , [1,1,1,0,0] ],
                               node([ [148,559] ,9,[5,17] , [1,1,0,1,0] ],
                                   node([ [763,1480] ,5, 0 , [0,0,0,0,1]]),
                                   node([ [763,1480] ,11,[5,17],[1,1,0,1,1] ])),
                               node([ [148,559] ,10,[5,17] , [1,1,1,0,1] ]))
                           )
                    )
random.seed(123)
class MedicationBlock(object):
    def __init__(self, params,medicalRecords):
        self.params = params
        self.medicalRecords = medicalRecords
    def update (self):
        """interface to update medication block"""
        """
        .update is called whenever patient visit doctor when he is on MedicationBlock
        However, self.DoctorPrescription() is only called when unusual event happens
        """
        # if no medication yet or Side Effect is inccured 
        if self.medicalRecords['CurrentMedicationType'] == 0 or self.medicalRecords['TreatmentOverallStatus'] == 'SEorIneffective':
            self.medicalRecords['ContinueTreatment'] = True
            self.DoctorPrescription()
        
        if self.params['IOPReduction'] < 0.1 and self.medicalRecords['MedicationIntake'] > 1 and self.medicalRecords['ContinueTreatment'] == True:
            self.medicalRecords['TreatmentOverallStatus'] ='SEorIneffective'
            self.DoctorPrescription()
            
        if self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget' and self.medicalRecords['MedicationIntake'] > 1:
            self.medicalRecords['ContinueTreatment'] = True
            self.DoctorPrescription()
            
        self.SetTimeNextVisit()
    def DoctorPrescription(self):
        """Reassign/assign medication to patient when unusual event/no medication yet """
        tracenode  = node(0)
        tracenode = TreatmentTree
        # .medicalRecords['MedicationPath'][0] == 0 means no medication assigned yet
        if self.medicalRecords['MedicationPath'][0] == 'stop':
            #assign first medication and block
            self.medicalRecords['MedicationPath'][0] = 'start'
            self.operations(TreatmentTree)
            self.medicalRecords['TreatmentOverallStatus'] = 'Normal'
            self.medicalRecords['MedicationIntake'] = 0
        else:
            #already on some medication
            i = 1
            #special case (premature exit), if current medication type (before reassigning) 
            #is 10, Exit 
            #because there is no more medication node to take.
            if  self.medicalRecords['CurrentMedicationType'] == 10 and self.params['FirstProgression'] == 1:
                self.medicalRecords['ExitCode'] = True
            #now, trace to the current medication block
            #while not exhaust all medication nodes on the path or not medication type == 10
            while i < 5 and self.medicalRecords['MedicationPath'][i] <> 'stop' and self.medicalRecords['CurrentMedicationType'] <> 10:  
                if self.medicalRecords['MedicationPath'][i] == 'down':
                    tracenode = tracenode.down
                    i = i +1
                elif self.medicalRecords['MedicationPath'][i] == 'right':
                    tracenode = tracenode.right
                    i = i+1
            #if current medication type (before reassigning) is not the terminal node
            #first, trace to the next medication node depending on overall status
            #then reassign .operations(tracenode)
            self.SetCorrectMedicationPath(i,tracenode)
            #if current medication type (before reassigning) is the terminal node
            if i == 5 and self.params['FirstProgression'] == 1:
                self.medicalRecords['ExitCode'] = True
            #Reset status variables
            self.medicalRecords['TreatmentOverallStatus'] = 'Normal'
            self.medicalRecords['MedicationIntake'] = 0
            # If exit code is True then exit the system now. 
            if self.medicalRecords['ExitCode'] == True:
                self.ResetMedicationPath()
    def SetCorrectMedicationPath(self,i,tracenode):
        """Set the correct history of patient depending on current state"""
        if i < 5 and self.medicalRecords['CurrentMedicationType'] <> 10 :
            if self.medicalRecords['TreatmentOverallStatus'] == 'SEorIneffective':
                self.medicalRecords['MedicationPath'][i] = 'down'
            elif self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget':
                self.medicalRecords['MedicationPath'][i] = 'right'
            elif self.medicalRecords['TreatmentOverallStatus'] == 'Normal':
                self.medicalRecords['MedicationPath'][i] = 'stop'
            else:
                print("report!")
                
            if self.medicalRecords['TreatmentOverallStatus'] == 'SEorIneffective':
                tracenode = tracenode.down
                self.operations(tracenode)
            elif self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget':
                tracenode = tracenode.right
                self.operations(tracenode)
            else: 
                print ("report!")        
    def operations(self,tracenode):
        """
        Assign IOP reduction,Current med type, Side Effect and Med combi using
            the values from tree node. 
        """
        for i in self.medicalRecords['IncidenceReaction']:
            if i == tracenode.value[1]:
                tracenode = tracenode.down
                if tracenode == None:
                    self.medicalRecords['ExitCode'] = True
                else: 
                    
                    self.SettingCorrectParameters(tracenode)
                break
        else:
            self.SettingCorrectParameters(tracenode)
    def SetTimeNextVisit(self):
        """Set next time to visit doctor for patients on medication block"""
        if self.medicalRecords['MedicationIntake'] == 0:
            self.params['time_next_visit'] = 3
        else:
            self.params['time_next_visit'] = 6
    
    def SettingCorrectParameters(self,tracenode):
        if self.medicalRecords['TreatmentOverallStatus'] == 'SEorIneffective':
                        (self.medicalRecords['IncidenceReaction']).append(self.medicalRecords['CurrentMedicationType'])
        self.params['IOPReduction'] = random.beta(tracenode.value[0][0],tracenode.value[0][1])
        self.medicalRecords['CurrentMedicationType'] = tracenode.value[1] 
        if self.medicalRecords['CurrentMedicationType'] <> 5:
            self.params['SideEffect'] = random.beta(tracenode.value[2][0],tracenode.value[2][1])
        else:
            self.params['SideEffect'] = 0
        self.medicalRecords['MedicationCombination'] = tracenode.value[3]
    def ResetMedicationPath(self):
        """Before leaving medication block, reset the history"""
        for i in range(5):
            self.medicalRecords['MedicationPath'][i] = 'stop'