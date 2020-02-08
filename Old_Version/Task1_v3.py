# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 13:35:38 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
plt.style.use('seaborn-whitegrid')

#parameter
m=1
n=1
thita=0.14
P=11000000.

# Data For Wuhan
file='Wuhan_Data.csv'
Wuhan_data=pd.read_csv(file,error_bad_lines=False) #1.15-2.4
#Row: 0--S, 1--E, 2--I, 3--R, 4--D 
#Total_person=P=1400w, P=S+E+I+R+D
#Col: Time Series. Dec 1st,2019  -->Feb 18th,2020(X)

# description about population flow, travel restriction considered 
Flow_rate = (np.random.rand(31) * 150 + 150) * 1000
Flow_rate/= P
Flow_rate_= pd.read_csv('Wuhan_Flow.csv',error_bad_lines=False) 
Flow_rate_.drop(['Date','Point','Rate'],axis=1,inplace=True)
Flow_rate=np.concatenate((Flow_rate, 1000*Flow_rate_.Flow/P),axis=0)
Flow_rate_=np.zeros(57)
Flow_rate=np.concatenate((Flow_rate,Flow_rate_),axis=0)
print(Flow_rate)

Wuhan=np.zeros([5,110],dtype=np.float32)
Wuhan[: , 0]=[P, 0., 1., 0., 0.]
for i in range(109):
    Wuhan[0,i+1]=P-Wuhan[1,i]-Wuhan[2,i]-Wuhan[3,i]-Wuhan[4,i]
    if i <= 53:
        b=0.6
    else:
        b=0.3              # Infectious intensity decreases as temperature goes up
    
    h=b*Wuhan[2,i]/P
    if i >= 80:
        h *= 0.25                   # ??? But this is necessary (Maybe we can consider linear decrease since day 67 and then level off)
    elif i >= 67:
        h *= 0.5                    # Most exposers show symptoms and get isolated (Two week after restriction)
    elif i >= 53:
        h *= 0.9                    # Travelling restriction
    elif i >= 31:
        h *= 0.98                   # Notice publicated
        
    if i<=53:
        r=0.05
    else:
        r=0.1
    k=0.035*r
    Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]-m*Wuhan[1,i]*Flow_rate[i]
    Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]-n*Wuhan[2,i]*Flow_rate[i]
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
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan[2,45:66], '--', label = 'Prediction')
plt.legend(loc = 'best')

fig = plt.figure(2)
plt.plot(range(len(Wuhan_NewConf)), Wuhan_NewConf, 'o-', label = 'Newly Confirmed')
plt.plot(range(len(Wuhan_New_Pre)), Wuhan_New_Pre, '--', label = 'Delta Prediction')
plt.legend(loc = 'best')

#fig = plt.figure(3)
#plt.plot(range(len(Wuhan_Add_Pre)), Wuhan_Add_Pre, '--', label = 'Delta Prediction')
#plt.plot(range(len(Wuhan_Add_Pre)), Wuhan[1,44:109] - Wuhan[1, 45:110], label = 'Delta Exposed')
#plt.legend(loc = 'best')

plt.show()
print(Wuhan[1:,45:66])





