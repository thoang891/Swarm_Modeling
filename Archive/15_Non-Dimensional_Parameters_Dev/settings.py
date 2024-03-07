# This file contains the settings for the simulation. 
# The settings are used to configure the simulation environment and the swarm population.

settings = {
    # Animation and Iteration Settings
    "animation": True, # True or False
    "animation_delay": 0.0001,
    "timestep": 0.1,
    "iterations": 1000,

    # Environment Settings
    "map_size": 15,
    "external_force_magnitude": 0,
    "fidelity": 200,
    "scalar": 6,

    # Target Settings
    "target_setting": "ON", # "ON" or "OFF"
    "target_speed_number": 0.4,

    # Seeker Population Settings
    "seeker_population": 5,
    "seeker_speed_number": 0.1,
    "seeker_com_number": 1.2,
    "seeker_repulsion_number": 0.1,
    "seeker_battery_number": 1,
    "seeker_gps_accuracy": 1,
    "seeker_sensor_accuracy": 3,
    "seeker_memory_duration": 1,

    # Explorer Population Settings
    "explorer_population": 10,
    "explorer_speed_number": 0.1,
    "explorer_com_number": 2,
    "explorer_repulsion_number": 1.5,
    "explorer_battery_number": 0.5,
    "explorer_gps_accuracy": 1,
    "explorer_sensor_accuracy": 3,
    "explorer_memory_duration": 5,

    # Isocontour Population Settings
    "isocontour_population": 15,
    "iso_speed_number": 0.2,
    "iso_com_number": 1.5,
    "iso_seeking_repulsion_number": 0.1,
    "iso_spreading_repulsion_number": 1.3,
    "iso_battery_number": 1,
    "iso_gps_accuracy": 1,
    "iso_sensor_accuracy": 3,
    "iso_memory_duration": 5,
    "isocontour_goal": 0.3,
    "isocontour_threshold": 0.01,
}