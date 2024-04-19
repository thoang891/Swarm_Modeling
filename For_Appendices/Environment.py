import numpy as np
import settings as set
import scalar_library

from Target import Target

import inspect

import os

# Library for scalar functions
scalar_function = {
    1: scalar_library.scalar_1,
}

class Env():

    def __init__(self, bounds=10, fidelity=200, dt=0.1, external_force_magnitude=0.25, Target_Setting="ON", target_speed_number=3, inertia=0.5, decay=0.9, scalar_duration=5, relative_strength=6):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T
        self.dt = dt
        self.external_force_magnitude = external_force_magnitude
        self.z_space = self.scalar(self.x_space, self.y_space)
        self.env_hist = []
        self.target_setting = Target_Setting
        self.decay = decay
        self.scalar_duration = scalar_duration
        if self.target_setting == "ON":
            self.target = Target(timestep=dt, bounds=bounds, speed_number=target_speed_number, inertia=inertia)
            self.target.set_speed()
            self.target.behv()

    @staticmethod
    def scalar(x, y, timestamp=0): 
        z = scalar_function[set.settings['scalar']](x, y, timestamp=timestamp)
        return z
            
    def external_force(self, x, y):
        # vector field that simulates a force field due to wind or current.
        force = [np.cos(x), np.sin(y)]
        magnitude = np.linalg.norm(force)

        if abs(magnitude) != 0:
            scaled_force = (force/magnitude)*self.external_force_magnitude

        else:
            scaled_force = [0, 0]
        
        return scaled_force
    
    def update_z_space(self):
        self.z_space = self.scalar(self.x_space, self.y_space)
        return self.z_space

    def update_scalar(self, current_time):
        tar_pos_x = self.target.position[0]
        tar_pos_y = self.target.position[1]
        timestamp = current_time

        new_scalar = lambda x, y, current_time: scalar_function[set.settings['scalar']](x, y, timestamp=timestamp, center_x=tar_pos_x, center_y=tar_pos_y, current_time=current_time)
        new_scalar_decayed = lambda x, y, current_time: new_scalar(x, y, current_time=current_time)

        self.env_hist.append(new_scalar_decayed)

        current_scalar = lambda x, y: scalar_function[set.settings['scalar']](x-tar_pos_x, y-tar_pos_y, timestamp=0)

        if len(self.env_hist) > self.scalar_duration/self.dt:
            self.env_hist.pop(0)

        # Define the scalar function as the sum of the updated history and the current scalar
        self.scalar = lambda x, y: sum(scalar_func(x, y, current_time) for scalar_func in self.env_hist) + current_scalar(x, y)

        return self.scalar

    def update(self, current_time):
        if self.target_setting == "ON":
            self.update_scalar(current_time)
            self.update_z_space()
            self.target.update(self)
