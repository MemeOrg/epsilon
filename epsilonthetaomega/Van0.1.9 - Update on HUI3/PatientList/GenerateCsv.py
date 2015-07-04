# -*- coding: utf-8 -*-
"""
Created on Wed May 20 00:50:02 2015

@author: Martin Nguyen
"""

#Generate CSV files in this file
import csv
from numpy import random
random.seed(123)
#male_prob = [0.00352,0.00389,0.00426, 0.00464,0.00514,0.00586,0.00625,0.00700,0.00801,0.00857,0.00946,0.01085,0.01184,
#             0.01329,0.01483,0.01633,0.01852,0.02013,0.02293,0.02540,0.02790,0.03136,0.03681,0.04124,0.04624,0.05112,0.05743,0.06489,0.07290,
#             0.08013,0.09210,0.09725,0.10879,0.12338,0.13710,0.14379,0.16263,0.17247,0.18968,0.20338,0.22488,0.23400,0.25564,0.27089,0.29603,
#             0.31900,0.33790,0.35492,0.37804,1.00]
#female_prob = [0.00280,0.00277,0.00330,0.00341,0.00382,0.00411,0.00454,0.00483,0.00530,0.00602,0.00654,0.00678,0.00808,0.00845,0.00895,0.01013,
#               0.01160,0.01231,0.01303,0.01445,0.01677,0.01778,0.02069,0.02330,0.02525,0.02871,0.03278,0.03683,0.04310,0.04363,0.05452,0.06029,
#               0.0669,0.07789,0.08854,0.09733,0.10813,0.12067,0.13391,0.14886,0.16526,0.18138,0.19979,0.21944,0.23855,0.25889,0.28367,0.30608,
#               0.33156,1.00]
male_prob = [0.02790,0.03136,0.03681,0.04124,0.04624,0.05112,0.05743,0.06489,0.07290,
             0.08013,0.09210,0.09725,0.10879,0.12338,0.13710,0.14379,0.16263,0.17247,0.18968,0.20338,0.22488,0.23400,0.25564,0.27089,0.29603,
             0.31900,0.33790,0.35492,0.37804,1.00]
female_prob = [0.01677,0.01778,0.02069,0.02330,0.02525,0.02871,0.03278,0.03683,0.04310,0.04363,0.05452,0.06029,
               0.0669,0.07789,0.08854,0.09733,0.10813,0.12067,0.13391,0.14886,0.16526,0.18138,0.19979,0.21944,0.23855,0.25889,0.28367,0.30608,
               0.33156,1.00]
def csv_dict_writer(path, fieldnames, data):
    with open(path, "wb") as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)
def csv_dict_reader(file_obj):
    reader = csv.DictReader(file_obj, delimiter=',')
    mylist = []
    for line in reader:
        mylist.append(line["IOP"])
        #print(line["last_name"])
    #print mylist
if __name__ == "__main__":
    field_names = "IOP,MD,MDR,Age,DeathAge,Gender".split(",")
    print field_names
    
    #print my_list
    path = "Patients_list.csv"
    for j in range(100):    
        
        my_list = []
        for i in range(3000):
            
            if random.uniform(0,1) < 0.34: 
                gender = 1
            else:
                gender = 0
            i = 0
            if gender == 1:
                while random.uniform(0,1) > male_prob[i]:
                    i += 1
            else:
                while random.uniform(0,1) > female_prob[i]:
                    i += 1
            death_age = (i+71)
            
            IOP = random.normal(28,3)
            while IOP < 22:
                IOP = random.normal(28,3)
            MD = -random.gamma(2,2.5)
            while MD > -3:
                MD = - random.gamma(2,2.5)
            MDR = random.gamma(2,0.014)
            Age = random.normal(68,5)    
            inner_dict = dict(zip(field_names, [IOP,MD,MDR,Age,death_age,gender]))
            my_list.append(inner_dict)
        csv_dict_writer("Patients_list_{}.csv".format(j), field_names, my_list)
    