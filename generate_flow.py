# -*- coding: utf-8 -*-
"""
Created on Sat Feb  8 11:37:40 2020

@author: 86150
"""

import pandas as pd
import numpy as np

P=11000000.

Flow_rate = (np.random.rand(31) * 150 + 150) * 1000
Flow_rate/= P
Flow_rate_= pd.read_csv('Wuhan_Flow.csv',error_bad_lines=False) 
Flow_rate_.drop(['Date','Point','Rate'],axis=1,inplace=True)
Flow_rate=np.concatenate((Flow_rate, 1000*Flow_rate_.Flow/P),axis=0)
Flow_rate_=np.zeros(67)
Flow_rate=np.concatenate((Flow_rate,Flow_rate_),axis=0)
pd.DataFrame(Flow_rate).to_csv('Flow_Rate_Data.csv')