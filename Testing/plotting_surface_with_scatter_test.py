import numpy as np 
import matplotlib.pyplot as plt
import random
#from mpl_toolkits import mplot3d

x = np.outer(np.linspace(-10, 10, 1000), np.ones(1000))
y = x.copy().T

fig = plt.figure(figsize=(14, 9))
ax = plt.axes(projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)

u = 0
v = 0

scatter_plot = None
surface_plot = None

for i in range(1000):
    u += random.uniform(-0.1,0.1)
    v += random.uniform(-0.1,0.1)
    w = np.sinc(u * np.cos(float(i)/100)) + np.sinc(v * np.sin(float(i)/100)) + (np.cos(u * v * np.sin(float(i)/100)) / 10)

    z = np.sinc(x * np.cos(float(i)/100)) + np.sinc(y * np.sin(float(i)/100)) + (np.cos(x * y * np.sin(float(i)/100)) / 10)
    print(z)
    surface_plot = ax.plot_surface(x, y, z, cmap='viridis', alpha=0.5)
    scatter_plot = ax.scatter(u, v, w, c='r', s=50, marker='o', depthshade=False)
    
    plt.pause(0.001)
    
    if scatter_plot is not None and i < 999:
        scatter_plot.remove()

    if surface_plot is not None and i < 999:
        surface_plot.remove()
    
   # time.sleep(0.01)

plt.show()

