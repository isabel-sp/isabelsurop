import numpy as np
import matplotlib.pyplot as plt


x = np.random.randint(0,10,5)
y = np.random.randint(0,10,5)
    
plt.plot(x, y, '-bD',  c='blue', mfc='red', mec='k')
plt.show()