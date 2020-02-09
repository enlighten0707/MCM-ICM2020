import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

#导入数据集
df = pd.read_csv("data.csv")
#拆分不同性别对应数据
mdf = df.query("sex=='m'")
fdf = df.query("sex=='f'")
#绘制男性数据
ax = mdf.plot.scatter(x='ageYear', y='heightIn', color='b', label='m')
#绘制女性数据
fdf.plot.scatter(x='ageYear', y='heightIn', color='r', label='f', ax=ax)
#显示绘图结果
plt.show()
