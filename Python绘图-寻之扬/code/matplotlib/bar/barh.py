# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
data_bar = pd.read_csv('data_week2015.txt',encoding='gb2312')
label = data_bar['day'].T
xtop = data_bar['nums'].T
idx = np.arange(len(xtop))
fig = plt.figure(figsize=(12,12))
plt.barh(idx, xtop, color='b',alpha=0.6)
plt.yticks(idx,label)
plt.grid(axis='x')#画竖直网格
plt.xlabel('XX事件次数')
plt.ylabel('XX事件名称')
plt.title('2015.1-2016.11月XX事件排行榜')
plt.show()
