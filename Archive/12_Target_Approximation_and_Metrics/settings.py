# This file contains the settings for the simulation. 
# The settings are used to configure the simulation environment and the swarm population.

settings = {
    # Animation and Iteration Settings
    "animation": False, # True or False
    "animation_delay": 0.001,
    "timestep": 0.1,
    "iterations": 1000,

    # Environment Settings
    "map_size": 15,
    "external_force_magnitude": 0,
    "fidelity": 100,

    # Target Settings
    "target_setting": "ON", # "ON" or "OFF"
    "target_speed": 4,

    # Seeker Population Settings
    "seeker_population": 4,
    "seeker_speed": 2,
    "seeker_com_radius": 7,
    "seeker_repulsion_radius": 0.5,
    "seeker_battery": 47520,
    "seeker_gps_accuracy": 1,
    "seeker_sensor_accuracy": 3,
    "seeker_memory_duration": 1,

    # Explorer Population Settings
    "explorer_population": 15,
    "explorer_speed": 2,
    "explorer_com_radius": 10,
    "explorer_repulsion_radius": 9,
    "explorer_battery": 47520,
    "explorer_gps_accuracy": 1,
    "explorer_sensor_accuracy": 1,
    "explorer_memory_duration": 5,

    # Isocontour Population Settings
    "isocontour_population": 20,
    "iso_speed": 1.5,
    "iso_com_radius": 7,
    "iso_repulsion_radius": 4.5,
    "iso_battery": 47520,
    "iso_gps_accuracy": 1,
    "iso_sensor_accuracy": 1,
    "iso_memory_duration": 5,
    "isocontour_goal": -100,
    "isocontour_threshold": 2,
}