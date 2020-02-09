# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 19:54:47 2020

@author: 86150
"""


#Dict: P,I,D,R
#Col: Time Series. Dec 1st,2019  --> Feb 18th,2020

import pandas as pd
import numpy as np

time_stamp={}

Date_List=['0122','0123','0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203','0204']


for i,date in enumerate(Date_List):
    file='./Province_Data/'+date+'.csv'
    data=pd.read_csv(file,sep='|',error_bad_lines=False)
    data.drop(['deaths','notes','sources'],axis=1,inplace=True)
    
    for j,place in enumerate(data.place):
        if time_stamp.get(place) ==None :
            time_stamp[place]=[]
            for k in range(i):
                time_stamp[place].append(0)
        time_stamp[place].append(data.confirmed_cases[j])
    
China_Total=time_stamp.pop('CHINA TOTAL')
Province=np.array(list(time_stamp))
Confirmed=np.array(list(time_stamp.values()))

data=pd.read_csv('Province_Basic_Data.csv',error_bad_lines=False)
Population=np.array(data.Population)
FlowRatio=np.array(data.FlowRatio,dtype=np.float32)
print(China_Total)