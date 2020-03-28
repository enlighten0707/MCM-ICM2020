# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 17:12:43 2020

@author: 86150
"""

import numpy as np
import pandas as pd
import Data_Analysis as DA
from scipy.stats.mstats import winsorize
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import LassoCV
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from ult_feature import Generate_feature_2c

np.set_printoptions(suppress = True)
# 由于数据中非常多的0赞评论和少量的高赞评论，直接求平均受极端值影响比较严重
# 这里设定缩尾比例，后文helpful_votes一项在求均值时均采用单侧缩尾均值
proportion_cut = 0.2

f = pd.read_csv('./Data/hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']
sells = f['product_parent'].value_counts()
f = f.iloc[::-1, :]
group_data = f.groupby('product_parent')
print('Preprocessing Complete!\n')

## X为自变量矩阵，需要添加语义特征，y为销量向量，无需修改
X, y = np.zeros((0,4)), [ ] # 这里改变量数
sx = MinMaxScaler()


for (prod_parent, file) in group_data:
    if sells[prod_parent] < 10:
        continue
    temp = file[file.star_rating >= 4]
    avg_star, avg_help = np.mean(file.star_rating), np.mean(file.helpful_votes)
    y.append(sells[prod_parent])
    
    avg_feature = Generate_feature_2c('hair_dryer',file,sells[prod_parent])
    avg_total, avg_help_total_ratio = np.mean(file.total_votes), np.mean(file.helpful_votes / file.total_votes)
    
    # 这里改变量
    X = np.concatenate((X, np.array([[avg_feature, avg_star, temp.shape[0] / file.shape[0], avg_help]])), axis = 0)
    
# y转为numpy对象并归一化
temp = np.zeros((len(y), 1))
temp[:,0] = y
y = temp
ss = MinMaxScaler()
y = ss.fit_transform(y)
print(y)

# 正则化系数alpha根据特征加入以后的拟合结果确定,通过搜索找到了相对合理的解
# 搜索，找到符合常数的alpha值，得到系数解
alpha = 0.000005
while alpha < 1 :
    print('alpha = %f' % alpha)
    lasso_filter = Lasso(alpha)
    lasso_filter.fit(X, y)
    coef = lasso_filter.coef_
    print(coef)
    alpha *= 2

##################################
#    以上代码先运行，运行完之后，把X，y部分注释掉，运行下面的代码，X变为筛选出来的变量
#################################
# 系数为0的项视为无关项去掉，然后再用LinearRegression做一次回归得到2c的最终模型
#X, y = np.zeros((0,3)), [ ]
#for (prod_parent, file) in group_data:
#    if sells[prod_parent] < 10:
#        continue
#    temp = file[file.star_rating >= 4]
#    avg_star = np.mean(file.star_rating)
#    y.append(sells[prod_parent])
#    
#    avg_feature = Generate_feature_2c('hair_dryer',file)
#    avg_help_total_ratio = np.mean(file.helpful_votes / file.total_votes)
#    
#    X = np.concatenate((X, np.array([[avg_feature, avg_star, avg_help_total_ratio]])), axis = 0)
#
## y转为numpy对象并归一化
#temp = np.zeros((len(y), 1))
#temp[:,0] = y
#y = temp
#ss = MinMaxScaler()
#y = ss.fit_transform(y)
#
#sx = MinMaxScaler()
#std_X = sx.fit_transform(X)
#lin = LinearRegression()
#lin.fit(std_X,y)
#coef = lin.coef_
#print(coef)
