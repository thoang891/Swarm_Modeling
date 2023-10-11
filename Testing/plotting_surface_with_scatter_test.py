import numpy as np 
import matplotlib.pyplot as plt
import time
#from mpl_toolkits import mplot3d

x = np.outer(np.linspace(-10, 10, 1000), np.ones(1000))
y = x.copy().T
z = np.sinh(x) * -1 * np.sinh(y)

fig = plt.figure(figsize=(14,9))
ax = plt.axes(projection='3d')

ax.plot_surface(x, y, z)

u = 0
v = 0

scatter_plot = None

for i in range(10):
    u += 1
    v += 1
    w = np.sinh(u) * -1 * np.sinh(v)

    scatter_plot = ax.scatter(u, v, w, c='r', marker='o')
    
    plt.pause(1)
    
    scatter_plot.remove()
    
    time.sleep(0.1)

plt.show()

