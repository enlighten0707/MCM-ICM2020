# -*- coding: utf-8 -*-
#导包，设置环境
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

# 导入/输入原始数据
raw_data = pd.read_csv('raw_data.csv',encoding='gb2312')
y = raw_data['val'].T.values
y1 = y[0:10]
y2 = y[10:20]
x1 = range(0,len(y1))
x2 = range(0,len(y2))

# 绘制折线图，更多属性请查阅https://matplotlib.org/api/_as_gen/matplotlib.pyplot.plot.html
h1 = plt.plot(x1,y1,label='Line1',linestyle='-',linewidth=1,color='blue',marker='x',markersize=4,markeredgecolor='green',markerfacecolor='red')
h2 = plt.plot(x2,y2,label='Line2',linestyle=':',linewidth=1,color=[1,.05,.5],marker='o',markersize=4,markeredgecolor='green',markerfacecolor='red')

# 其他属性设置
# 坐标轴
# plt.xlim()    # x轴范围
plt.ylim(min(min(y1),min(y2)),max(max(y1),max(y2)))    # y轴范围
plt.xticks([0,2,4,6,8],[1,2,'cutoff',4,5])         # x轴标签，第一个参数为欲替换的x坐标，第二个参数为对应替换坐标的标签
# plt.yticks()

# 坐标轴标签，更多属性请查阅https://matplotlib.org/api/text_api.html#matplotlib.text.Text
plt.xlabel('Year',fontname='Times New Roman',fontsize=10)
plt.ylabel('Val')

# 图例显示
# loc--位置（1:右上，2：左上，3：左下，4：右下）
plt.legend(loc=1,prop={'size':10})

# 网格线开关
plt.grid(x1)
# plt.grid(x2);

plt.savefig('line.png', dpi=800)
plt.show()
