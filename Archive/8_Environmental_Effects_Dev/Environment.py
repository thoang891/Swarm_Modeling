import numpy as np

class Env():

    def __init__(self, bounds=10, fidelity=2000, dt=0.1, external_force_magnitude=0.25):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T
        self.dt = dt
        self.external_force_magnitude = external_force_magnitude

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
    
    def z_space(self):
        z_space = Env.scalar(self.x_space, self.y_space)
        return z_space
        