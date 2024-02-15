import matplotlib.pyplot as plt

from Swarm import Swarm

# Animation and Iteration Settings
animation = False # Set to False to disable animation
animation_delay = 0.001 # lower is faster
timestep = 0.1
iterations = 10000

# Environment Settings
map_size = 10
external_force_magnitude = 0.1
fidelity = 100

# Target Settings
target_setting = "ON" # "ON" or "OFF"
target_speed = 10

# Swarm Population Settings
seeker_population = 1
explorer_population = 1
isocontour_population = 1

# Swarm Performance Settings
communication_radius = 7
isocontour_goal = -80
isocontour_threshold = 3
speed = 1.5
battery = 47520
gps_accuracy = 1 # Control decimal places of GPS coordinates. Minimum is 1.
sensor_accuracy = 1 # Control decimal places of sensor measurements. Minimum is 1.
memory_duration = 1 # How long a buoy can remember the best measurement in seconds.

# Initialize Environment, Swarm, and Target
swarm = Swarm(seeker_pop=seeker_population, explorer_pop=explorer_population, 
                iso_pop=isocontour_population, com_radius=communication_radius, 
                speed=speed, battery = battery, timestep=timestep, map_size=map_size, 
                iso_goal=isocontour_goal, gps_accuracy=gps_accuracy, sensor_accuracy=sensor_accuracy,
                external_force_magnitude=external_force_magnitude, memory_duration=memory_duration,
                fidelity=fidelity, target_setting=target_setting, target_speed=target_speed)

env = swarm.env
if animation:
    ax = plt.axes(projection='3d')
    ax.set_xlim(-env.bounds, env.bounds)
    ax.set_ylim(-env.bounds, env.bounds)

def surf_plot(surface_plot):
    if surface_plot is not None:
        surface_plot.remove()
    surface_plot = ax.plot_surface(env.x_space, env.y_space, 
                    env.z_space, cmap='viridis', alpha=0.5) # Plot the surface
    return surface_plot

def scatter_plot(scatter_plots, broadcast_data):
    if broadcast_data is not None:
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

        if env.target_setting == "ON":
            x_targ = env.target.position[0]
            y_targ = env.target.position[1]
            z_targ = env.scalar(x_targ, y_targ)

            scatter_plot = ax.scatter(x_targ, y_targ, z_targ, c='r', marker='x', depthshade=False)
            scatter_plots.append(scatter_plot)

        return scatter_plots

def main(iters=iterations):
    swarm.construct()
    if animation:
        surface_plot = surf_plot(None)
        scatter_plots = []

    total_time = iters*env.dt

    # Animation Loop
    for i in range(iters):
        if animation:
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
        
        if animation:
            surface_plot = surf_plot(surface_plot)
            scatter_plots = scatter_plot(scatter_plots, broadcast_data)

            plt.pause(animation_delay)
        print(" ")
    if animation:
        plt.show()

if __name__ == "__main__":
    main(iterations)
