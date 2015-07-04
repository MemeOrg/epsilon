# -*- coding: utf-8 -*-
"""
Created on Wed May 20 00:50:02 2015

@author: Martin Nguyen
"""

#Generate CSV files in this file
#import csv
#from numpy import random
#def csv_dict_writer(path, fieldnames, data):
#    with open(path, "wb") as out_file:
#        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
#        writer.writeheader()
#        for row in data:
#            writer.writerow(row)
#def csv_dict_reader(file_obj):
#    reader = csv.DictReader(file_obj, delimiter=',')
#    mylist = []
#    for line in reader:
#        mylist.append(line["IOP"])
#        #print(line["last_name"])
#    #print mylist
#if __name__ == "__main__":
#    field_names = "IOP,MD,MDR,Age".split(",")
#    print field_names
#    my_list = []
#    for i in range(3000):
#        IOP = random.normal(28,3)
#        while IOP < 22:
#            IOP = random.normal(28,3)
#        MD = -random.gamma(2,2.5)
#        while MD > -3:
#            MD = - random.gamma(2,2.5)
#        MDR = random.gamma(2,0.014)
#        Age = random.normal(68,5)    
#        inner_dict = dict(zip(field_names, [IOP,MD,MDR,Age]))
#        my_list.append(inner_dict)
#    #print my_list
#    path = "Patients_list.csv"
#    csv_dict_writer(path, field_names, my_list)
#    with open("Patients_list.csv") as f_obj:
#        csv_dict_reader(f_obj)
#==============================================================================
# def initializationAttributes(self):
#         self.Attribute['IOP'] = random.normal(28,3) # need to do truncation later
#         while self.Attribute['IOP'] < 22:
#             self.Attribute['IOP'] = random.normal(28,3)
#         self.Attribute['MD'] = -random.gamma(2,2.5) # need to do truncation later
#         while self.Attribute['MD'] > -3:
#             self.Attribute['MD'] = -random.gamma(2,2.5)
#         self.Attribute['MDR'] = random.gamma(2,0.014)
#         self.Attribute['Age'] = random.normal(68,5)
#==============================================================================
#from Queue import PriorityQueue
#
#q = PriorityQueue(6)
#q.put(5)
#q.put(2)
#q.put(0)
#print q.get()
#q = [1,2,3,2,1,6,8,1,2,4,5]
#q.append(321)
#q.sort()
#for i in q:
#    print i

for i in range(10):
    if i == 3:
        i += 2
        break
else:
    print (i)



#            if i < 5 and self.medicalRecords['CurrentMedicationType'] <> 10 :
#                if self.medicalRecords['TreatmentOverallStatus'] == 'SEorIneffective':
#                    self.medicalRecords['MedicationPath'][i] = 'down'
#                elif self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget':
#                    self.medicalRecords['MedicationPath'][i] = 'right'
#                elif self.medicalRecords['TreatmentOverallStatus'] == 'Normal':
#                    self.medicalRecords['MedicationPath'][i] = 'stop'
#                else:
#                    print("report!")
#                if self.medicalRecords['TreatmentOverallStatus'] == 'SEorIneffective':
#                    tracenode = tracenode.down
#                    self.operations(tracenode)
#                if self.medicalRecords['TreatmentOverallStatus'] == 'ExceedTarget':
#                    tracenode = tracenode.right
#                    self.operations(tracenode)