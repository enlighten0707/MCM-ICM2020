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


#Wuhan={}
#Wuhan['P']=1400
#Wuhan['dI']=[] # 1.15~2.3
#Wuhan['dD']=[]
#Wuhan['dR']=[]
#Wuhan['C']=np.array(Wuhan_data.Confirmed).astype(np.float32)
#Wuhan['D']=np.array(Wuhan_data.Death).astype(np.float32)
#Wuhan['R']=np.array(Wuhan_data.Recover).astype(np.float32)
#Wuhan['I']=Wuhan['C']/beta
#Wuhan['F']=[18.64, 18.92, 20.31, 24.32, 23.37, 26.21, 33.87, 37.34, 35.14]#1.15~1.23
#for i in range(12):
#    Wuhan['F'].append(m*random.random())
#for i in range(20):
#    Wuhan['dI'].append(Wuhan['I'][i+1]-Wuhan['I'][i])
#    Wuhan['dD'].append(Wuhan['D'][i+1]-Wuhan['D'][i])
#    Wuhan['dR'].append(Wuhan['R'][i+1]-Wuhan['R'][i])
#
#Wuhan['E']=[] #1.15-2.3 (19)
#for i in range(19):
#    Wuhan['E'].append(Wuhan['dI'][i]+Wuhan['dD'][i]+Wuhan['dR'][i]+n*Wuhan['I'][i]*Wuhan['F'][i]/Wuhan['P'])
#Wuhan['E']=np.array(Wuhan['E'])/thita
#
#Wuhan['h*S']=[] #1.15-2.3 (19)
#for i in range(18):
#    Wuhan['h*S'].append(Wuhan['E'][i+1]-Wuhan['E'][i]+thita*Wuhan['E'][i]+n*Wuhan['E'][i]*Wuhan['F'][i]/Wuhan['P'])
#
#print(Wuhan['h*S'])

#parameter
beta=0.5
m=1
thita=0.14
n=1
P=14000000.
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

Wuhan=np.zeros([5,80],dtype=np.float32)
Wuhan[: , 0]=[P, 0., 1., 0., 0.]
for i in range(79):
    Wuhan[0,i+1]=P-Wuhan[1,i]-Wuhan[2,i]-Wuhan[3,i]-Wuhan[4,i]
    h=b*Wuhan[2,i]/P
    Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]
    Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]
    Wuhan[3,i+1]=Wuhan[3,i]+r*Wuhan[2,i]
    Wuhan[4,i+1]=Wuhan[4,i]+k*Wuhan[2,i]
Wuhan=Wuhan.astype(np.int)

fig = plt.figure()
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan_data.Confirmed, '-')
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan[2,45:66], '--')
plt.show()
print(Wuhan)





