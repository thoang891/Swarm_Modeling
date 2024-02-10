
import numpy as np
import matplotlib.pyplot as plt

import pyswarms as ps

# Surface Data set
x_space = np.outer(np.linspace(-10, 10, 2000), np.ones(2000))
y_space = x_space.copy().T

# Objective Function
def fx(x, y):
    return (np.sinc(x) + np.sinc(y) + (np.cos(x * y) / 10)) * -1
    
#Objective Function for Swarm

def objective_func(x): # Known solution at position (0,0)
    x_ = x[:, 0]
    y_ = x[:, 1]
    z = fx(x_, y_)
    return z

# Optimize
options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
n_particles = 25
dimensions = 2
iters = 1000
max_bounds = 10 * np.ones(dimensions)
min_bounds = -max_bounds
bounds = (min_bounds, max_bounds)
optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=dimensions, options=options, bounds=bounds)
cost, pos = optimizer.optimize(objective_func, iters=iters)

# Extract position and cost history
pos_history = optimizer.pos_history
pos_history = np.array(pos_history)
print(pos_history.shape)

cost_history = optimizer.cost_history
cost_history = np.array(cost_history)


# Initilize empty lists for position values

x_vals = [[] for _ in range(n_particles)]  # Create empty lists for each particle
y_vals = [[] for _ in range(n_particles)]

# Extract x and y values from position history
for i in range(iters):
    for j in range(n_particles):
        x_pos = pos_history[i, j, 0]
        y_pos = pos_history[i, j, 1]
        x_vals[j].append(x_pos)
        y_vals[j].append(y_pos)

# Plotting and animation
fig = plt.figure(figsize=(7, 7))
ax = plt.axes(projection='3d')
ax.set_xlim(-10, 10)
ax.set_ylim(-10, 10)
ax.plot_surface(x_space, y_space, fx(x_space, y_space), cmap='viridis', alpha=0.5)

scatter_plots = []
delay = 0.15

for i in range(iters):
    # Clear the previous scatter plots
    for plot in scatter_plots:
        plot.remove()
    scatter_plots = []  # Clear the list for the new iteration

    for particle_index in range(n_particles):
        x = x_vals[particle_index][i]
        y = y_vals[particle_index][i]
        fx(x, y)

        scatter_plot = ax.scatter(x, y, fx(x, y), c='b', s=50, marker='o', depthshade=False)
        scatter_plots.append(scatter_plot)

    plt.pause(delay)

plt.show()
