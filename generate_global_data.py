# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 22:28:09 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

time_stamp={}

Date_List=['0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203']

for i,date in enumerate(Date_List):
    file='./Global_Data/'+date+'.csv'
    data=pd.read_csv(file,sep='|',error_bad_lines=False)
    data.drop(['deaths','notes','sources'],axis=1,inplace=True)
    
    for j,place in enumerate(data.place):
        if time_stamp.get(place) ==None :
            time_stamp[place]=[]
            for k in range(i):
                time_stamp[place].append(0)
        time_stamp[place].append(data.confirmed_cases[j])

# Less Infected. Neglected.
Global_Neg=['Sri Lanka','Sweden','Russia','India','Spain','UAE','Nepal','Italy','Philippines','Cambodia','Finland','England']
for country in Global_Neg:
    time_stamp.pop(country)
#pd.DataFrame(time_stamp).to_csv('Global_Data.csv')
print('全球感染人数较多的国家——')
tmp=pd.DataFrame(time_stamp)
print(tmp)

# Prediction for International Total (China Excluded)
Global_total=time_stamp['INTERNATIONAL TOTAL']
fig= plt.figure(1)
plt.plot(range(11), Global_total, 'o-',label='Confirmed')
plt.xticks(range(11),Date_List)
plt.legend(loc = 'best')
plt.title('Confirmed Globally')

tmp=[]
tmp.append(10)
for i in range(10):
    tmp.append(Global_total[i+1]-Global_total[i])
plt.plot(range(11), tmp, 'o-',label='Daily_Confirmed')
plt.xticks(range(11),Date_List)
plt.legend(loc = 'best')

# Some Country
Global_Pos=['Australia','Germany','Japan','Singapore','South Korea','Thailand']

fig= plt.figure(2)
for country in Global_Pos:
    plt.plot(range(11), time_stamp[country], 'o-',label=country)
    plt.xticks(range(11),Date_List)
    plt.legend(loc = 'best')
plt.title('Confirmed Globally')