import numpy as np
import matplotlib.pyplot as plt

from Buoy import Buoy
from Environment import Env
import time

env = Env()

def construct_swarm(population=5):
    swarm = []
    for i in range(population):
        swarm.append(Buoy(i+1))
    return swarm

def plot(duration=100): 
    # Plotting the surface
    fig = plt.figure(figsize=(7, 7))
    ax = plt.axes(projection='3d')
    ax.set_xlim(-env.bounds, env.bounds)
    ax.set_ylim(-env.bounds, env.bounds)
    ax.plot_surface(env.x_space, env.y_space, env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

    scatter_plots = []
    delay = 0.15

    # Animation Loop
    for i in range(duration):
        # Clear the previous scatter plots
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        print("Iteration: ", i+1)
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
