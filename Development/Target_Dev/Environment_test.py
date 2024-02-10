import numpy as np

from Target_test import Target

class Env():

    def __init__(self, bounds=10, fidelity=2000, dt=0.1):
        self.bounds = bounds
        self.x_space = np.outer(np.linspace(-bounds, bounds, fidelity), np.ones(fidelity))
        self.y_space = self.x_space.copy().T
        self.dt = dt
        self.targ = Target()

    @staticmethod
    def scalar(x, y): 
        z = np.sinc((x/5)**2 + (y/5)**2) + np.sinc((x + 2)/5 + (y + 2)/5)/2
        return z
    
    def z_space(self):
        z_space = Env.scalar(self.x_space, self.y_space)
        return z_space


    ### TESTING ###

    def scalar_test(self, x, y): 
        z = np.sinc((x/5)**2 + (y/5)**2) + np.sinc((x + 2)/5 + (y + 2)/5)/2

        x_targ = []
        y_targ = []
        self.update()
        if x == x_targ and y == y_targ:
            z += 10
        return z
    
    def z_space_test(self):
        x_targ = []
        y_targ = []
        z_space = Env.scalar(self.x_space, self.y_space)
        self.update()
        z_space[x_targ, y_targ] += 10
        return z_space
    
    def update(self):
        self.targ.update()
        x_targ = self.targ.position[0]
        y_targ = self.targ.position[1]

        return x_targ, y_targ

        
        
