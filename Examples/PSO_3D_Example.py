# 3D Example of PSO algorithm

import numpy as np
import pyswarms as ps
from pyswarms.utils.functions.single_obj import rosenbrock
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Define the optimziation problem
objective_function = rosenbrock
n_dim = 2 # Number of dimensions
bounds = (np.array([-5.12,-5.12]), np.array([5.12,5.12])) # Bounds of the problem

# Initialiazation of PSO parameters
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9, 'k': 30, 'p': 2}

# Create a swarm of 50 particles
num_particles = 25
optimizer = ps.single.GlobalBestPSO(n_particles=num_particles, dimensions=n_dim, options=options, bounds=bounds)

# Optimize the Rosenbrock function
best_position, best_value = optimizer.optimize(objective_function, iters=1000)

print("Optimal solution found at position: {}".format(best_position))
print("Objective function value at optimal solution: {}".format(best_value))

# Extract position history from optimizer
pos_history = optimizer.pos_history
pos_history = np.array(pos_history)

# Create a figure and 3D axis for the animation
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Objective Score')
ax.set_xlim(bounds[0][0], bounds[1][0])
ax.set_ylim(bounds[0][1], bounds[1][1])

# Initilize particles
x = pos_history[0,:,0]
y = pos_history[0,:,1]
z = [objective_function(p) for p in pos_history[0]]
particles = ax.scatter(x, y, z, c = 'b', marker='o', label="Particles")

def animate(i):
    x = pos_history[i,:,0]
    y = pos_history[i,:,1]
    z = [objective_function(p) for p in pos_history[i]]
    particles._offsets3d = (x, y, z)
    ax.set_title("Particle positions at iteration {}".format(i + 1))

# Create the animation
ani = FuncAnimation(fig, animate, frames=pos_history.shape[0], interval=200, repeat=False)
plt.legend(loc='upper left')
plt.show()