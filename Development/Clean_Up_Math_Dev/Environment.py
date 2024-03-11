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
                Target_Setting="ON", target_speed_number=3, inertia=0.5, decay=0.9, scalar_duration=5,
                relative_strength=6):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T
        self.dt = dt
        self.external_force_magnitude = external_force_magnitude
        self.z_space = self.scalar(self.x_space, self.y_space)
        self.env_hist = []
        self.target_setting = Target_Setting
        self.target_strength = None
        self.relative_strength = relative_strength
        self.decay = decay
        self.scalar_duration = scalar_duration
        if self.target_setting == "ON":
            self.target = Target(timestep=dt, bounds=bounds, 
                                 speed_number=target_speed_number,
                                 inertia=inertia)
            self.target.set_speed()
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

    def update_scalar(self, current_time):
        tar_pos_x = self.target.position[0]
        tar_pos_y = self.target.position[1]
        timestamp = current_time
        elapsed_time = current_time-timestamp
        decay_factor = (self.decay ** (elapsed_time + self.dt)) * self.dt
        new_scalar = lambda x, y: scalar_function[set.settings['scalar']](x, y, center_x=tar_pos_x, center_y=tar_pos_y)
        new_scalar_decayed = lambda x, y: new_scalar(x, y) * decay_factor
        self.env_hist.append(new_scalar_decayed)

        current_scalar = lambda x, y: scalar_function[set.settings['scalar']](x-tar_pos_x, y-tar_pos_y)

        if len(self.env_hist) > self.scalar_duration/self.dt:
            self.env_hist.pop(0)

        # Define the scalar function as the sum of the updated history and the current scalar
        self.scalar = lambda x, y: sum(scalar_func(x, y) for scalar_func in self.env_hist) + self.target_strength*current_scalar(x, y)

        return self.scalar
    
    def calculate_target_strength(self):
        decay = self.decay
        duration = self.scalar_duration
        timestep = self.dt

        iters = duration/timestep
        strength = 0

        for i in range(int(iters)):
            strength += decay ** (1 + i*timestep) * timestep

        self.target_strength = strength * self.relative_strength

        return self.target_strength

    def update(self, current_time):
        if self.target_setting == "ON":
            if self.target_strength is None:
                self.calculate_target_strength()

            self.target.update(self)
            self.update_scalar(current_time)
            self.update_z_space()
