# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 16:04:45 2020

@author: 86150
"""

import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import generate_province_data as prov
plt.style.use('seaborn-whitegrid')

StackProvince={}
Date_List=['0115','0116','0117','0118','0119','0120','0121','0122','0123','0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203','0204']
#parameter
m=1
n=1
thita=0.14
P=11000000.
b=0.6


# Data For Wuhan
file='Wuhan_Data.csv'
Wuhan_data=pd.read_csv(file,error_bad_lines=False) #1.15-2.4

data=pd.read_csv('./Data/Flow_Rate_Data_No_Geo_Restriction.csv',error_bad_lines=False)
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
    else:
        r+=0.005
        
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

Date_List_tmp=['1.15','1.19','1.23','1.27','1.31','2.4']
fig = plt.figure(1)
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan_data.Confirmed, 'o-', label = 'True Values')
plt.plot(range(len(Wuhan_data.Confirmed)), Wuhan[2,45:66], '+-', label = 'Predictions')
plt.xticks(range(0,21,4),Date_List_tmp)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend(loc = 'best')
plt.title('Prediction for Infected in Wuhan')
plt.savefig('./figure/Wuhan_Comp.png',dpi=300)
#StackProvince['Wuhan']=Wuhan[2,52:83]
#fig = plt.figure(2)
#plt.plot(range(len(Wuhan_NewConf)), Wuhan_NewConf, 'o-', label = 'Newly Confirmed')
#plt.plot(range(len(Wuhan_New_Pre)), Wuhan_New_Pre, '--', label = 'Delta Prediction')
#plt.legend(loc = 'best')


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
    else:
        r+=0.005
        
    k=0.035*r
    Hubei[1,i+1]=Hubei[1,i]+ h*Hubei[0,i]- thita*Hubei[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
    Hubei[2,i+1]=Hubei[2,i]+ thita*Hubei[1,i]- r*Hubei[2,i]- k*Hubei[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
    Hubei[3,i+1]=Hubei[3,i]+r*Hubei[2,i]
    Hubei[4,i+1]=Hubei[4,i]+k*Hubei[2,i]
Hubei=Hubei.astype(np.int)
Hubei[:,:]+=Wuhan[:,:]
#StackProvince['Hubei']=Hubei[2,52:83]

file='Hubei_Data.csv'
Hubei_data=pd.read_csv(file,error_bad_lines=False) #1.20-2.4

Date_List_tmp=['1.20','1.23','1.26','1.29','2.1','2.4']
fig = plt.figure(3)
plt.plot(range(len(Hubei_data.Confirmed)), Hubei_data.Confirmed, 'o-',label='True Values')
plt.plot(range(len(Hubei_data.Confirmed)), Hubei[2,50:66], '+-',label='Predictions')
plt.xticks(range(0,16,3),Date_List_tmp)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.legend(loc = 'best')
plt.title('Prediction for Infected in Hubei')
plt.savefig('./figure/Hubei_Comp.png',dpi=300)

plt.show()

#print(Hubei[1:,50:66])


#Other Province,Hubei excluded

China_Total_Pre=np.zeros([5,120],dtype=np.float32)
China_Total_Pre=Hubei
ShowProvince=['Beijing','Shanghai','Guangdong','Zhejiang','Henan','Hunan','Jiangxi','Anhui']
# Adjust the pupolation flow
Little_High_Province=['Hunan','Guangxi','Jilin','Liaoning','Shanghai']
High_Province=['Jilin','Tibet','Xinjiang','Sichuan','Liaoning','Shaanxi','Tianjin','Shanxi','Gansu','Qinghai','Hebei','Yunnan','Hainan','Guizhou','Inner Mongolia','Fujian']
Far_High_Province=['Jilin','Tibet','Sichuan','Liaoning','Shaanxi','Hainan','Qinghai','Inner Mongolia','Gansu','Shanxi','Yunnan']
Low_Province=['Ningxia','Zhejiang','Shandong','Jiangsu','Guangdong','Henan','Chongqing','Fujian']
Far_Low_Province=['Shandong','Jiangsu','Guangdong','Chongqing']
for j in range(34):
    Province=prov.Province[j]
    if(prov.Province[j]=='Hubei' or prov.Province[j]=='Hong Kong' or prov.Province[j]=='Macau' or prov.Province[j]=='Taiwan'):
        continue
    p    =prov.Population[j] * 10000
    alpha=prov.FlowRatio[j]/100
    if Province=='Guangxi':
        alpha=0.85/100.
    if Province=='Hunan':
        alpha=3.52/100.
        
    if Province=='Tibet':
        alpha/=10
    if Province in High_Province:
        alpha/=3
    if Province in Far_High_Province:
        alpha/=2
    if Province in Little_High_Province:
        alpha/=2
    if Province in Low_Province:
        alpha*=3
    if Province in Far_Low_Province:
        alpha*=2
    if Province=='Anhui':
        alpha*=1.2
    if Province =='Henan' or Province =='Guangdong' :
        alpha*=5
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
        
        h=b*Place[2,i]/p
        
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
        Place[1,i+1]=Place[1,i]+ h*Place[0,i]- thita*Place[1,i]+ alpha*m*Wuhan[1,i]*Flow_rate[i]
        Place[2,i+1]=Place[2,i]+ thita*Place[1,i]- r*Place[2,i]- k*Place[2,i]+ alpha*n*Wuhan[2,i]*Flow_rate[i]
        Place[3,i+1]=Place[3,i]+r*Place[2,i]
        Place[4,i+1]=Place[4,i]+k*Place[2,i]
    
    Place=Place.astype(np.int)
    China_Total_Pre+=Place
    Date_List_tmp=['1.22','1.27','2.1','2.6','2.11','2.16','2.21']
#    if Province=='Beijing' or Province=='Shanghai':
#    fig = plt.figure(4+j)
#    plt.plot(range(len(prov.Confirmed[j])), Place[2,52:66], '+-',label='Predictions') #1.22->2.4
#    Date_List_tmp=['1.22','1.24','1.26','1.28','1.30','2.1','2.3','2.5']
#    plt.xticks(range(0,15,2),Date_List_tmp)
#    plt.xlabel('Date')
#    plt.ylabel('Confirmed Cases')
#    plt.legend(loc = 'best')
#    tit='Prediction for Infected in '+prov.Province[j]
#    plt.title(tit)
#    if Province== 'Shanghai':
#        plt.savefig('./figure/Shanghai_Validation.png',dpi=1000)
#    else:
#        plt.savefig('./figure/Beijing_Validation.png',dpi=1000)
    
    if Province in ShowProvince:
        StackProvince[Province]=Place[2,52:93]#1.22->3.1


pd.DataFrame(StackProvince).to_csv('./Data/Stack_Province_No_Geo_Restriction.csv')
#print(StackProvince)
#1.22->2.4

#fig = plt.figure(40)
#plt.plot(range(len(prov.China_Total)), prov.China_Total, 'o-',label='True Values')
#plt.plot(range(len(prov.China_Total)), China_Total_Pre[2,52:66], '+-',label='Predictions') #1.22->2.4
#plt.xticks(range(0,15,2),Date_List_tmp)
#plt.xlabel('Date')
#plt.ylabel('Confirmed Cases')
#plt.legend(loc = 'best')
#plt.title('Prediction for Infected in China')
#plt.savefig('./figure/China_Validation.png',dpi=1000)
#
#China_Total_No_Holiday=No_Holiday.China_Total_Pre
#Date_List_tmp=['1.22','1.27','2.1','2.6','2.11','2.16','2.21','2.26','3.2']
#fig = plt.figure(41)
#plt.plot(range(41), China_Total_Pre[2,52:93], 'o-',label='Predictions With Extended Holiday') #1.22->2.20
#plt.plot(range(41), China_Total_No_Holiday[2,52:93], 'o-',label='Predictions')
#plt.xticks(range(0,41,5),Date_List_tmp)
#plt.xlabel('Date')
#plt.ylabel('Confirmed Cases')
#plt.legend(loc = 'best')
#plt.title('Prediction for Infected in China')
#plt.savefig('./figure/China_Total_Holiday_Comp.png',dpi=1000)