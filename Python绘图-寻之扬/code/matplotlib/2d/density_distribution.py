# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


def joint_plot(x, y):
    """
    绘制二维密度分布图
    x: list of real number, x-axis coordinates
    y: list of real number, y-axis coordinates
    """
    sns.jointplot('xlabel', 'ylabel', data=pd.DataFrame({'xlabel':x, 'ylabel':y}), kind='hex')
    # kind: 使用的joint plot的种类。例如: 'hex'，六边图（效果类似于hist2d）；'kde'，核密度（即密度等高线）等
    # plt.colorbar()
    # plt.show()


def density_contour(x, y):
    """
    绘制密度等高线
    x: list of real number, x-axis coordinates
    y: list of real number, y-axis coordinates
    """
    plt.figure()
    sns.kdeplot(x, y, cmap='Reds', shade=True, cbar=True, shade_lowest=False)
    # cmap: 使用的颜色，  shade: 是否填充颜色
    # shade_lowest: 尽可能少的填充等高线
    # cbar: 是否使用颜色条（在部分电脑上无法使用）
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.title('title')
    # plt.colorbar()
    # plt.show()


def plot_hist2d(x, y, bins=50):
    """
    绘制二维密度分布图（导入seaborn后效果变差）
    x: list of real number, x-axis coordinates
    y: list of real number, y-axis coordinates
    bins: int, number of bins along one axis
    """
    plt.figure()
    plt.hist2d(x, y, bins=bins)  #range, cmin, cmax
    # bins: 同一维直方图
    plt.xlabel('xlabel')
    plt.ylabel('ylabel')
    plt.title('title')
    plt.colorbar()
    # plt.show()


def demo():
    x = np.random.normal(size=5000)
    y = x / 2 + np.random.normal(size=5000)

    # plot_hist2d(x, y)
    density_contour(x, y)
    # joint_plot(x, y)
    plt.savefig('demo1.png', dpi=800)
    plt.show()


if __name__ == '__main__':
    demo()
