import numpy as np
import matplotlib.pyplot as plt

from Buoy import Buoy
from Environment import Env
import time

timewarp = 0.5
env = Env(bounds=10, fidelity=2000, dt=timewarp)

def construct_swarm(population=5, behv="seeker"):
    swarm = []
    for i in range(population):
        swarm.append(Buoy(i+1, timewarp=timewarp))
    return swarm

def plot(iters=100): 
    # Plotting the surface
    fig = plt.figure(figsize=(7, 7))
    ax = plt.axes(projection='3d')
    ax.set_xlim(-env.bounds, env.bounds)
    ax.set_ylim(-env.bounds, env.bounds)
    ax.plot_surface(env.x_space, env.y_space, env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

    scatter_plots = []
    delay = 0.15

    # Animation Loop
    for i in range(iters):
        # Clear the previous scatter plots
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        print("Iteration: {0} Time Elapsed: {1:>10.2f} seconds".format(i, i*env.dt))
        print("***_ID_**************_Position_************_Measurement")

        for buoy in swarm:
            x = buoy.position[0]
            y = buoy.position[1]
            z = buoy.measure()
            print("ID: {0:>2}, Position: {1:>6.2f}, {2:>6.2f}, Measurement: {3:>6.2f}".format(buoy.id, x, y, z))

            scatter_plot = ax.scatter(x, y, z, c='r', marker='o') 
            scatter_plots.append(scatter_plot)

            buoy.update()
        plt.pause(delay)
        print(" ")

    plt.show()

if __name__ == "__main__":
    swarm = construct_swarm()
    plot(1000)
