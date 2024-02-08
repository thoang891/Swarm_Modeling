import numpy as np

class Env():

    def __init__(self, bounds=10, fidelity=2000, dt=0.1):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T
        self.dt = dt

    @staticmethod
    def scalar(x, y): 
        z = -(x**2 + y**2)
        return z

    def z_space(self):
        z_space = Env.scalar(self.x_space, self.y_space)
        return z_space
