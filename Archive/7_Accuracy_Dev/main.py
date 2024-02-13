import matplotlib.pyplot as plt

from Environment import Env
from Swarm import Swarm

# Animation and Iteration Settings
animation_delay = 0.001 # lower is faster
timestep = 0.1
iterations = 10000

# Environment Settings
map_size = 10

# Swarm Population Settings
seeker_population = 5
explorer_population = 20
isocontour_population = 0

# Swarm Performance Settings
communication_radius = 10
isocontour_goal = -80
isocontour_threshold = 5
speed = 3
battery = 47520
gps_accuracy = 1 # Control decimal places of GPS coordinates. Minimum is 1.
sensor_accuracy = 1 # Control decimal places of sensor measurements. Minimum is 1.

# Initialize Environment and Plot
env = Env(bounds=map_size, fidelity=2000, dt=timestep)
ax = plt.axes(projection='3d')
ax.set_xlim(-env.bounds, env.bounds)
ax.set_ylim(-env.bounds, env.bounds)

def surf_plot():
    ax.plot_surface(env.x_space, env.y_space, 
                    env.z_space(), cmap='viridis', alpha=0.5) # Plot the surface

def main(iters=iterations):
    swarm = Swarm(seeker_pop=seeker_population, explorer_pop=explorer_population, 
                  iso_pop=isocontour_population, com_radius=communication_radius, 
                  speed=speed, battery = battery, timestep=timestep, map_size=map_size, 
                  iso_goal=isocontour_goal, gps_accuracy=gps_accuracy, sensor_accuracy=sensor_accuracy)
    
    swarm.construct()
    surf_plot()

    scatter_plots = []
    total_time = iters*env.dt

    # Animation Loop
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

        for mail in broadcast_data:
            id = mail['ID']
            behavior = mail['behv']
            x = mail['x']
            y = mail['y']
            z = mail['Measurement']
           
            if behavior == "seeker":
                scatter_plot = ax.scatter(x, y, z, c='r', marker='o')
            elif behavior == "explorer":
                scatter_plot = ax.scatter(x, y, z, c='b', marker='o')
            elif behavior == "isocontour":
                scatter_plot = ax.scatter(x, y, z, c='g', marker='o')
            scatter_plots.append(scatter_plot)

        plt.pause(animation_delay)
        print(" ")

    plt.show()

if __name__ == "__main__":
    main(iterations)
