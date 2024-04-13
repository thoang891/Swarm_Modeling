import numpy as np
import random

# Target currently is generating a random walk and a repulsion vector
# Target is generated at a random position within the bounds of the environment

class Target():

    def __init__(self, timestep = 0.1, bounds = 10, speed_number=1, inertia=0.5):
        self.ID = "Target" 
        self.position = [random.uniform(-bounds, bounds), 
                        random.uniform(-bounds, bounds)]
        self.bounds = bounds
        self.speed_number = speed_number
        self.inertia = inertia
        self.speed = None
        self.measurement = None
        self.velocity = None
        self.prev_velocity = [0,0]
        self.dt = timestep
        self.random_vector = None
        self.repulsion_vector = None
        self.circle_vector = None
        self.A = None
        self.B = None
        self.C = None
        self.external_force = None
        self.target_data = {'ID': self.ID, 'behv': "Target", 'x': round(self.position[0], 2), 
                            'y': round(self.position[1], 2), 'u': None, 'v': None}

    def move(self, env):
        # Need to get external force
        external_force = env.external_force(self.position[0], self.position[1])

        # Update position by adding velocity * time step
        self.position[0] += (self.inertia * self.prev_velocity[0] + 
                            (1-self.inertia) * self.velocity[0] + external_force[0])*self.dt
        self.position[1] += (self.inertia * self.prev_velocity[1] + 
                            (1-self.inertia) * self.velocity[1] + external_force[1])*self.dt

        print("Target position: {0}".format(self.position))

        return self.position

    def motor(self):
        self.random_walk()
        self.repulse()
        self.circle()

        self.velocity = [self.A*self.speed*self.random_vector[0] + self.B*self.speed*self.repulsion_vector[0] + self.C*self.speed*self.circle_vector[0], 
                        self.A*self.speed*self.random_vector[1] + self.B*self.speed*self.repulsion_vector[1] + self.C*self.speed*self.circle_vector[1]]
        
        return self.velocity
    
    def set_speed(self):
        self.speed = self.speed_number*np.sqrt((self.bounds*2)**2)
        
        return self.speed

    def behv(self):
        
        def normalize_behavior(A, B, C):
            sum_behv = sum([A, B])
            self.A = A/sum_behv
            self.B = B/sum_behv
            self.C = C/sum_behv
            return self.A, self.B

        A = 1.5 # Random walk
        B = 2 # Repulsion
        C = 1 # Circle
        normalize_behavior(A, B, C)

        return self.A, self.B, self.C

    def repulse(self):  
        # Reset the repulsion vector
        bounding_vector = [0, 0]
        self.repulsion_vector = [0, 0]

         # Calculate the repulsion vector due to the bounds
        if self.position[0] > self.bounds:
            bounding_vector[0] = -1
        elif self.position[0] < -self.bounds:
            bounding_vector[0] = 1
        else:
            bounding_vector[0] = 0

        if self.position[1] > self.bounds:
            bounding_vector[1] = -1
        elif self.position[1] < -self.bounds:
            bounding_vector[1] = 1
        else:
            bounding_vector[1] = 0

        self.repulsion_vector = self.normalize(bounding_vector)
        
        return self.repulsion_vector

    def random_walk(self):
        random_vector_unnormalized = [random.uniform(-1, 1), random.uniform(-1, 1)]
        self.random_vector = self.normalize(random_vector_unnormalized)
        return self.random_vector
    
    def circle(self):
        circle_vector = [self.position[1], -self.position[0]]

        # Normalize the circle vector
        magnitude = np.linalg.norm(circle_vector)
        self.circle_vector = [circle_vector[0]/magnitude, 
                              circle_vector[1]/magnitude]

        return self.circle_vector
    
    def measure(self, env):
        self.measurement = env.scalar(self.position[0], self.position[1])
        return self.measurement

    def normalize(self, vector):
        magnitude = np.linalg.norm(vector)
        if magnitude != 0:
            return [vector[0]/magnitude, vector[1]/magnitude]
        else:
            return [0, 0]
        
    def update(self, env):
        self.motor()
        self.move(env)
        self.measure(env)
        self.target_data = {'ID': self.ID, 'x': round(self.position[0], 2), 
                            'y': round(self.position[1], 2), 'u': round(self.velocity[0], 2), 
                            'v': round(self.velocity[1], 2), 'Measurement': round(self.measurement, 3)}