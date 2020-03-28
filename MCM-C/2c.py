import numpy as np
import pandas as pd
from scipy.stats.mstats import winsorize
from sklearn.linear_model import Lasso
from sklearn.preprocessing import MinMaxScaler

np.set_printoptions(suppress = True)
# 由于数据中非常多的0赞评论和少量的高赞评论，直接求平均受极端值影响比较严重
# 这里设定缩尾比例，后文helpful_votes一项在求均值时均采用单侧缩尾均值
proportion_cut = 0.2

f = pd.read_csv('.\\hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']
sells = f['product_parent'].value_counts()
f = f.iloc[::-1, :]
group_data = f.groupby('product_parent')
print('Preprocessing Complete!\n')

# X为自变量矩阵，需要添加语义特征，y为销量向量，无需修改
X, y = np.zeros((0,5)), [ ]

for (prod_parent, file) in group_data:
    if sells[prod_parent] < 10:
        continue
    temp = file[file.star_rating >= 4]
    avg_star, avg_help = np.mean(file.star_rating), np.mean(file.helpful_votes)
    y.append(sells[prod_parent])

    # 本段代码待补充，X的列需要添加特征
    avg_total, avg_help_total_ratio = np.mean(file.total_votes), np.mean(file.helpful_votes / file.total_votes)
    X = np.concatenate((X, np.array([[avg_help, avg_star, temp.shape[0] / file.shape[0], avg_total, avg_help_total_ratio]])), axis = 0)
    # 待补充片段结束

# y转为numpy对象并归一化
temp = np.zeros((len(y), 1))
temp[:,0] = y
y = temp
ss = MinMaxScaler()
y = ss.fit_transform(y)

# 正则化系数alpha根据特征加入以后的拟合结果确定
lasso_filter = Lasso(alpha = 0.0005)
sx = MinMaxScaler()
lasso_filter.fit(X, y)
coef = lasso_filter.coef_
print(coef)

# 系数为0的项视为无关项去掉，然后再用LinearRegression做一次回归得到2c的最终模型

