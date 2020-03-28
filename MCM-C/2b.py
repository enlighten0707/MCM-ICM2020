import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm

# 超参数：销量数据清洗阈值 min_sell，滑动平均/趋势分析窗口 N，趋势检验显著性水平 p
min_sell = 200
N = 12
p = 0.10

# 计算 Z 统计量
def Z_stats(x, var):
    Z = (x - np.sign(x)) / np.sqrt(var)
    return Z

f = pd.read_csv('.\\Problem_C_Data\\hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']
f = f.iloc[::-1, :]

# 以月为时间单位，格式化 review_date
f['review_date'] = pd.to_datetime(f['review_date'])
f['review_date'] = f['review_date'].map(lambda x: x.strftime("%Y-%m"))

# 1）整理出有review的月份（这里存在月份不连续的情况，后面会把2008年以前的稀疏数据洗掉，保证连续）
# 2）洗掉低销量的产品，这些产品可能带来较大噪声（这一步的阈值可以修改，目前只是一个框架）
temp = pd.value_counts(f['review_date'])
sells = f['product_parent'].value_counts()
for item in sells.index:
    if sells[item] < min_sell:
        f = f[f.product_parent != item]
sells = f['product_parent'].value_counts()
group_data = f.groupby('product_parent')

# 生成单月销量和星级数据，2008年以前数据剔除，导入数据并填充缺失值
sell_mat = pd.DataFrame(index = temp.index, columns = sells.index)
star_mat = pd.DataFrame(index = temp.index, columns = sells.index)
sell_mat = sell_mat.sort_index()
star_mat = star_mat.sort_index()
sell_mat = sell_mat[sell_mat.index >= '2008-01']
star_mat = star_mat[star_mat.index >= '2008-01']

for (prod_parent, file) in group_data:
    temp = pd.value_counts(file.review_date)
    temp = temp[temp.index >= '2008-01']
    for date in temp.index:
        sell_mat.loc[date].loc[prod_parent] = temp[date]
        star_mat.loc[date].loc[prod_parent] = np.mean(f[f.review_date == date].star_rating)

sell_mat = sell_mat.fillna(0)

star_mat = star_mat.fillna(method = 'ffill')
star_mat = star_mat.fillna(0)

# 销量和星级数据归一化，加权得到目标变量矩阵
sell_min, sell_max = sell_mat.min().min(), sell_mat.max().max()
star_min, star_max = star_mat.min().min(), star_mat.max().max()

weight = (0.9, 0.1)

y_mat = weight[0] * (sell_mat - sell_min) / (sell_max - sell_min) + weight[1] * (star_mat - star_min) / (star_max - star_min)

# y为y_mat进行12个月滑动平均处理后的数据（现在是简单平均，可以考虑改成指数平滑），用于可视化和模型验证分析
y = pd.DataFrame(index = y_mat.index, columns = sells.index)
y = y.fillna(0)

trend = pd.DataFrame(index = y_mat.index, columns = sells.index)
trend = trend.fillna(0)
idx_rev = y_mat.index[::-1]

for i in range(np.shape(idx_rev)[0] - N + 1):
    temp = idx_rev[i : i + N]
    count = 1
    for j in temp:
        y.loc[idx_rev[i]] += y_mat.loc[j]
        for k in temp[count:N]:
            trend.loc[idx_rev[i]] += np.sign(y_mat.loc[j] - y_mat.loc[k])
        count += 1

y = y / N

# 季度为单位，得到 Z 统计量，假设检验（U-test）得到上升/下降趋势是否在 p 水平上显著
idx = y_mat.index
for i in idx:
    if int(str(i).split('-')[1]) % 3 != 0:
        idx = idx[idx != i]
        
var_trend = pd.DataFrame(index = y_mat.index, columns = sells.index)
var_trend = var_trend.fillna(0) + N * (N - 1) * (2 * N + 5) / 18

for i in trend.index:
    for j in sells.index:
        trend.loc[i].loc[j] = Z_stats(trend.loc[i].loc[j], var_trend.loc[i].loc[j])

rise_sig = pd.DataFrame(index = idx, columns = sells.index)
fall_sig = pd.DataFrame(index = idx, columns = sells.index)

for i in idx:
    for j in sells.index:
        rise_sig.loc[i].loc[j] = trend.loc[i].loc[j] >= abs(norm.ppf(p))
        fall_sig.loc[i].loc[j] = trend.loc[i].loc[j] <= -abs(norm.ppf(p))

print(y, '\n')
print(trend, '\n')
print(rise_sig, '\n')
print(fall_sig)

# 绘制原始数据滑动平均后的曲线，进行模型验证分析
plt.style.use('seaborn-whitegrid')
plt.figure(1)
plt.plot(y.index, y, linewidth = 0.8)
plt.show()
