import numpy as np
import random

from Environment import Env

class Buoy():

    def __init__(self, id):
        self.id = id
        self.env = Env()
        self.position = [random.uniform(-self.env.bounds, self.env.bounds), random.uniform(-self.env.bounds, self.env.bounds)]
        self.velocity = [1, 1]
        self.com_radius = 10

    def measure(self):
        z_pos = Env.scalar(self.position[0], self.position[1])
        return z_pos
    
    def move(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]

    def update(self, dt=0.1):
        self.move()
        self.velocity[0] = random.uniform(-1, 1)
        self.velocity[1] = random.uniform(-1, 1)
        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

