import numpy as np
import random

from Environment import Env

class Buoy():

    def __init__(self, id, behv="seeker", speed=1, com_radius=10, timestep=0.1, repulsion_radius=0.5):
        self.id = id
        self.env = Env(dt=timestep)
        self.position = [random.uniform(-self.env.bounds, self.env.bounds), random.uniform(-self.env.bounds, self.env.bounds)]
        self.velocity = None
        self.com_radius = com_radius
        self.behv = behv
        self.A = None
        self.B = None
        self.C = None
        self.goal_vector = None
        self.repulsion_vector = None
        self.neighbor_repulsion_vector = None
        self.bound_repulsion_vector = None
        self.random_vector = None
        self.speed = speed
        self.broadcast_data_processed = None
        self.repulsion_radius = repulsion_radius

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
        # Update position by adding velocity * time step
        self.position[0] += self.velocity[0]*self.env.dt
        self.position[1] += self.velocity[1]*self.env.dt

    def motor(self):
        # Reset velocity vector
        self.velocity = [] 

        # Define behavior vectors
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
        data_frame = self.broadcast_data_processed
        bounding_vector = [0, 0]
        self.neighbor_repulsion_vector = [0, 0] # Reset neighbor repulsion vector
        self.bound_repulsion_vector = [0, 0] # Reset neighbor repulsion vector
        self.repulsion_vector = [0, 0] # Reset repulsion vector

        # Calculate the repulsion vector due to the bounds
        if self.position[0] > self.env.bounds:
            bounding_vector[0] = -1
        elif self.position[0] < -self.env.bounds:
            bounding_vector[0] = 1
        else:
            bounding_vector[0] = 0

        if self.position[1] > self.env.bounds:
            bounding_vector[1] = -1
        elif self.position[1] < -self.env.bounds:
            bounding_vector[1] = 1
        else:
            bounding_vector[1] = 0

        # Normalize the bounding repulsion vector
        bounding_vector_magnitude = np.linalg.norm(bounding_vector)
        self.bound_repulsion_vector = [bounding_vector[0]/bounding_vector_magnitude, bounding_vector[1]/bounding_vector_magnitude]
    
        for data in data_frame:
            x2 = data['x']
            y2 = data['y']
            # print("x2: {0}, y2: {1}".format(x2, y2))

            # Calculate the distance between the two buoys
            distance = np.sqrt((x2 - self.position[0])**2 + (y2 - self.position[1])**2)
            print("Distance between buoy {0} and buoy {1}: {2}".format(self.id, data['ID'], distance))

            # Compare the distance to the repulsion radius and set the repulsion vector
            if distance < self.repulsion_radius:
                neighbor_repulsion_vector_unnormalized = [self.position[0] - x2, self.position[1] - y2]
                print("Repulsion between buoy {0} and buoy {1}".format(self.id, data['ID']))
            else:
                neighbor_repulsion_vector_unnormalized = [0, 0]

            # Normalize the neighbor repulsion vector
            magnitude = np.linalg.norm(neighbor_repulsion_vector_unnormalized)
            self.neighbor_repulsion_vector = [neighbor_repulsion_vector_unnormalized[0]/magnitude, neighbor_repulsion_vector_unnormalized[1]/magnitude]

        self.repulsion_vector = [self.neighbor_repulsion_vector[0] + self.bound_repulsion_vector[0], self.neighbor_repulsion_vector[1] + self.bound_repulsion_vector[1]]
        return self.repulsion_vector 

    def random_walk(self):
        random_vector_unnormalized = [random.uniform(-1, 1), random.uniform(-1, 1)]
        random_vector_magnitude = np.linalg.norm(random_vector_unnormalized)
        self.random_vector = [random_vector_unnormalized[0]/random_vector_magnitude, random_vector_unnormalized[1]/random_vector_magnitude]
        return self.random_vector

    def read_mail(self, broadcast_data):
        print("")
        print("Buoy {0} is reading mail".format(self.id))
        self.broadcast_data_processed= broadcast_data.copy()
        for data in self.broadcast_data_processed:
            if data['ID'] == self.id:
                # remove the own buoy's data from the broadcast data
                self.broadcast_data_processed.remove(data)
                print("Removed buoy {}'s data from own mail".format(self.id))
        
        for data in self.broadcast_data_processed:
            x2 = data['x']
            y2 = data['y']

            # Calculate the distance between the two buoys
            distance = np.sqrt((x2 - self.position[0])**2 + (y2 - self.position[1])**2)

            if distance > self.com_radius:
                self.broadcast_data_processed.remove(data)
                print("Removed buoy {0}'s data from buoy {1}'s mail because the distance {2} is greater than the communication radius {3}".format(data['ID'], self.id, distance, self.com_radius))
        print("\n".join(str(data) for data in self.broadcast_data_processed)) # Print broadcast data to be read by buoy
        return self.broadcast_data_processed

    def update(self):
        self.behavior()
        self.motor()
        self.move()
