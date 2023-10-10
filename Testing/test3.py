from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt

import pyswarms as ps
from pyswarms.utils.plotters.formatters import Mesher

# Dataset
x = np.outer(np.linspace(-15, 15, 1000), np.ones(1000))
y = x.copy().T
z = (x ** 2) + (y ** 2)

def objective_func(x): # Known solution at position (0,0) and value of 0
    x_ = x[:, 0]
    y_ = x[:, 1]
    z = (x_ ** 2) + (y_ ** 2)
    
    return z

m = Mesher(func=objective_func)

# Figure
fig = plt.figure(figsize = (15, 15))
ax = plt.axes(projection = '3d')

# Optimization
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
optimizer = ps.single.GlobalBestPSO(n_particles=25, dimensions=2, options=options)
cost, pos = optimizer.optimize(objective_func, iters = 100)


# Create the plot
ax.plot_surface(x, y, z)
plt.show()