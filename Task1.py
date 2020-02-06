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
m=0.8
n=0.5
thita=0.14
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
Flow_rate = (np.random.rand(80) * 200 + 150) * 1000
Flow_rate/= P
Wuhan=np.zeros([5,80],dtype=np.float32)
Wuhan[: , 0]=[P, 0., 1., 0., 0.]
for i in range(79):
    Wuhan[0,i+1]=P-Wuhan[1,i]-Wuhan[2,i]-Wuhan[3,i]-Wuhan[4,i]
    h=b*Wuhan[2,i]/P
    Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]-m*Wuhan[1,i]*Flow_rate[i]
    Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]-n*Wuhan[2,i]*Flow_rate[i]
    Wuhan[3,i+1]=Wuhan[3,i]+r*Wuhan[2,i]
    Wuhan[4,i+1]=Wuhan[4,i]+k*Wuhan[2,i]
Wuhan=Wuhan.astype(np.int)

fig_Wuhan = plt.figure()
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan_data.Confirmed, '-')
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan[2,45:66], '--')
plt.show()

p=59000000-P
alpha=0.67

Hubei=np.zeros([5,80],dtype=np.float32)
Hubei[: , 0]=[p, 0., 0., 0., 0.]
for i in range(79):
    Hubei[0,i+1]=p-Hubei[1,i]-Hubei[2,i]-Hubei[3,i]-Hubei[4,i]
    h=b*Hubei[2,i]/p
    Hubei[1,i+1]=Hubei[1,i]+ h*Hubei[0,i]- thita*Hubei[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
    Hubei[2,i+1]=Hubei[2,i]+ thita*Hubei[1,i]- r*Hubei[2,i]- k*Hubei[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
    Hubei[3,i+1]=Hubei[3,i]+r*Hubei[2,i]
    Hubei[4,i+1]=Hubei[4,i]+k*Hubei[2,i]
Hubei=Hubei.astype(np.int)
Hubei[:,:]+=Wuhan[:,:]

file='Hubei_Data.csv'
Hubei_data=pd.read_csv(file,error_bad_lines=False) #1.20-2.4

fig_Hubei = plt.figure()
plt.plot(range(len(Hubei_data.Confirmed)), Hubei_data.Confirmed, '-')
plt.plot(range(len(Hubei_data.Confirmed)), Hubei[2,50:66], '--')
plt.show()


