import numpy as np
import settings as set
import scalar_library

from Target import Target

# Library for scalar functions

scalar_function = {
    1: scalar_library.scalar_1,
    2: scalar_library.scalar_2,
    3: scalar_library.scalar_3,
    4: scalar_library.scalar_4,
    5: scalar_library.scalar_5,
    6: scalar_library.scalar_6,
}

class Env():

    def __init__(self, bounds=10, fidelity=200, dt=0.1, external_force_magnitude=0.25, 
                Target_Setting="ON", target_speed=3):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T
        self.dt = dt
        self.external_force_magnitude = external_force_magnitude
        self.z_space = self.scalar(self.x_space, self.y_space)
        self.target_setting = Target_Setting
        if self.target_setting == "ON":
            self.target = Target(timestep=dt, bounds=bounds, speed=target_speed)
            self.target.behv()

    @staticmethod
    def scalar(x, y): 
        z = scalar_function[set.settings['scalar']](x, y)
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
    
    def update_scalar(self):
        tar_pos_x = self.target.position[0]
        tar_pos_y = self.target.position[1]

        self.scalar = lambda x, y: scalar_function[set.settings['scalar']](x-tar_pos_x, y-tar_pos_y)


    def update(self):
        if self.target_setting == "ON":
            self.target.update(self)
            self.update_scalar()
            self.update_z_space()
