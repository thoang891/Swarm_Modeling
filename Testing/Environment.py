import numpy as np

class Env():

    def __init__(self, bounds=10, fidelity=2000):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T

    @staticmethod
    def scalar(x, y): # Define the scalar field to be measured
        z = x**2 + y**2
        return z

    def z_space(self):
        z_space = Env.scalar(self.x_space, self.y_space)
        return z_space




