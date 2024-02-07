import numpy as np
import matplotlib.pyplot as plt

from Buoy import Buoy
from Environment import Env
import time

# Settings
timewarp = 1
iterations = 100

# Initialize Environment and Plot
env = Env(bounds=10, fidelity=2000, dt=timewarp)
ax = plt.axes(projection='3d')

def construct_swarm(population=5, behv="seeker"):
    swarm = []
    for i in range(population):
        swarm.append(Buoy(i+1, timewarp=timewarp))
    return swarm

def surf_plot():
    ax.set_xlim(-env.bounds, env.bounds)
    ax.set_ylim(-env.bounds, env.bounds)
    ax.plot_surface(env.x_space, env.y_space, env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

def broadcast():
    pass

def main(iters=iterations):
    swarm = construct_swarm()
    surf_plot()

    scatter_plots = []
    delay = 0.15
    broadcast = []

    # Animation Loop
    for i in range(iters):
        # Clear the previous scatter plots
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        broadcast_data = []

        print("Iteration: {0} Time Elapsed: {1:>10.2f} seconds".format(i, i*env.dt))
        print("***_ID_**************_Position_************_Measurement")

        # Building scatter plot and broadcast data
        for buoy in swarm:
            id = buoy.id
            x = buoy.position[0]
            y = buoy.position[1]
            z = buoy.measure()
            print("ID: {0:>2}, Position: {1:>6.2f}, {2:>6.2f}, Measurement: {3:>6.2f}".format(id, x, y, z))

            # buoy_data = [id, x, y, z]
            buoy_data = {'ID': id, 'x': x, 'y': y, 'Measurement': z}
            broadcast_data.append(buoy_data)

            scatter_plot = ax.scatter(x, y, z, c='r', marker='o') 
            scatter_plots.append(scatter_plot)

        # Swarm operating loop
        for buoy in swarm:
            buoy.update()
        
        print(broadcast_data) #Testing dataframe
         
        plt.pause(delay)
        print(" ")

    plt.show()

if __name__ == "__main__":
    main(1000)
