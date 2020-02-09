"""
=========================================================
matplotlib中没有Wilkinson点图示例，并排多重直方图效果相同
=========================================================

这原本是一个multiple histograms side by side的示例，我在其
基础上添加了部分中文注释提高可读性。

=======================================================
Demo of how to produce multiple histograms side by side
=======================================================

This example plots horizontal histograms of different samples along
a categorical x-axis. Additionally, the histograms are plotted to
be symmetrical about their x-position, thus making them very similar
to violin plots.

To make this highly specialized plot, we can't use the standard ``hist``
method. Instead we use ``barh`` to draw the horizontal bars directly. The
vertical positions and lengths of the bars are computed via the
``np.histogram`` function. The histograms for all the samples are
computed using the same range (min and max values) and number of bins,
so that the bins for each sample are in the same vertical positions.

Selecting different bin counts and sizes can significantly affect the
shape of a histogram. The Astropy docs have a great section on how to
select these parameters:
http://docs.astropy.org/en/stable/visualization/histogram.html
"""

import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
number_of_bins = 20

# An example of three data sets to compare
# 下面产生测试数据，分为三种A、B、C
number_of_data_points = 387
labels = ["A", "B", "C"]
data_sets = [np.random.normal(0, 1, number_of_data_points),
             np.random.normal(6, 1, number_of_data_points),
             np.random.normal(-3, 1, number_of_data_points)]

# Computed quantities to aid plotting
hist_range = (np.min(data_sets), np.max(data_sets))
binned_data_sets = [
    np.histogram(d, range=hist_range, bins=number_of_bins)[0]
    for d in data_sets
# 生成柱状图
]
binned_maximums = np.max(binned_data_sets, axis=1)
# 设置x坐标，按数据集最大数目
x_locations = np.arange(0, sum(binned_maximums), np.max(binned_maximums))

# The bin_edges are the same for all of the histograms
# 每一行的下边缘位置
bin_edges = np.linspace(hist_range[0], hist_range[1], number_of_bins + 1)
# 每一行的中心位置
centers = 0.5 * (bin_edges + np.roll(bin_edges, 1))[:-1]
# 每一行的高度
heights = np.diff(bin_edges)

# Cycle through and plot each histogram
fig, ax = plt.subplots()
# zip函数将长度相同的列表相同位置上的元素组合为元组并返回新的列表
for x_loc, binned_data in zip(x_locations, binned_data_sets):
    lefts = x_loc - 0.5 * binned_data
    ax.barh(centers, binned_data, height=heights, left=lefts)

ax.set_xticks(x_locations)
ax.set_xticklabels(labels)

ax.set_ylabel("Data values")
ax.set_xlabel("Data sets")

plt.show()
