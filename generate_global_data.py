# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 22:28:09 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 600



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
#print('全球感染人数较多的国家——')
tmp=pd.DataFrame(time_stamp)
#print(tmp)

# Prediction for International Total (China Excluded)
Date_List_tmp=['1.24','1.25','1.26','1.27','1.28','1.29','1.30','1.31','2.1','2.2','2.3']
Global_total=time_stamp['INTERNATIONAL TOTAL']
fig= plt.figure(1)
plt.plot(range(11), Global_total, 'o-',label='Confirmed')
plt.xticks(range(11),Date_List_tmp)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend(loc = 'best')
plt.title('Total Confirmed Cases Outside China')


tmp=[]
tmp.append(10)
for i in range(10):
    tmp.append(Global_total[i+1]-Global_total[i])
plt.plot(range(11), tmp, 'o-',label='Daily_Confirmed')
plt.xticks(range(11),Date_List_tmp)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend(loc = 'best')
plt.savefig('./figure/Global_Total.png',dpi=300)


# Some Country
Global_Pos=['Australia','Germany','Japan','Singapore','South Korea','Thailand']

fig= plt.figure(2)
Date_List=['1.24','1.26','1.28','1.30','2.1','2.3']
#colors = ['#ff9999','#9999ff','#cc1234','#1E8449','#3498DB','#34495E','#6C3483','#283747']
colors = ['#cc1234','#9999ff','#6C3483','#1E8449','#3498DB','#34495E']
plt.stackplot(range(11), time_stamp['Australia'],time_stamp['Germany'],time_stamp['Japan'],time_stamp['Singapore'],time_stamp['South Korea'],time_stamp['Thailand'],colors=colors,alpha=0.9)

for i in range(len(colors)):
	plt.plot([],[],color=colors[i],label=Global_Pos[i],linewidth=5)

plt.legend(loc='upper left')
plt.title('Confirmed Cases in Several Countries')
plt.ylabel('Confirmed Cases')
plt.xlabel('Date')
plt.xlim((0,10))
plt.xticks(range(0,11,2),Date_List)
plt.savefig('./figure/Global_Partial.png')
