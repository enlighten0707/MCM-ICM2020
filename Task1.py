# -*- coding: utf-8 -*-
"""
Created on Wed Feb  5 14:00:18 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import random

#parameter
beta=0.3
m=1
thita=0.14
n=0.3

# Data For Wuhan
file='Wuhan_Data.csv'
Wuhan_data=pd.read_csv(file,error_bad_lines=False) #1.5-2.4

Wuhan={}
Wuhan['P']=1400
Wuhan['dI']=[] # 1.5~2.3
Wuhan['dD']=[]
Wuhan['dR']=[]
Wuhan['C']=np.array(Wuhan_data.Confirmed).astype(np.float32)
Wuhan['D']=np.array(Wuhan_data.Death).astype(np.float32)
Wuhan['R']=np.array(Wuhan_data.Recover).astype(np.float32)
Wuhan['I']=Wuhan['C']/beta
Wuhan['F']=[186.4, 189.2, 203.1, 243.2, 233.7, 262.1, 338.7, 373.4, 351.4]#1.5~1.23
for i in range(12):
    Wuhan['F'].append(m*random.random())
for i in range(20):
    Wuhan['dI'].append(Wuhan['I'][i+1]-Wuhan['I'][i])
    Wuhan['dD'].append(Wuhan['D'][i+1]-Wuhan['D'][i])
    Wuhan['dR'].append(Wuhan['R'][i+1]-Wuhan['R'][i])

Wuhan['E']=[] #1.15-2.3 (19)
for i in range(19):
    Wuhan['E'].append(Wuhan['dI'][i]+Wuhan['dD'][i]+Wuhan['dR'][i]+n*Wuhan['I'][i]*Wuhan['F'][i]/Wuhan['P'])
Wuhan['E']=np.array(Wuhan['E'])/thita

Wuhan['h*S']=[] #1.15-2.3 (19)
for i in range(18):
    Wuhan['h*S'].append(Wuhan['E'][i+1]-Wuhan['E'][i]+thita*Wuhan['E'][i]+n*Wuhan['E'][i]*Wuhan['F'][i]/Wuhan['P'])

print(Wuhan['h*S'])








