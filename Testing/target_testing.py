import numpy as np
import matplotlib.pyplot as plt

from Target import Target
from Environment import Env


# Settings
timestep = 0.1
iterations = 1000
map_size = 10

# Initialize Environment and Plot
env = Env(bounds=map_size, fidelity=50, dt=timestep)
ax = plt.axes(projection='3d')
ax.set_xlim(-env.bounds, env.bounds)
ax.set_ylim(-env.bounds, env.bounds)

# def construct_targ():
target = Target()

def surf_plot():
    surface_plot = ax.plot_surface(env.x_space, env.y_space, env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

def main(iters=iterations):
    # surf_plot()

    scatter_plots = []
    surface_plot = []
    delay = 0.2

    for i in range(iters):
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        if surface_plot is not None and i < iters -1:
            for plot in surface_plot:
                plot.remove()

        surf_plot()

        x = env.targ.position[0]
        y = env.targ.position[1]
        z = env.scalar(x, y)

        scatter_plot = ax.scatter(x, y, z, c='r', marker='o')
        scatter_plots.append(scatter_plot)

        env.z_space()
        plt.pause(delay)

    plt.show()

if __name__ == "__main__":
    main(iterations)