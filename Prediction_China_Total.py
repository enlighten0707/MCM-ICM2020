# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:30:53 2020

@author: 86150
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import Prediction_China_With_Holiday

fig = plt.figure(figsize=(8.0,4.0))

plt.style.use('seaborn-whitegrid')



plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 600
#plt.rcParams['figure.figsize'] = (8.0, 4.0)

Date_List=['1.24','1.29','2.3','2.8','2.13','2.18','2.23','2.28','3.4']
data=pd.read_csv('./Data/Prediction_China_Total.csv')
Pre_China_Total=data.Total
plt.plot(range(31),Prediction_China_With_Holiday.China_Total_Pre[2,52:83],'o-',label='Prediction',markersize=5)
plt.xticks(range(0,35,5),Date_List)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.title('China Infection Prediction',fontsize=13)

data=pd.read_csv('./Data/True_Value_China_Total.csv')
True_China_Total=data.Total
plt.plot(range(len(True_China_Total)),True_China_Total,'x',label='True Value',markersize=5)
plt.legend(loc='best')

plt.savefig('./figure/China_Total_Prediction.png')