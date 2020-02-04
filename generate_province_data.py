# -*- coding: utf-8 -*-
"""
Created on Tue Feb  4 19:54:47 2020

@author: 86150
"""

import pandas as pd

time_stamp={}

Date_List=['0122','0123','0124','0125','0126','0127','0128','0129','0130','0131','0201','0202','0203']


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
    
pd.DataFrame(time_stamp).to_csv('Province_Data.csv')
tmp=pd.DataFrame(time_stamp)
print(tmp)
