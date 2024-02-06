# Import modules
import numpy as np
import matplotlib.pyplot as plt
import pyswarms.backend as P
from pyswarms.backend import topology as top

# Create surface array
x_space = np.outer(np.linspace(-10, 10, 2000), np.ones(2000))
y_space = x_space.copy().T

# Objective function where x and y are define the spatial dimension and i is the iteration/time varying parameter
def f(x, y, i):
    # z = ((x + np.cos(float(i)/3))**2 + (y + np.sin(float(i)/3))**2)
    z = (np.sinc((x + np.cos(float(i)))/2) + np.sinc((y - np.sin(float(i)))/2) + (np.cos(x * y * np.sin(float(i)/100)))) * -1
    return z

# Optimization variables where c1 and c2 are the cognitive and social parameters, w is the inertia parameter, and n_particles is the number of particles
options = {'c1': 0.3, 'c2': 0.3, 'w': 0.5}
n_particles = 25
dimensions = 2
iters = 1000
max_bounds = 10 * np.ones(dimensions)
min_bounds = -max_bounds
iterations = 1000
bounds = (min_bounds, max_bounds)
my_topology = top.Ring()

# Create a swarm instance
my_swarm = P.create_swarm(n_particles=n_particles, dimensions=dimensions, options=options, bounds=bounds)

# Create empty lists for each particle
pos_history = []

# Optimization Loop
for j in range(iterations):
    # Part 1: Simulate a moving surface/target
    # Define dynamic objective function for swarm
    def objective_func(x, j=j):
        x_ = x[:, 0]
        y_ = x[:, 1]
        z = f(x_, y_, j)
        return z
    
    #Part 2: Update personal best
    my_swarm.current_cost = objective_func(my_swarm.position) # Compute current cost
    my_swarm.pbest_cost = objective_func(my_swarm.pbest_pos) # Compute personal best pos
    my_swarm.pbest_pos, my_swarm.pbest_cost = P.compute_pbest(my_swarm) # Update and store

    pos_history.append(my_swarm.position)
    
    # Part 3: Update global best (defined as minimum of personal best)
    if np.min(my_swarm.pbest_cost) < my_swarm.best_cost:
        my_swarm.best_pos, my_swarm.best_cost = my_topology.compute_gbest(my_swarm, p=2, k=3)

    print("Iteration: {} | my_swarm.best_pos: {}".format(j+1, my_swarm.best_pos))
    print("Iteration: {} | my_swarm.best_cost: {:.4f}".format(j+1, my_swarm.best_cost))

    # Part 4: Update position and velocity matrices
    my_swarm.velocity = my_topology.compute_velocity(my_swarm)
    my_swarm.position = my_topology.compute_position(my_swarm)

print("The best position found by our swarm is: {}".format(my_swarm.best_pos))
print("The best cost found by our swarm is: {:.4f}".format(my_swarm.best_cost))

# Create a 3D plot and animation
delay = 0.01
fig = plt.figure(figsize=(7, 7))
ax = plt.axes(projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.set_zlim(-3, 3)

# Extract x and y values from position history
pos_history_array = np.array(pos_history)

x_vals = [[] for _ in range(n_particles)] 
y_vals = [[] for _ in range(n_particles)]

for i in range(iters):
    for j in range(n_particles):
        x_pos = pos_history_array[i, j, 0]
        y_pos = pos_history_array[i, j, 1]
        x_vals[j].append(x_pos)
        y_vals[j].append(y_pos)

scatter_plots = []
surface_plot = None

# Animation Loop
for i in range(iterations):
    # Refresh plots
    if surface_plot is not None and i < iterations - 1:
        surface_plot.remove()

    for plot in scatter_plots:
        plot.remove()
    scatter_plots = []

    # Plot surface
    z_space = f(x_space, y_space, i=i)
    surface_plot = ax.plot_surface(x_space, y_space, z_space, cmap='viridis', alpha=0.5)

    # Plot particles
    for particle_index in range(n_particles):
        x = x_vals[particle_index][i]
        y = y_vals[particle_index][i]
        z = f(x, y, i=i)

        scatter_plot = ax.scatter(x, y, z, c='b', s=50, marker='o', depthshade=False)
        scatter_plots.append(scatter_plot)
    
    plt.pause(delay)

plt.show()
