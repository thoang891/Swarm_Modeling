from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import pyswarms as ps
from pyswarms.utils.plotters.formatters import Mesher

# Surface Data set
u = np.outer(np.linspace(-2, 2, 100), np.ones(100))
v = u.copy().T
w = (u ** 2) + (v ** 2)

def objective_func(x): # Known solution at position (0,0) and value of 0
    x_ = x[:, 0]
    y_ = x[:, 1]
    z = (x_ ** 2) + (y_ ** 2)
    
    return z

# m = Mesher(func=objective_func)

# Optimization
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
n_particles = 1
dimensions = 2
iters = 1000
optimizer = ps.single.GlobalBestPSO(n_particles= n_particles, dimensions= dimensions, options=options)
cost, pos = optimizer.optimize(objective_func, iters = iters)

# Extract position and cost history
pos_history = optimizer.pos_history
pos_history = np.array(pos_history)

x_vals = []
y_vals = []

for row in pos_history:
    x_vals.append(row[0, 0])
    y_vals.append(row[0, 1])

cost_history = optimizer.cost_history
cost_history = np.array(cost_history)

fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')

#ax.plot_surface(u, v ,w, cmap = 'Blues', alpha = 0.5, label='Surface')
    
for i in range(iters):
    plt.clf()
    
    x = x_vals[i]
    y = y_vals[i]
    z = cost_history[i]
    plt.scatter(x, y, z, c = 'b', marker='o', label="Particles")
    #plt.set_title('Particle positions at iteration {}'.format(i + 1))
    plt.pause(0.001)
    
# ax.set_xlim(-15,15)
# ax.set_ylim(-15,15)
# ax.set_zlim(0, 500)
    
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Z')
    
plt.show()







# # Figure
# fig = plt.figure()
# ax = fig.add_subplot(111, projection = '3d')
# ax.set_xlabel('X')
# ax.set_ylabel('Y')
# ax.set_zlabel('Objective Score')
# ax.set_xlim()

# bounds = (np.array([-1, -1]), np.array([1, 1]))
# ax.set_xlim(bounds[0][0], bounds[1][0])
# ax.set_ylim(bounds[0][1], bounds[1][1])

# # Initialize particles
# x = pos_history[0,:,0]
# y = pos_history[0,:,1]
# z = cost_history[0]
# particles = ax.scatter(x, y, z, c = 'b', marker='o', label="Particles")

# def animate(i):
#     x = pos_history[i,:,0]
#     y = pos_history[i,:,1]
#     z = cost_history[i]
#     particles._offsets3d = (x, y, z)
#     ax.set_title("Particle positions at iteration {}".format(i + 1))
    

# # Create animation
# ani = FuncAnimation(fig, animate, frames=pos_history.shape[0], interval = 200, repeat = False)
# plt.legend(loc='upper left')
# plt.show()

# # # Create the plot
# # ax.plot_surface(x, y, z)
# # plt.show()