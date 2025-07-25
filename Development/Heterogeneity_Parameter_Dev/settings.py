# This file contains the settings for the simulation. 
# The settings are used to configure the simulation environment and the swarm population.

settings = {
    # Animation and Iteration Settings
    "animation": True, # True or False
    "animation_delay": 0.01,
    "timestep": 0.1,
    "iterations": 100,

    # Environment Settings
    "map_size": 20,
    "external_force_magnitude": 0,
    "fidelity": 200,
    "scalar": 5,
    "inertia": 0.15,
    "decay": 0.4,
    "scalar_duration": 10,
    "relative_strength": 8,

    # Target Settings
    "target_setting": "ON", # "ON" or "OFF"
    "target_speed_number": 0.18,

    # Swarm Population Settings
    "set_by_fraction": True, # True or False
    "mission": "search", # "search" or "isocontour"
    "population": 25,
    "heterogeneiety_coefficient": 0.5,

    # Seeker Population Settings
    "seeker_population": 4,
    "seeker_speed_number": 0.1,
    "seeker_com_number": 1.5,
    "seeker_repulsion_number": 0.1,
    "seeker_battery_number": 1,
    "seeker_gps_accuracy": 1,
    "seeker_sensor_accuracy": 3,
    "seeker_memory_duration": 1,

    # Explorer Population Settings
    "explorer_population": 20,
    "explorer_speed_number": 0.1,
    "explorer_com_number": 2,
    "explorer_repulsion_number": 1.9,
    "explorer_battery_number": 1,
    "explorer_gps_accuracy": 1,
    "explorer_sensor_accuracy": 3,
    "explorer_memory_duration": 0.5,

    # Isocontour Population Settings
    "isocontour_population": 0,
    "iso_speed_number": 0.1,
    "iso_com_number": 1.5,
    "iso_seeking_repulsion_number": 0.1,
    "iso_spreading_repulsion_number": 1.3,
    "iso_battery_number": 1,
    "iso_gps_accuracy": 1,
    "iso_sensor_accuracy": 3,
    "iso_memory_duration": 2,
    "isocontour_goal": 0.5,
    "isocontour_threshold": 0.01,
}