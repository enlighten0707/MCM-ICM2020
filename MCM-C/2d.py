import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import trim_mean
from scipy.stats.mstats import winsorize
from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression

np.set_printoptions(suppress = True)
proportion_cut = 0.2

f = pd.read_csv('.\\hair_dryer.tsv', sep = '\t')
f = f[f.verified_purchase == 'Y']
sells = f['product_parent'].value_counts()
f = f.iloc[::-1, :]
group_data = f.groupby('product_parent')
print('Preprocessing Complete!\n')

for (prod_parent, file) in group_data:
    if sells[prod_parent] < 200:
        continue
    print('-------------------------------------------\n')
    print('Product Parent:', prod_parent)
    print('Sell Counts:', sells[prod_parent],'\n')
    max_cont_low, max_cont_high = 5, 10
    m = file.shape[0]
    data = np.zeros((m,2))
    data[:,0], data[:,1] = file.star_rating, file.helpful_votes
    
    avg_star, avg_help = np.mean(file.star_rating), np.mean(winsorize(file.helpful_votes, limits = [0, proportion_cut]))
    low, high = np.zeros((max_cont_low - 1, 3)), np.zeros((max_cont_high - 1, 3))

    for i in range(2, max_cont_low + 1):
        m = file.shape[0]
        star_low, help_low = [ ], [ ]
        for j in range(i, m):
            cont_low = True
            #Another strange way to define continuous anomaly star.
            #if np.average(data[(j - i):(j - 1), 0]) <= 4.5:
            #    cont_high = False
            #if np.average(data[(j - i):(j - 1), 0]) >= 3:
            #    cont_low = False
            for k in range(j - i, j):
                if data[k, 0] >= 4:
                    cont_low = False
                    break
            if cont_low:
                star_low.append(data[j,0])
                help_low.append(data[j,1])

        if len(help_low) == 0:
            break
        help_low = winsorize(np.array(help_low), limits = [0, proportion_cut])
        low[i - 2, 0] = np.mean(help_low)
        low[i - 2, 1] = np.var(help_low)
        low[i - 2, 2] = len(help_low)

    for i in range(2, max_cont_high + 1):
        m = file.shape[0]
        star_high, help_high = [ ], [ ]
        for j in range(i, m):
            cont_high = True
            for k in range(j - i, j):
                if data[k, 0] <= 3:
                    cont_high = False
                    break
            if cont_high:
                star_high.append(data[j,0])
                help_high.append(data[j,1])

        if len(help_high) == 0:
            break
        help_high = winsorize(np.array(help_high), limits = [0, proportion_cut])
        high[i - 2, 0] = np.mean(help_high)
        high[i - 2, 1] = np.var(help_high)
        high[i - 2, 2] = len(help_high)

    low = pd.DataFrame(data = low, index = range(2,6), columns = ['Average', 'Varience', 'Count'])
    high = pd.DataFrame(data = high, index = range(2,11), columns = ['Average', 'Varience', 'Count'])

    print(avg_star, avg_help, '\n')
    print('Continuously Low Star:', '\n')
    print(low, '\n')
    print('Continuously High Star:', '\n')
    print(high, '\n')
