# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 15:39:08 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 600
plt.rcParams['figure.figsize'] = (6.0, 4.0)

Date_List=['0115','0116','0117','0118','0119','0120','0121','0122','0123','0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203','0204']
#parameter
m=1
n=1
thita=0.14
P=11000000.
b=0.6

# Data For Wuhan
file='./Data/Wuhan_Data.csv'
Wuhan_data=pd.read_csv(file,error_bad_lines=False) #1.15-2.4
#Row: 0--S, 1--E, 2--I, 3--R, 4--D 
#Total_person=P=1400w, P=S+E+I+R+D
#Col: Time Series. Dec 1st,2019  -->Feb 18th,2020(X)

# description about population flow, travel restriction considered 
Wuhan=np.zeros([5,120],dtype=np.float32)
Wuhan[: , 0]=[P, 0., 1., 0., 0.]
for i in range(119):
    Wuhan[0,i+1]=P-Wuhan[1,i]-Wuhan[2,i]-Wuhan[3,i]-Wuhan[4,i]
    if i >= 67 and i <= 80:
        b -= 0.04                  # Infectious intensity decreases as temperature goes up
    
    h=b*0.75*Wuhan[2,i]/P
    
    if i >= 80:
        h *= 0.08                    # ??? But this is necessary (Maybe we can consider linear decrease since day 67 and then level off)
    elif i >= 67:
        h *= 0.36                    # Most exposers show symptoms and get isolated (Two week after restriction)
    elif i >= 53:
        h *= 0.6                    # Travelling restriction
    elif i >= 31:
        h *= 0.98                   # Notice publicated
        
    if i <=31:
        r = 0.005
    elif i <=67 :
        r = 0.01
    else:
        r+=0.005
        
    k=0.035*r
    
    Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]-m*Wuhan[1,i]
    Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]
    Wuhan[3,i+1]=Wuhan[3,i]+r*Wuhan[2,i]
    Wuhan[4,i+1]=Wuhan[4,i]+k*Wuhan[2,i]
Wuhan=Wuhan.astype(np.int)

Date_List_tmp=['1.15','1.19','1.23','1.27','1.31','2.4']
fig = plt.figure(1)
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan_data.Confirmed, 'o-', label = 'True Values')
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan[2,45:66], 'o-', label = 'Predictions')
plt.xticks(range(0,21,4),Date_List_tmp)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend(loc = 'best')
plt.title('Prediction for Infected in Wuhan')