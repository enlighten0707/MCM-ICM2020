import numpy as np
import matplotlib.pyplot as plt

def one_dimension():
    data = np.random.rand(1000)
    plt.hist(data, bins=20, edgecolor='green', facecolor='red', linewidth=3, stacked=False, histtype='stepfilled')

def two_dimemsions():
    x = np.random.randn(20000, 2)
    n, bins, patches = plt.hist(x, alpha=0.5, normed=False, histtype='bar', bins=20, facecolor='r', edgecolor='black', stacked=False)
    #
    # plt.xticks(fontsize=30)
    # plt.yticks(fontsize=30)
    plt.xlabel("hahaha")
    plt.title("THIS IS A TITLE", verticalalignment = 'baseline')  #baseline, top

    for patch in patches[0]:
        patch.set_facecolor('b')
    for patch in patches[1]:
        patch.set_facecolor('r')


# one_dimension()
two_dimemsions()
plt.savefig("sample.png", dpi = 1000)
plt.show()
