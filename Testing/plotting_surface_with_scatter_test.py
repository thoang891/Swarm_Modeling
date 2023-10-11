import numpy as np 
import matplotlib.pyplot as plt
import time
import random
#from mpl_toolkits import mplot3d

x = np.outer(np.linspace(-20, 20, 1000), np.ones(1000))
y = x.copy().T
z = np.sinh(x/5) * np.sin(y/5) * (x**2 + y**2)

fig = plt.figure(figsize=(14,9))
ax = plt.axes(projection='3d')

ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)

u = 0
v = 0

scatter_plot = None

for i in range(1000):
    u += random.uniform(-1,1)
    v += random.uniform(-1,1)
    w = np.sinh(u/5) * np.sin(v/5) * (u**2 + v**2)

    scatter_plot = ax.scatter(u, v, w, c='r', s=50, marker='o', depthshade=False)
    
    plt.pause(0.001)
    
    scatter_plot.remove()
    
    #time.sleep(0.01)

plt.show()

