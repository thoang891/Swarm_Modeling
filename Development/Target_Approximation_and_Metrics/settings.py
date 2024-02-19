# This file contains the settings for the simulation. 
# The settings are used to configure the simulation environment and the swarm population.

settings = {
    # Animation and Iteration Settings
    "animation": False, # True or False
    "animation_delay": 0.001,
    "timestep": 0.1,
    "iterations": 1000,

    # Environment Settings
    "map_size": 10,
    "external_force_magnitude": 0,
    "fidelity": 100,

    # Target Settings
    "target_setting": "ON", # "ON" or "OFF"
    "target_speed": 10,

    # Seeker Population Settings
    "seeker_population": 5,
    "seeker_speed": 4,
    "seeker_com_radius": 5,
    "seeker_battery": 47520,
    "seeker_gps_accuracy": 1,
    "seeker_sensor_accuracy": 3,
    "seeker_memory_duration": 1,

    # Explorer Population Settings
    "explorer_population": 5,
    "explorer_speed": 2,
    "explorer_com_radius": 10,
    "explorer_battery": 47520,
    "explorer_gps_accuracy": 1,
    "explorer_sensor_accuracy": 1,
    "explorer_memory_duration": 5,

    # Isocontour Population Settings
    "isocontour_population": 5,
    "iso_speed": 10,
    "iso_com_radius": 6,
    "iso_battery": 47520,
    "iso_gps_accuracy": 1,
    "iso_sensor_accuracy": 1,
    "iso_memory_duration": 1,
    "isocontour_goal": -80,
    "isocontour_threshold": 3,
}