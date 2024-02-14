import numpy as np
import random

# Create a target class that will affect the environment

class Target():

    def __init__(self, timestep = 0.1, bounds = 10, speed=2):
        # self.env = Env(dt = timestep, bounds = bounds)
        # self.position = [random.uniform(-bounds, bounds), random.uniform(-bounds, bounds)]
        self.position = [0,0]
        self.speed = speed
        self.dt = timestep

    def move(self):
        self.position[0] += random.uniform(-self.speed, self.speed)*self.dt
        self.position[1] += random.uniform(-self.speed, self.speed)*self.dt

    def update(self):
        self.move()