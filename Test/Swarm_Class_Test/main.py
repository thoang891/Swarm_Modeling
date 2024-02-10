import numpy as np
import matplotlib.pyplot as plt

from Environment import Env
from Swarm import Swarm

# Settings
timestep = 0.1
iterations = 1000
map_size = 10
seeker_population = 5
explorer_population = 20

# Initialize Environment and Plot
env = Env(bounds=map_size, fidelity=2000, dt=timestep)
ax = plt.axes(projection='3d')
ax.set_xlim(-env.bounds, env.bounds)
ax.set_ylim(-env.bounds, env.bounds)

def surf_plot():
    ax.plot_surface(env.x_space, env.y_space, env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

def main(iters=iterations):
    swarm = Swarm(seeker_pop=seeker_population, explorer_pop=explorer_population, timestep=timestep, map_size=map_size)
    swarm.construct()
    surf_plot()

    scatter_plots = []
    delay = 0.2
    total_time = iters*env.dt

    # Swarm operating loop 
    for i in range(iters):
        # Clear the previous scatter plots
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        broadcast_data = [] # Clear the list for the new iteration

        print("#"*100)
        print("Iteration: {0} Time Elapsed: {1:>10.2f} seconds/ {2:>10.2f} seconds".format(i, i*env.dt, total_time))
        print("#"*100)

        swarm.update()
        broadcast_data = swarm.broadcast_data

        # Animation Loop
        for mail in broadcast_data:
            id = mail['ID']
            behavior = mail['behv']
            x = mail['x']
            y = mail['y']
            z = mail['Measurement']
           
            if behavior == "seeker":
                scatter_plot = ax.scatter(x, y, z, c='r', marker='o')
            else:
                scatter_plot = ax.scatter(x, y, z, c='b', marker='o')
            scatter_plots.append(scatter_plot)
         
        plt.pause(delay)
        print(" ")

    plt.show()

if __name__ == "__main__":
    main(iterations)
