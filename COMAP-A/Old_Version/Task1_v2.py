# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:00:18 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

#parameter
beta=0.5
m=1
thita=0.14
n=1
P=11000000.
b=0.6
r=0.1
k=0.035*r

# Data For Wuhan
file='Wuhan_Data.csv'
Wuhan_data=pd.read_csv(file,error_bad_lines=False) #1.15-2.4
#Data without person flow
#Row: 0--S, 1--E, 2--I, 3--R, 4--D 
#Total_person=P=1400w, P=S+E+I+R+D
#Col: Time Series. Dec 1st,2019  -->Feb 18th,2020

Wuhan=np.zeros([5,110],dtype=np.float32)
Wuhan[: , 0]=[P, 0., 1., 0., 0.]
for i in range(109):
    Wuhan[0,i+1]=P-Wuhan[1,i]-Wuhan[2,i]-Wuhan[3,i]-Wuhan[4,i]
    if i >= 70:
        b -= 0.004                  # Infectious intensity decreases as temperature goes up
    h=b*Wuhan[2,i]/P
#    if i >= 80:
#        h *= 0.25                   # ??? But this is necessary (Maybe we can consider linear decrease since day 67 and then level off)
#    elif i >= 67:
#        h *= 0.5                    # Most exposers show symptoms and get isolated (Two week after restriction)
#    elif i >= 53:
#        h *= 0.9                    # Travelling restriction
#    elif i >= 31:
#        h *= 0.98                   # Notice publicated
    Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]
    Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]
    Wuhan[3,i+1]=Wuhan[3,i]+r*Wuhan[2,i]
    Wuhan[4,i+1]=Wuhan[4,i]+k*Wuhan[2,i]
Wuhan=Wuhan.astype(np.int)

Wuhan_NewConf = np.zeros((21))      # Daily Confirmed Cases
Wuhan_New_Pre = np.zeros((65))

for i in range(1,len(Wuhan_data.Confirmed)):
    Wuhan_NewConf[i - 1] = Wuhan_data.Confirmed.values[i] - Wuhan_data.Confirmed.values[i - 1]
    
Wuhan_NewConf[20] = 10113 - Wuhan_data.Confirmed.values[20]

for i in range(1,66):
    Wuhan_New_Pre[i - 1] = Wuhan[2, i + 44] - Wuhan[2, i + 43]

fig = plt.figure(1)
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan_data.Confirmed, 'o-', label = 'Confirmed')
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan[2,45:66], 'o-', label = 'Prediction')
plt.legend(loc = 'best')

#fig = plt.figure(2)
#plt.plot(range(len(Wuhan_NewConf)), Wuhan_NewConf, 'o-', label = 'Newly Confirmed')
#plt.plot(range(len(Wuhan_New_Pre)), Wuhan_New_Pre, 'o-', label = 'Delta Prediction')
#plt.legend(loc = 'best')

#fig = plt.figure(3)
#plt.plot(range(len(Wuhan_Add_Pre)), Wuhan_Add_Pre, '--', label = 'Delta Prediction')
#plt.plot(range(len(Wuhan_Add_Pre)), Wuhan[1,44:109] - Wuhan[1, 45:110], label = 'Delta Exposed')
#plt.legend(loc = 'best')

plt.show()
#print(Wuhan[1:,45:66])




