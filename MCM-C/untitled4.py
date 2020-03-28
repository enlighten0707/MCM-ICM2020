# -*- coding: utf-8 -*-
"""
Created on Tue Mar 10 03:19:07 2020

@author: 86150
"""

import numpy as np
import random
import matplotlib.pyplot as plt

words=['use','power','price','work','time','blow']
data = [0.07474, 0.071009, 0.062131,0.056785,0.05136,0.042903]

#fig = plt.figure()
#plt.plot(range(6), data, 'o-',label='No Mutation') #1.22->2.20
#plt.xticks(range(0,51,5),Date_List_tmp)
#plt.xlabel('Date')
#plt.ylabel('Infected Cases')
#plt.legend(loc = 'best')
#plt.title('Prediction for Infected in China\n(With Mutation)')

plt.style.use('seaborn-white')


# 使用一个灰色的背景图 
ax = plt.axes(axisbg='#E6E6E6') 
ax.set_axisbelow(True) 

# 加上白色实心的网格线 
plt.grid(color='w', linestyle='solid') 

# 隐藏坐标系的外围框线 
for spine in ax.spines.values(): 
    spine.set_visible(False) 

# 隐藏上方与右侧的坐标轴刻度 
ax.xaxis.tick_bottom() 
ax.yaxis.tick_left() 

# 让刻度线与标签的颜色更亮一些 
ax.tick_params(colors='gray', direction='out') 
for tick in ax.get_xticklabels(): 
    tick.set_color('gray') 
for tick in ax.get_yticklabels(): 
    tick.set_color('gray') 

# 修改柱形的填充与边框颜色 
ax.hist(data, edgecolor='#E6E6E6', color='#EE6666'); 
        
##x1 = np.random.normal(0, 0.8, 1000)
##x2 = np.random.normal(-2, 1, 1000)
##x3 = np.random.normal(3, 2, 1000)
#kwargs = dict(histtype='stepfilled', alpha=0.7, normed=True, bins=40,edgecolor='#E6E6E6', color='#EE6666')
#ax.hist(data, **kwargs)
##ax.hist(x2, **kwargs)
##ax.hist(x3, **kwargs)

