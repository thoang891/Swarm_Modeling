# Import libraries
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


# Creating dataset
x = np.outer(np.linspace(-10, 10, 100), np.ones(100))
y = x.copy().T # transpose
z = (np.sin(x **2) * x + np.cos(y **2) * y )

# Creating figure
fig = plt.figure(figsize =(14, 9))
ax = plt.axes(projection ='3d')

# Creating plot
ax.plot_surface(x, y, z)

# show plot
plt.show()
