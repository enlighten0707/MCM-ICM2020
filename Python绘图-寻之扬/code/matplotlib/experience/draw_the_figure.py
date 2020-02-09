import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad


#get the data from the .txt file
def get_data(filename):
    f = open(filename, 'r')
    new = []
    for line in f.readlines():
        new.append(float(line))

    f.close()
    return new

#return the size of alist
def size_of(alist):
    tem = np.array(alist)
    return int(tem.shape[0])

#return the value of F(x)
def fenbu_for_lisan(ax, new):
    old_data = np.array(new)
    new_data = np.sort(old_data, axis=0, kind='quicksort')
    size = size_of(new)
    i = 0
    count = 0
    while(i < size):
        if new_data[i] <= ax:
            count = count+1
        i = i+1
    return count*1.0/size

#sort the data list
def sort_list(alist):
    old_data = np.array(alist)
    new_data = np.sort(old_data, axis=0, kind='quicksort')
    tem_list = list(new_data)
    return tem_list

#return the element in the data list
#except the same one
def get_ele(alist):
    tem_list = sort_list(alist)
    size = size_of(tem_list)
    box = []
    for i in range(size):
        if (i == 0 or tem_list[i] != tem_list[i-1]):
            box.append(tem_list[i])
    return box



#frequency function of x
def f(x):
    y=-(x-172)**2/24.0
    t=np.sqrt(4*np.sqrt(3)*np.pi)
    return np.exp(y)/t
#distribution function of x
def F(x):
    if x < 0:
        return quad(f, -np.inf, x)[0]
    else:
        return quad(f, -np.inf, 0)[0]+quad(f, 0, x)[0]




#get the value of x
data = get_data("data_example.txt")
tem_x = []
tem_y1 = []
tem_y2 = []
index = get_ele(data)
size = size_of(index)
j = np.linspace(index[0]-1, index[0]) # default: num=50
tem_x.extend(list(j))
tem_x.append(index[0])

for i in range(size-1):
    j = np.linspace(index[i], index[i+1])
    tem_x.extend(list(j))
    tem_x.append(index[i+1])
j = np.linspace(index[size-1],index[size-1]+1,5)
tem_x.extend(list(j))
tem_x=sort_list(tem_x)

x = np.array(tem_x)

for element in tem_x:
    tem_y1.append(fenbu_for_lisan(element, data))
    tem_y2.append(F(element)/np.sqrt(np.pi))
y1 = np.array(tem_y1)
y2 = np.array(tem_y2)

plt.plot(x, y1, 'b-', lw=2.0, label='F‘(X) of x')
plt.plot(x, y2, 'r-', lw=2.0, label='F(X) of x')
plt.legend(loc='best')

ax = plt.gca()
ax.spines['right'].set_color('none') #set the right axe
ax.spines['top'].set_color('none')
ax.set_title('figure')

plt.savefig('experience.png', dpi = 1000)
plt.show()
