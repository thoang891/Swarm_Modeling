import matplotlib.pyplot as plt

from Environment import Env
from Swarm import Swarm

# Animation and Iteration Settings
animation_delay = 0.1 # lower is faster
timestep = 0.1
iterations = 10000

# Environment Settings
map_size = 10
external_force_magnitude = 0.1

# Swarm Population Settings
seeker_population = 1
explorer_population = 1
isocontour_population = 1

# Swarm Performance Settings
communication_radius = 7
isocontour_goal = -80
isocontour_threshold = 1
speed = 1.5
battery = 47520
gps_accuracy = 1 # Control decimal places of GPS coordinates. Minimum is 1.
sensor_accuracy = 1 # Control decimal places of sensor measurements. Minimum is 1.
memory_duration = 2 # How long a buoy can remember the best measurement in seconds.

# Initialize Environment and Plot
env = Env(bounds=map_size, fidelity=100, dt=timestep)
ax = plt.axes(projection='3d')
ax.set_xlim(-env.bounds, env.bounds)
ax.set_ylim(-env.bounds, env.bounds)

def surf_plot(surface_plot):
    if surface_plot is not None:
        surface_plot.remove()
    surface_plot = ax.plot_surface(env.x_space, env.y_space, 
                    env.z_space, cmap='viridis', alpha=0.5) # Plot the surface
    return surface_plot

def main(iters=iterations):
    swarm = Swarm(seeker_pop=seeker_population, explorer_pop=explorer_population, 
                  iso_pop=isocontour_population, com_radius=communication_radius, 
                  speed=speed, battery = battery, timestep=timestep, map_size=map_size, 
                  iso_goal=isocontour_goal, gps_accuracy=gps_accuracy, sensor_accuracy=sensor_accuracy,
                  external_force_magnitude=external_force_magnitude, memory_duration=memory_duration)
    
    swarm.construct()
    surface_plot = surf_plot(None)

    scatter_plots = []
    # surface_plot = None
    total_time = iters*env.dt

    # Animation Loop
    for i in range(iters):

        if surface_plot is not None and i > iterations - 1:
            surface_plot = None

        # Clear the previous scatter plots
        for plot in scatter_plots:
            plot.remove()
        scatter_plots = []  # Clear the list for the new iteration
        broadcast_data = [] # Clear the list for the new iteration
        current_time = i*env.dt

        print("#"*100)
        print("Iteration: {0} Time Elapsed: {1:>10.2f} seconds/ {2:>10.2f} seconds".format(i, current_time, total_time))
        print("#"*100)

        swarm.update(current_time)
        broadcast_data = swarm.broadcast_data
        env.update()

        surface_plot = surf_plot(surface_plot)

        for mail in broadcast_data:
            id = mail['ID']
            behavior = mail['behv']
            x = mail['x']
            y = mail['y']
            z = mail['Measurement']
           
            if behavior == "seeker":
                scatter_plot = ax.scatter(x, y, z, c='r', marker='.')
            elif behavior == "explorer":
                scatter_plot = ax.scatter(x, y, z, c='b', marker='.')
            elif behavior == "isocontour":
                scatter_plot = ax.scatter(x, y, z, c='g', marker='.')
            scatter_plots.append(scatter_plot)

        x_targ = env.target.position[0]
        y_targ = env.target.position[1]
        z_targ = env.scalar(x_targ, y_targ)

        scatter_plot = ax.scatter(x_targ, y_targ, z_targ, c='r', marker='x', depthshade=False)
        scatter_plots.append(scatter_plot)
        plt.pause(animation_delay)
        print(" ")

    plt.show()

if __name__ == "__main__":
    main(iterations)
