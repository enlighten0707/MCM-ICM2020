import matplotlib.pyplot as plt
import random

# 输入为一个字典，格式为{x值:{y值:点个数, ...}, ...}
def Wilkinson(data):
    item_num = len(data)

    label = list(data.keys())
    print(label)
    y = []
    for i in data:
        y += list(data[i].keys())
    y_min = min(y)
    y_max = max(y)
    num = []
    for i in data:
        num += list(data[i].values())
    num_max = max(num)
    num_max = num_max*1.2

    x_center = []
    for i in range(item_num):
        x_center.append(num_max*(i+1))

    dot_x = []
    dot_y = []
    for i in range(item_num):
        tmp = label[i]
        cen = x_center[i]
        for j in data[tmp]:
            n = data[tmp][j]
            for k in range(data[tmp][j]):
                dot_x.append(cen+k-n/2)
                dot_y.append(j)
    # print(dot_x)
    # print(dot_y)
    fig, ax = plt.subplots()
    # 在此修改图像样式，c为颜色，s为大小，可以给点单独设置格式，列表中位置需对应
    ax.scatter(dot_x,dot_y,c=dot_x,s=dot_x,alpha=0.5)
    ax.set_xticks(x_center)
    ax.set_xticklabels(label)
    plt.show()

if __name__ == '__main__':
    data = {}
    label = ['A','B','C']
    for i in label:
        value = {}
        for j in range(-5, 5):
            value[j] = random.randint(0,10)
        data[i] = value
    # print('data=',data)
    Wilkinson(data)
