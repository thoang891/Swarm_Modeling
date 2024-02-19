import numpy as np
import math

from Target import Target

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
        # z = np.sinc((x/5)**2 + (y/5)**2) + np.sinc((x + 2)/5 + (y + 2)/5)/2
        # z = np.cos(x/2) + np.sin(y/2)
        z = -((x)**2 + (y)**2)
        # z = x**2 + 20*np.sin(x) + y**2 - 20*np.sin(y)
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
        self.scalar = lambda x, y: -((x-tar_pos_x)**2 + (y-tar_pos_y)**2) # This function should match the scalar

    def update(self):
        if self.target_setting == "ON":
            self.target.update(self)
            self.update_scalar()
            self.update_z_space()
