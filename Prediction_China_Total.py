# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 17:30:53 2020

@author: 86150
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

fig = plt.figure()

plt.style.use('seaborn-whitegrid')


plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 2000

Date_List=['1.24','1.29','2.3','2.8','2.13','2.18','2.23','2.28','3.4']
data=pd.read_csv('./Data/Prediction_China_Total.csv')
Pre_China_Total=data.Total
plt.plot(range(31),Pre_China_Total[:31],'o-',label='Prediction')
plt.xticks(range(0,35,5),Date_List)
plt.xlabel('Date')
plt.ylabel('Confirmed Cases')
plt.title('China Infection Prediction')

data=pd.read_csv('./Data/True_Value_China_Total.csv')
True_China_Total=data.Total
plt.plot(range(len(True_China_Total)),True_China_Total,'x',label='True Value')
plt.legend(loc='best')

plt.savefig('./figure/China_Total_Prediction.png')