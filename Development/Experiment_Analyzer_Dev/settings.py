# This file contains the settings for the simulation. 
# The settings are used to configure the simulation environment and the swarm population.

settings = {
    # Animation and Iteration Settings
    "animation": False, # True or False
    "animation_delay": 0.01,
    "timestep": 0.1,
    "iterations": 1500,

    # Environment Settings
    "map_size": 25,
    "external_force_magnitude": 0,
    "fidelity": 200,
    "scalar": 1,
    "inertia": 0.15,
    "decay": 0.5,
    "scalar_duration": 2,
    "relative_strength": 2,

    # Target Settings
    "target_setting": "ON", # "ON" or "OFF"
    "target_speed_number": 0.2,

    # Seeker Population Settings
    "seeker_population": 0,
    "seeker_speed_number": 0.1,
    "seeker_com_number": 2,
    "seeker_repulsion_number": 0.1,
    "seeker_battery_number": 1,
    "seeker_gps_accuracy": 1,
    "seeker_sensor_accuracy": 3,
    "seeker_memory_duration": 1,

    # Explorer Population Settings
    "explorer_population": 0,
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
    "isocontour_goal": 0.2,
    "isocontour_threshold": 0.01,
}

behavior = {
    "seeker": {
        "A": 1,
        "B": 3,
        "C": 3,
        "D": 0.5,
        "E": 0,
    },
    "explorer": {
        "A": 0.05,
        "B": 0.05,
        "C": 1,
        "D": 1,
        "E": 0,
    },
    "isocontour": {
        "A": 0.05,
        "B": 0.1,
        "C": 1,
        "D": 0.5,
        "E": 1,
    }
}