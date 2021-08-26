import os
os.system('clear')
print("Gaussian Filter")

import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt

#arr = np.arange(50, step=2).reshape((5,5))
arr = np.load('path').reshape((2,2,2),order='F')

attenuation_map = gaussian_filter(arr, sigma=1)

plt.imshow(attenuation_map)
plt.show()