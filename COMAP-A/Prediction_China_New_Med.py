# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 23:10:12 2020

@author: 86150
"""


import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import generate_province_data as prov
import Prediction_China_No_Holiday as No_Holiday
plt.style.use('seaborn-whitegrid')
Date_List=['0115','0116','0117','0118','0119','0120','0121','0122','0123','0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203','0204']

ncolors = len(plt.rcParams['axes.prop_cycle'])
plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 600
#plt.style.use('ggplot')

fig = plt.figure(50,figsize=(8.0,4.0))

Date_dict={}
Date_dict[72]='2.10'
Date_dict[77]='2.15'
Date_dict[82]='2.20'
Date_dict[87]='2.25'
Date_dict[92]='3.1'
Date_dict[97]='3.6'
Date_dict[102]='3.11'

for New_Med_Day in range(72,103,5):
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
    data=pd.read_csv('./Data/Flow_Rate_Data.csv',error_bad_lines=False)
    Flow_rate=data.Flow_rate
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
        elif i <= New_Med_Day:
            r+=0.005
        else:
            r+=0.01
        
            
        k=0.035*r
        Wuhan[1,i+1]=Wuhan[1,i]+h*Wuhan[0,i]-thita*Wuhan[1,i]-m*Wuhan[1,i]*Flow_rate[i]
        Wuhan[2,i+1]=Wuhan[2,i]+thita*Wuhan[1,i]-r*Wuhan[2,i]-k*Wuhan[2,i]-n*Wuhan[2,i]*Flow_rate[i]
        Wuhan[3,i+1]=Wuhan[3,i]+r*Wuhan[2,i]
        Wuhan[4,i+1]=Wuhan[4,i]+k*Wuhan[2,i]
    Wuhan=Wuhan.astype(np.int)
    
    Date_List_tmp=['1.15','1.19','1.23','1.27','1.31','2.4']
    
    #Data for Hubei
    p=59000000-P
    alpha=0.67
    m=1
    n=1
    thita=0.14
    P=11000000.
    b=0.6
    
    Hubei=np.zeros([5,120],dtype=np.float32)
    Hubei[: , 0]=[p, 0., 0., 0., 0.]
    for i in range(119):
        Hubei[0,i+1]=p-Hubei[1,i]-Hubei[2,i]-Hubei[3,i]-Hubei[4,i]
        
        if i >= 67 and i <= 80 :
            b -= 0.04   
            
        h=0.75*b*Hubei[2,i]/p
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
        elif i <= New_Med_Day:
            r+=0.005
        else:
            r+=0.01
            
        k=0.035*r
        Hubei[1,i+1]=Hubei[1,i]+ h*Hubei[0,i]- thita*Hubei[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
        Hubei[2,i+1]=Hubei[2,i]+ thita*Hubei[1,i]- r*Hubei[2,i]- k*Hubei[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
        Hubei[3,i+1]=Hubei[3,i]+r*Hubei[2,i]
        Hubei[4,i+1]=Hubei[4,i]+k*Hubei[2,i]
    Hubei=Hubei.astype(np.int)
    Hubei[:,:]+=Wuhan[:,:]
    #StackProvince['Hubei']=Hubei[2,52:83]
    
    file='./Data/Hubei_Data.csv'
    Hubei_data=pd.read_csv(file,error_bad_lines=False) #1.20-2.4
    
    
    #Other Province,Hubei excluded
    China_Total_Pre=np.zeros([5,120],dtype=np.float32)
    China_Total_Pre=Hubei
    ShowProvince=['Beijing','Shanghai','Guangdong','Zhejiang','Henan','Hunan','Jiangxi','Anhui']
    # Adjust the pupolation flow
    High_Province=['Gansu','Qinghai','Hainan','Shanghai','Yunnan','Tianjin']
    Far_High_Province=['Shanghai']
    Low_Province=['Sichuan','Jiangxi','Guangdong','Xinjiang','Hunan','Beijing','Anhui','Shandong','Guangxi','Jiangsu','Hebei','Zhejiang','Heilongjiang','Sichuan','Jiangxi','Fujian']
    Far_Low_Province=['Sichuan','Jiangxi','Guangdong','Xinjiang','Zhejiang','Fujian','Anhui']
    for j in range(34):
        Province=prov.Province[j]
        if(prov.Province[j]=='Hubei' or prov.Province[j]=='Hong Kong' or prov.Province[j]=='Macau' or prov.Province[j]=='Taiwan' or prov.Province[j]=='Tibet'):
            continue
        p    =prov.Population[j] * 10000
        alpha=prov.FlowRatio[j]/100
        if Province=='Inner Mongolia':
            continue
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
    #    if Province =='Guangdong':
    #        alpha*=5
    #    if Province == 'Zhejiang':
    #        alpha*=5
        if Province =='Fujian' or Province=='Jiangxi' or Province=='Shaanxi':
            alpha*=2
    #    if Province == 'Shanghai':
    #        alpha/=5    
        m=1
        n=1
        thita=0.14
        b=0.6
        Place=np.zeros([5,120],dtype=np.float32)
        Place[: , 0]=[p, 0., 0., 0., 0.]
        
        for i in range(119):
            Place[0,i+1]=p-Place[1,i]-Place[2,i]-Place[3,i]-Place[4,i]
            if i >= 67 and i <= 80:
                b -= 0.04   
            
            h=0.75*b*Place[2,i]/p
            
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
            elif i <= New_Med_Day:
                r+=0.005
            else:
                r+=0.01
            
            k=0.035*r
            
            Place[1,i+1]=Place[1,i]+ h*Place[0,i]- thita*Place[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
            Place[2,i+1]=Place[2,i]+ thita*Place[1,i]- r*Place[2,i]- k*Place[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
            Place[3,i+1]=Place[3,i]+r*Place[2,i]
            Place[4,i+1]=Place[4,i]+k*Place[2,i]
        
        Place=Place.astype(np.int)
        China_Total_Pre+=Place
        Date_List_tmp=['1.22','1.27','2.1','2.6','2.11','2.16','2.21']
        
       
    
    China_Total_No_Holiday=No_Holiday.China_Total_Pre
    Date_List_tmp=['1.22','1.27','2.1','2.6','2.11','2.16','2.21','2.26','3.2','3.7','3.12','3.17','3.22','3.27']
    
    plt.plot(range(66), China_Total_Pre[2,52:118], 'o-',label='From '+Date_dict[New_Med_Day],markersize=3) #1.22->2.20
    plt.xticks(range(0,66,5),Date_List_tmp)
    plt.xlabel('Date')
    plt.ylabel('Confirmed Cases')
    plt.legend(loc = 'best',fontsize=8)
    plt.title('Prediction for Infected in China')

plt.savefig('./figure/Prediction_New_Medicine.png')