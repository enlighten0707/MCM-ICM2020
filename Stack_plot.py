import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

Date_List=['1-22','1-27','2-1','2-5','2-10','2-15','2-20','2-25','3-1']
fig = plt.figure()
# #fig.set_size_inches(6, 4)
#
#plt.subplot(1,2,1)
plt.grid()

plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 600
plt.style.use('ggplot')

data=pd.read_excel('./Data/Stack_Province.xlsx')

channel = data.columns
#
N = np.arange(data.shape[0])

labels = data[channel[0]]
y1=data[channel[1]]
y2=data[channel[2]]
y3=data[channel[3]]
y4=data[channel[4]]
y5=data[channel[5]]
y6=data[channel[6]]
y7=data[channel[7]]
y8=data[channel[8]]


colors = ['#ff9999','#9999ff','#cc1234','#1E8449','#3498DB','#34495E','#6C3483','#283747']
#colors = ['#ff9999','#9999ff','#cc1234','#1E8449','#3498DB']
plt.stackplot(N, y1,y2,y3,y4,y5,y6,y7,y8,colors=colors)


for i in range(len(colors)):
	plt.plot([],[],color=colors[i],label=channel[i + 1],linewidth=5)

fig=plt.figure(1)
plt.legend(loc='upper left')
plt.title('Predictions for Several Provinces')
plt.ylabel('Num of Infected (person)')
plt.xlabel('Date')
plt.xlim((0,40))
plt.xticks(range(0,41,5),Date_List)
plt.savefig('./figure/Stack_Province.png')
plt.show()




#------------------------------------------------------------------------------
data=pd.read_excel('./Data/Stack_Province_No_Holiday.xlsx')

channel = data.columns

N = np.arange(data.shape[0])

labels = data[channel[0]]
y1=data[channel[1]]
y2=data[channel[2]]
y3=data[channel[3]]
y4=data[channel[4]]
y5=data[channel[5]]
y6=data[channel[6]]
y7=data[channel[7]]
y8=data[channel[8]]

plt.grid()
plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 1000
plt.style.use('ggplot')
colors = ['#ff9999','#9999ff','#cc1234','#1E8449','#3498DB','#34495E','#6C3483','#283747']
plt.stackplot(N, y1,y2,y3,y4,y5,y6,y7,y8,colors=colors)


for i in range(len(colors)):
	plt.plot([],[],color=colors[i],label=channel[i + 1],linewidth=5)




#plt.legend(loc='upper left')
plt.title('Predictions for Several Provinces')
plt.ylabel('Num of Infected (person)')
plt.xlabel('Date')
plt.xlim((0,40))
plt.xticks(range(0,41,5),Date_List)
plt.savefig('./figure/Stack_Province_No_Holiday.png')
plt.show()




#------------------------------------------------------------------------------
data=pd.read_excel('./Data/Stack_Province_No_Geo_Restriction.xlsx')

channel = data.columns

N = np.arange(data.shape[0])

labels = data[channel[0]]
y1=data[channel[1]]
y2=data[channel[2]]
y3=data[channel[3]]
y4=data[channel[4]]
y5=data[channel[5]]
y6=data[channel[6]]
y7=data[channel[7]]
y8=data[channel[8]]

plt.grid()
plt.rcParams['font.sans-serif'] = 'Consolas'
plt.rcParams['axes.unicode_minus'] = True
plt.rcParams['savefig.dpi'] = 1000
plt.style.use('ggplot')
colors = ['#ff9999','#9999ff','#cc1234','#1E8449','#3498DB','#34495E','#6C3483','#283747']
plt.stackplot(N, y1,y2,y3,y4,y5,y6,y7,y8,colors=colors)


for i in range(len(colors)):
	plt.plot([],[],color=colors[i],label=channel[i + 1],linewidth=5)


#plt.legend(loc='upper left')
plt.title('Predictions for Several Provinces')
plt.ylabel('Num of Infected (person)')
plt.xlabel('Date')
plt.xlim((0,40))
plt.xticks(range(0,41,5),Date_List)
plt.savefig('./figure/Stack_Province_No_Geo_Restriction.png')
plt.show()