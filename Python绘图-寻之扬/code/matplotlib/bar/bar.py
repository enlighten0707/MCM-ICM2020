# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
# plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

data_week2015 = pd.read_csv('data_week2015.txt')['nums'].T.values
data_week2016 = pd.read_csv('data_week2016.txt')['nums'].T.values
plt.figure(figsize=(10, 6))
xweek=range(0,len(data_week2015))
xweek1=[i+0.3 for i in xweek]
plt.bar(xweek,data_week2015,color='g',width = .3,alpha=0.6,label='2015年')
plt.bar(xweek1,data_week2016,color='r',width = .3,alpha=0.4,label='2016年')
plt.xlabel('周')
plt.ylabel('XX事件数量')
plt.title('XX事件数周分布')
plt.legend(loc='upper right')
plt.xticks(range(0,7),['星期日','星期一','星期二','星期三','星期四','星期五','星期六'])
plt.show()
