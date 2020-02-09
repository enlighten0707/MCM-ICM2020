import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# fig = plt.figure()
# #fig.set_size_inches(6, 4)
#
plt.grid()



plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 1000
plt.style.use('ggplot')

gdp=pd.read_excel('GDP.xlsx')

labels = gdp.index

print(labels)
channel = gdp.columns


N = np.arange(gdp.shape[0])

y1=gdp[channel[1]]/10.0
y2=gdp[channel[2]]/10.0
y3=gdp[channel[3]]/10.0
y4=gdp[channel[4]]/10.0
y5=gdp[channel[5]]/10.0
y6=gdp[channel[6]]/10.0
y7=gdp[channel[7]]/10.0
y8=gdp[channel[8]]/10.0

colors = ['#ff9999','#9999ff','#cc1234','#1E8449','#3498DB','#34495E','#6C3483','#283747']

plt.stackplot(N, y1,y2,y3,y4,y5,y6,y7,y8,colors=colors)


for i in range(len(colors)):
	plt.plot([],[],color=colors[i],label=channel[i + 1],linewidth=5)


plt.legend(loc='upper left')
plt.title('2004-2013 Several Provinces GDP')
plt.ylabel('GDP (billion yuan)')
plt.xlabel('Year')
plt.xticks(N,gdp[channel[0]].values)
plt.savefig('Stack_plot.png')
plt.show()


print(gdp.columns)
