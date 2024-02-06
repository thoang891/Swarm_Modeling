import numpy as np
import random

from Environment import Env

# Currently assigns random initial positions and random velocities to the buoys, need to update with movement algorithm

class Buoy():

    def __init__(self, id, behv="seeker", timewarp=0.1):
        self.id = id
        self.env = Env(dt=timewarp)
        self.position = [random.uniform(-self.env.bounds, self.env.bounds), random.uniform(-self.env.bounds, self.env.bounds)]
        self.velocity = None
        self.com_radius = 10
        self.behv = behv
        self.A = None
        self.B = None
        self.C = None
        self.goal_vector = None
        self.repulsion_vector = None
        self.random_vector = None
        self.speed = 1

    def measure(self):
        z_pos = Env.scalar(self.position[0], self.position[1])
        return z_pos
    
    def behavior(self):
        if self.behv == "seeker":
            self.A = 1
            self.B = 3
            self.C = 0.5
        return self.A, self.B, self.C

    def move(self):
        self.position[0] += self.velocity[0]*self.env.dt
        self.position[1] += self.velocity[1]*self.env.dt

    def motor(self):
        self.velocity = [] # Reset velocity vector
        self.goal()
        self.repulse()
        self.random_walk()
        u = (self.A*self.goal_vector[0] + self.B*self.repulsion_vector[0] + self.C*self.random_vector[0])
        v = (self.A*self.goal_vector[1] + self.B*self.repulsion_vector[1] + self.C*self.random_vector[1])
        velocity_unnormalized = [u, v]
        velocity_magnitude = np.linalg.norm(velocity_unnormalized)
        self.velocity = [velocity_unnormalized[0]*self.speed/velocity_magnitude, velocity_unnormalized[1]*self.speed/velocity_magnitude]
        return self.velocity

    def goal(self):
        self.goal_vector = [0, 0]
        return self.goal_vector # NOTE: Define goal vector based on neighrbor proximity. Need to normalize.

    def repulse(self):
        self.repulsion_vector = [0, 0]
        return self.repulsion_vector # NOTE: Define repulsion vector based on neighbor proximity and boundary proximity. Need to normalize.

    def random_walk(self):
        random_vector_unnormalized = [random.uniform(-1, 1), random.uniform(-1, 1)]
        random_vector_magnitude = np.linalg.norm(random_vector_unnormalized)
        self.random_vector = [random_vector_unnormalized[0]/random_vector_magnitude, random_vector_unnormalized[1]/random_vector_magnitude]
        return self.random_vector

    def read_mail(self):
        pass # NOTE: Define communication behavior

    def update(self):
        self.behavior()
        self.motor()
        self.move()


