# # Animation and Iteration Settings
# animation = True # Set to False to disable animation
# animation_delay = 0.001 # lower is faster
# timestep = 0.1
# iterations = 1000

# # Environment Settings
# map_size = 10
# external_force_magnitude = 0.1
# fidelity = 100

# # Target Settings
# target_setting = "ON" # "ON" or "OFF"
# target_speed = 10

# # Swarm Population Settings
# seeker_population = 1
# explorer_population = 1
# isocontour_population = 1

# # Swarm Performance Settings
# communication_radius = 7
# isocontour_goal = -80
# isocontour_threshold = 3
# speed = 1.5
# battery = 47520
# gps_accuracy = 1 # Control decimal places of GPS coordinates. Minimum is 1.
# sensor_accuracy = 1 # Control decimal places of sensor measurements. Minimum is 1.
# memory_duration = 1 # How long a buoy can remember the best measurement in seconds.

settings = {
    # Animation and Iteration Settings
    "animation": True,
    "animation_delay": 0.001,
    "timestep": 0.1,
    "iterations": 1000,

    # Environment Settings
    "map_size": 10,
    "external_force_magnitude": 0.1,
    "fidelity": 100,

    # Target Settings
    "target_setting": "ON",
    "target_speed": 10,

    # Swarm Population Settings
    "seeker_population": 1,
    "explorer_population": 1,
    "isocontour_population": 1,

    # Swarm Performance Settings
    "communication_radius": 7,
    "isocontour_goal": -80,
    "isocontour_threshold": 3,
    "speed": 1.5,
    "battery": 47520,
    "gps_accuracy": 1,
    "sensor_accuracy": 1,
    "memory_duration": 1
}