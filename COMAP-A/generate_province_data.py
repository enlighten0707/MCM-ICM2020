# -*- coding: utf-8 -*-

#Dict: P,I,D,R
#Col: Time Series. Dec 1st,2019  -->

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 600


time_stamp={}

Date_List=['0122','0123','0124','0125','0126','0127','0128','0129','0130',
           '0131','0201','0202','0203','0204']


for i,date in enumerate(Date_List):
    file='./Data/Province_Data/'+date+'.csv'
    data=pd.read_csv(file,sep='|',error_bad_lines=False)
    data.drop(['deaths','notes','sources'],axis=1,inplace=True)
    
    for j,place in enumerate(data.place):
        if time_stamp.get(place) ==None :
            time_stamp[place]=[]
            for k in range(i):
                time_stamp[place].append(0)
        time_stamp[place].append(data.confirmed_cases[j])
    
China_Total=np.array(time_stamp.pop('CHINA TOTAL'))
Province=np.array(list(time_stamp))
Confirmed=np.array(list(time_stamp.values()))

data=pd.read_csv('./Data/Province_Basic_Data.csv',error_bad_lines=False)
Population=np.array(data.Population)
FlowRatio=np.array(data.FlowRatio,dtype=np.float32)
Cases=np.array(data.Confirmed_Cases,dtype=np.float32)


fig=plt.figure()

for i in range(34):
    if FlowRatio[i]>20:
        continue
    plt.plot(FlowRatio[i],Cases[i],'o',markersize=8)
plt.xlabel('FlowRatio(%)')
plt.ylabel('Confirmed Cases')
plt.title('Correlation Between Cases and Inflow')

fig.savefig('./figure/Relation_Ana.png')

