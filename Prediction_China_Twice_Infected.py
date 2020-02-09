# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:56:18 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import generate_province_data as prov

Date_List=['0115','0116','0117','0118','0119','0120','0121','0122','0123','0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203','0204']
#parameter
m=1
n=1
thita=0.14
P=11000000.
b=0.6
gama=0.75

# Data For Wuhan
file='./Data/Wuhan_Data.csv'
Wuhan_data=pd.read_csv(file,error_bad_lines=False) #1.15-2.4
#Row: 0--S, 1--E, 2--I, 3--R, 4--D 
#Total_person=P=1400w, P=S+E+I+R+D
#Col: Time Series. Dec 1st,2019  -->Feb 18th,2020(X)

# description about population flow, travel restriction considered 
data=pd.read_csv('./Data/Flow_Rate_Data.csv',error_bad_lines=False)
Flow_rate=data.Flow_rate
Wuhan=np.zeros([5,120],dtype=np.float32)
Wuhan[: , 0]=[P, 0., 1., 0., 0.]
for i in range(119):
    Wuhan[0,i+1]=P-Wuhan[1,i]-Wuhan[2,i]-Wuhan[3,i]-Wuhan[4,i]
    if i >= 67 and i <= 80:
        b -= 0.04                  # Infectious intensity decreases as temperature goes up
    
    if i >= 67 and i <= 80:
        gama = min(1.0, gama+0.015) 
        
    h=b*gama*Wuhan[2,i]/P
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
#    else:
#        r+=0.005
        
    k=0.035*r
    Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]-m*Wuhan[1,i]*Flow_rate[i]
    Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]-n*Wuhan[2,i]*Flow_rate[i]
    Wuhan[3,i+1]=Wuhan[3,i]+r*Wuhan[2,i]
    Wuhan[4,i+1]=Wuhan[4,i]+k*Wuhan[2,i]
Wuhan=Wuhan.astype(np.int)

Wuhan_NewConf = np.zeros((21))      # Daily Confirmed Cases
Wuhan_New_Pre = np.zeros((75))

for i in range(1,len(Wuhan_data.Confirmed)):
    Wuhan_NewConf[i - 1] = Wuhan_data.Confirmed.values[i] - Wuhan_data.Confirmed.values[i - 1]
    
Wuhan_NewConf[20] = 10113 - Wuhan_data.Confirmed.values[20]

for i in range(1,76):
    Wuhan_New_Pre[i - 1] = Wuhan[2, i + 44] - Wuhan[2, i + 43]

#Data for Hubei
p=59000000-P
alpha=0.67
m=1
n=1
thita=0.14
P=11000000.
b=0.6
gama=0.75

Hubei=np.zeros([5,120],dtype=np.float32)
Hubei[: , 0]=[p, 0., 0., 0., 0.]
for i in range(119):
    Hubei[0,i+1]=p-Hubei[1,i]-Hubei[2,i]-Hubei[3,i]-Hubei[4,i]
    
    if i >= 67 and i <= 80 :
        b -= 0.04   
    if i >= 67 and i <= 80:
        gama = min(1.0, gama+0.015) 
        
    h=gama*b*Hubei[2,i]/p
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
#    else:
#        r+=0.005
        
    k=0.035*r
    Hubei[1,i+1]=Hubei[1,i]+ h*Hubei[0,i]- thita*Hubei[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
    Hubei[2,i+1]=Hubei[2,i]+ thita*Hubei[1,i]- r*Hubei[2,i]- k*Hubei[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
    Hubei[3,i+1]=Hubei[3,i]+r*Hubei[2,i]
    Hubei[4,i+1]=Hubei[4,i]+k*Hubei[2,i]
Hubei=Hubei.astype(np.int)
Hubei[:,:]+=Wuhan[:,:]

file='./Data/Hubei_Data.csv'
Hubei_data=pd.read_csv(file,error_bad_lines=False) #1.20-2.4


#Other Province,Hubei excluded
China_Total_Pre=np.zeros([5,120],dtype=np.float32)
China_Total_Pre=Hubei
ShowProvince=['Beijing','Shanghai','Guangdong','Zhejiang','Henan','Hunan','Jiangxi','Anhui']
# Adjust the pupolation flow
High_Province=['Gansu','Qinghai','Hainan','Shanghai','Yunnan','Tianjin']
Far_High_Province=['Shanghai']
Low_Province=['Sichuan','Jiangxi','Guangdong','Xinjiang','Hunan','Beijing','Anhui','Shandong','Liaoning','Guangxi','Chongqing','Jiangsu','Hebei','Zhejiang','Heilongjiang','Sichuan','Jiangxi','Fujian']
Far_Low_Province=['Sichuan','Jiangxi','Guangdong','Xinjiang','Zhejiang','Fujian','Liaoning','Anhui']
for j in range(34):
    Province=prov.Province[j]
    if(prov.Province[j]=='Hubei' or prov.Province[j]=='Hong Kong' or prov.Province[j]=='Macau' or prov.Province[j]=='Taiwan' or prov.Province[j]=='Tibet'):
        continue
    p    =prov.Population[j] * 10000
    alpha=prov.FlowRatio[j]/100
    if Province=='Guangxi':
        alpha=0.85/100.
    if Province=='Hunan':
        alpha=3.52/100.
#        
#    if Province=='Tibet':
#        alpha/=10
    if Province in High_Province:
        alpha/=3
    if Province in Far_High_Province:
        alpha/=2
    if Province in Low_Province:
        alpha*=3
    if Province in Far_Low_Province:
        alpha*=2
    if Province =='Guangdong':
        alpha*=11
    if Province == 'Zhejiang':
        alpha*=5
    if Province == 'Liaoning' or Province =='Jiangxi'or Province =='Fujian' or Province=='Jiangxi' or Province=='Shaanxi':
        alpha*=2
    if Province == 'Shanghai':
        alpha/=5    
    m=1
    n=1
    thita=0.14
    b=0.6
    gama=0.75
    Place=np.zeros([5,120],dtype=np.float32)
    Place[: , 0]=[p, 0., 0., 0., 0.]
    
    for i in range(119):
        Place[0,i+1]=p-Place[1,i]-Place[2,i]-Place[3,i]-Place[4,i]
        if i >= 67 and i <= 80:
            b -= 0.04   
        if i >= 67 :
            gama = min(1.0, gama+0.015) 
        
        h=gama*b*Place[2,i]/p
        
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
#        else:
#            r+=0.005
#        
        k=0.035*r
        Place[1,i+1]=Place[1,i]+ h*Place[0,i]- thita*Place[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
        Place[2,i+1]=Place[2,i]+ thita*Place[1,i]- r*Place[2,i]- k*Place[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
        Place[3,i+1]=Place[3,i]+r*Place[2,i]
        Place[4,i+1]=Place[4,i]+k*Place[2,i]
    
    Place=Place.astype(np.int)
    China_Total_Pre+=Place


#Date_List_tmp=['1.22','1.27','2.1','2.6','2.11','2.16','2.21','2.26','3.2','3.7']
#fig = plt.figure()
#plt.plot(range(46), China_Total_Pre[2,52:98], 'o-',label='No Mutation') #1.22->2.20
#plt.xticks(range(0,51,5),Date_List_tmp)
#plt.xlabel('Date')
#plt.ylabel('Infected Cases')
#plt.legend(loc = 'best')
#plt.title('Prediction for Infected in China\n(With Mutation)')
