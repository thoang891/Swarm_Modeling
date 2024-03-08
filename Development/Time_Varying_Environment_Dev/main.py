import matplotlib.pyplot as plt
import logger
import log_analyzer

import settings as set
from Swarm import Swarm

# Initialize the swarm, environment, and target
swarm = Swarm(seeker_pop=set.settings['seeker_population'],
                seeker_speed_number=set.settings['seeker_speed_number'],
                seeker_com_number=set.settings['seeker_com_number'],
                seeker_repulsion_number=set.settings['seeker_repulsion_number'],
                seeker_battery_number=set.settings['seeker_battery_number'],
                seeker_gps_accuracy=set.settings['seeker_gps_accuracy'],
                seeker_sensor_accuracy=set.settings['seeker_sensor_accuracy'],
                seeker_memory_duration=set.settings['seeker_memory_duration'],
                explorer_pop=set.settings['explorer_population'],
                explorer_speed_number=set.settings['explorer_speed_number'],
                explorer_com_number=set.settings['explorer_com_number'],
                explorer_repulsion_number=set.settings['explorer_repulsion_number'],
                explorer_battery_number=set.settings['explorer_battery_number'],
                explorer_gps_accuracy=set.settings['explorer_gps_accuracy'],
                explorer_sensor_accuracy=set.settings['explorer_sensor_accuracy'],
                explorer_memory_duration=set.settings['explorer_memory_duration'],
                iso_pop=set.settings['isocontour_population'],
                iso_speed_number=set.settings['iso_speed_number'],
                iso_com_number=set.settings['iso_com_number'],
                iso_repulsion_number=set.settings['iso_seeking_repulsion_number'],
                iso_seeking_repulsion_number=set.settings['iso_seeking_repulsion_number'],
                iso_spreading_repulsion_number=set.settings['iso_spreading_repulsion_number'],
                iso_battery_number=set.settings['iso_battery_number'],
                iso_gps_accuracy=set.settings['iso_gps_accuracy'],
                iso_sensor_accuracy=set.settings['iso_sensor_accuracy'],
                iso_memory_duration=set.settings['iso_memory_duration'],
                iso_goal=set.settings['isocontour_goal'],
                iso_thresh=set.settings['isocontour_threshold'],
                timestep=set.settings['timestep'],
                map_size=set.settings['map_size'],
                external_force_magnitude=set.settings['external_force_magnitude'],
                inertia=set.settings['inertia'],
                fidelity=set.settings['fidelity'],
                target_setting=set.settings['target_setting'],
                target_speed_number=set.settings['target_speed_number'])

env = swarm.env
if set.settings['animation']:
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
    
def clear_plot(surface_plot, scatter_plots, i):
    pass

def main(iters=set.settings['iterations'], log_folder=None):
    swarm.construct()
    if set.settings['animation']:
        surface_plot = surf_plot(None)
        scatter_plots = []

    total_time = iters*env.dt

    # Animation Loop
    for i in range(iters):
        if set.settings['animation']:
            if surface_plot is not None and i > set.settings['iterations'] - 1:
                surface_plot = None

            # Clear the previous scatter plots
            for plot in scatter_plots:
                plot.remove()
            scatter_plots = []  # Clear the list for the new iteration
            broadcast_data = [] # Clear the list for the new iteration

        current_time = round(i*env.dt, 2)

        print("#"*100)
        print("Iteration: {0} Time Elapsed: {1:>10.2f} seconds/ {2:>10.2f} seconds".format(i, current_time, total_time))
        print("#"*100)

        swarm.update(current_time)
        broadcast_data = swarm.broadcast_data
        if set.settings['target_setting'] == "ON":
            target_data = swarm.env.target.target_data
            all_data = broadcast_data + [target_data]
        else:
            all_data = broadcast_data

        logger.log_buoy_data(current_time, all_data, log_folder)

        if set.settings['animation']:
            surface_plot = surf_plot(surface_plot)
            scatter_plots = scatter_plot(scatter_plots, broadcast_data)

            plt.pause(set.settings['animation_delay'])
        print(" ")
    if set.settings['animation']:
        plt.show()

if __name__ == "__main__":
    log_folder = logger.create_log_folder()
    logger.log_settings(set.settings, folder_path=log_folder)
    main(set.settings['iterations'], log_folder)
    log_analyzer.main()
