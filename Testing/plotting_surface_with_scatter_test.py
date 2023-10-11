import numpy as np 
import matplotlib.pyplot as plt
import time
import random
#from mpl_toolkits import mplot3d

x = np.outer(np.linspace(-10, 10, 1000), np.ones(1000))
y = x.copy().T

fig = plt.figure(figsize=(14, 9))
ax = plt.axes(projection='3d')
ax.set_xlim(-20, 20)
ax.set_ylim(-20, 20)

u = 0
v = 0

scatter_plot = None
surface_plot = None

for i in range(100):
    u += random.uniform(-1,1)
    v += random.uniform(-1,1)
    w = np.sinc((u + float(i)/10) * v)

    z = np.sinc((x + float(i)/10) * y)
    print(z)
    surface_plot = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)
    scatter_plot = ax.scatter(u, v, w, c='r', s=50, marker='o', depthshade=False)
    
    plt.pause(0.001)
    
    if scatter_plot is not None and i < 99:
        scatter_plot.remove()

    if surface_plot is not None and i < 99:
        surface_plot.remove()
    
    time.sleep(0.01)

plt.show()

