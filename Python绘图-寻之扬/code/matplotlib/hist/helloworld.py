import numpy as np
import matplotlib.pyplot as plt

data = np.random.randn(1000)

plt.hist(data, normed = True)

plt.show()
