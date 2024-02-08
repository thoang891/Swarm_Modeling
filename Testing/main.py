import numpy as np
import matplotlib.pyplot as plt

from Buoy import Buoy
from Environment import Env

# Settings
timestep = 0.1
iterations = 1000
seeker_population = 5
explorer_population = 10

# Initialize Environment and Plot
env = Env(bounds=10, fidelity=2000, dt=timestep)
ax = plt.axes(projection='3d')

def construct_swarm(seeker_population = seeker_population, explorer_population = explorer_population):
    swarm = []

    for i in range(seeker_population):
        swarm.append(Buoy(i+1, timestep=timestep, behv="seeker"))
    
    for i in range(explorer_population):
        swarm.append(Buoy(i+1+seeker_population, timestep=timestep, behv="explorer"))

    return swarm

def surf_plot():
    ax.set_xlim(-env.bounds, env.bounds)
    ax.set_ylim(-env.bounds, env.bounds)
    ax.plot_surface(env.x_space, env.y_space, env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

def main(iters=iterations):
    swarm = construct_swarm()
    surf_plot()

    scatter_plots = []
    broadcast_data = []
    delay = 0.2
    total_time = iters*env.dt

    # Animation Loop
    for i in range(iters):
        # Clear the previous scatter plots
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        broadcast_data = [] # Clear the list for the new iteration

        print("Iteration: {0} Time Elapsed: {1:>10.2f} seconds/ {2:>10.2f} seconds".format(i, i*env.dt, total_time))
        print("***_ID_**************_Position_************_Measurement")

        # Building scatter plot and broadcast data
        for buoy in swarm:
            id = buoy.id
            behavior = buoy.behv
            x = buoy.position[0]
            y = buoy.position[1]
            z = buoy.measure()
            print("ID: {0:>2}, Behavior: {1}, Position: {2:>6.2f}, {3:>6.2f}, Measurement: {4:>6.2f}".format(id, behavior, x, y, z))

            buoy_data = {'ID': id, 'behv': behavior , 'x': x, 'y': y, 'Measurement': z}
            broadcast_data.append(buoy_data)
            
            if behavior == "seeker":
                scatter_plot = ax.scatter(x, y, z, c='r', marker='o')
            else:
                scatter_plot = ax.scatter(x, y, z, c='b', marker='o')
            scatter_plots.append(scatter_plot)

        print(" ")
        print("Broadcast Data")
        print("\n".join(str(data) for data in broadcast_data)) # Print broadcast data to be read by buoy
        print(" ")
        
        # Swarm operating loop
        for buoy in swarm:
            buoy.read_mail(broadcast_data)
            buoy.update()
         
        plt.pause(delay)
        print(" ")

    plt.show()

if __name__ == "__main__":
    main(iterations)
