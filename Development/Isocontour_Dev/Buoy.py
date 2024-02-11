import numpy as np
import random

from Environment import Env

# Buoys are currently spawned in a uniform distribution within the environment

class Buoy():

    def __init__(self, id, behv="seeker", speed=2, com_radius=7, 
                 repulsion_radius=0.5, timestep=0.1, bounds=10):
        self.id = id
        self.env = Env(dt=timestep, bounds = bounds)
        self.position = [random.uniform(-self.env.bounds, self.env.bounds), 
                         random.uniform(-self.env.bounds, self.env.bounds)]
        self.velocity = None
        self.measurement = None
        self.com_radius = com_radius
        self.repulsion_radius = repulsion_radius
        self.behv = behv
        self.A = None # Local goal weight
        self.B = None # Global goal weight
        self.C = None # Repulsion weight
        self.D = None # Random walk weight
        self.local_goal_vector = None
        self.global_goal_vector = None
        self.repulsion_vector = None
        self.random_vector = None
        self.speed = speed
        self.broadcast_data_processed = None
        self.best_known_position = self.position
        self.best_known_measure = self.measure()
        self.best_known_id = self.id

    def measure(self):
        z_pos = self.env.scalar(self.position[0], self.position[1])
        self.measurement = z_pos
        return self.measurement
    
    def behavior(self):
        if self.behv == "seeker":
            self.A = 1
            self.B = 3
            self.C = 5
            self.D = 0.5
            
        elif self.behv == "explorer":
            self.A = 0.05
            self.B = 0.05
            self.C = 2
            self.D = 1
            self.repulsion_radius = 3

        return self.A, self.B, self.C, self.D, self.repulsion_radius

    def move(self):
        # Update position by adding velocity * time step
        self.position[0] += self.velocity[0]*self.env.dt
        self.position[1] += self.velocity[1]*self.env.dt

    def motor(self):
        # Reset velocity vector
        self.velocity = [] 

        # Define behavior vectors
        self.local_goal()
        self.global_goal()
        self.repulse()
        self.random_walk()

        u = (self.A*self.local_goal_vector[0] + self.B*self.global_goal_vector[0] +
            self.C*self.repulsion_vector[0] + self.D*self.random_vector[0])
        v = (self.A*self.local_goal_vector[1] + self.B*self.global_goal_vector[1] +
            self.C*self.repulsion_vector[1] + self.D*self.random_vector[1])
        
        # Normalize the velocity vector then multiply by speed
        velocity_unnormalized = [u, v]
        velocity_magnitude = np.linalg.norm(velocity_unnormalized)
        self.velocity = [velocity_unnormalized[0]*self.speed/velocity_magnitude, 
                         velocity_unnormalized[1]*self.speed/velocity_magnitude]
        
        return self.velocity

    def local_goal(self):
        data_frame = self.broadcast_data_processed.copy() # Copy the broadcast data to a local variable
        goal_vector_unnormalized = [0, 0] # Reset goal vector
        sum_neighbor_vector = [0, 0] # Reset neighbor vector
        self.local_goal_vector = [0, 0] # Reset goal vector
        
        # If data frame is not empty, find the buoy with the maximum measurement
        if data_frame:
            max_measurement = max(data_frame, key=lambda x: x['Measurement'])

            # Move towards the buoy with the maximum measurement if the current buoy's measurement is less than the maximum measurement
            if self.measure() < max_measurement['Measurement']:
                goal_vector_unnormalized = [max_measurement['x'] - self.position[0], 
                                            max_measurement['y'] - self.position[1]]
                goal_vector_magnitude = np.linalg.norm(goal_vector_unnormalized)
                self.local_goal_vector = [goal_vector_unnormalized[0]/goal_vector_magnitude, 
                                    goal_vector_unnormalized[1]/goal_vector_magnitude]

                print()
                print("max_measurement: {0}".format(max_measurement))
                print("Moving towards buoy {0} at position ({1}, {2})"\
                      .format(max_measurement['ID'], max_measurement['x'], max_measurement['y']))
                print()
            
            else:
                for data in data_frame:
                    x2 = data['x']
                    y2 = data['y']

                    # Construct vector from neighbor to self
                    neighbor_vector_unnormalized = [self.position[0] - x2, self.position[1] - y2] # NOTE: Testing unnormalized version to give furthest neighbor most weight
                    sum_neighbor_vector[0] += neighbor_vector_unnormalized[0]
                    sum_neighbor_vector[1] += neighbor_vector_unnormalized[1]

                # Normalize the sum of the neighbor vectors
                sum_neighbor_vector_magnitude = np.linalg.norm(sum_neighbor_vector)
                self.local_goal_vector = [sum_neighbor_vector[0]/sum_neighbor_vector_magnitude, 
                                    sum_neighbor_vector[1]/sum_neighbor_vector_magnitude]

                print()
                print("Buoy {0} is moving towards the average direction of its neighbors".format(self.id))
                print()

        else:
            self.local_goal_vector = [0, 0]
            print()
            print("No nearby neighbors to move with")

        print("Local goal vector: {0}".format(self.local_goal_vector))
        return self.local_goal_vector
    
    def global_goal(self):
        # Calculate normalized vector pointing from position to best known position
        # Need to condition it such that this only applies if there exists enough difference otherwise division by 0
        # condition with distance

        distance = np.sqrt((self.best_known_position[0] - self.position[0])**2 + 
                           (self.best_known_position[1] - self.position[1])**2)
        
        if distance > 0.001:
            goal_vector_unnormalized = [self.best_known_position[0] - self.position[0], 
                                        self.best_known_position[1] - self.position[1]]
            goal_vector_magnitude = np.linalg.norm(goal_vector_unnormalized)
            self.global_goal_vector = [goal_vector_unnormalized[0]/goal_vector_magnitude, 
                                    goal_vector_unnormalized[1]/goal_vector_magnitude]
        else:
            self.global_goal_vector = [0, 0]
            print()
            print("Buoy {0} is close enough to best known position".format(self.id))
            print()
        print("Global goal vector: {0}".format(self.global_goal_vector))

        return self.global_goal_vector

    def repulse(self):
        data_frame = self.broadcast_data_processed.copy() # Copy the broadcast data to a local variable
        bounding_vector = [0, 0] # Reset bounding vector
        bound_repulsion_vector = [0, 0] # Reset neighbor repulsion vector
        neighbor_repulsion_vector = [0, 0] # Reset neighbor repulsion vector
        neighborhood_repulsion_vector_unnormalized = [0, 0] # Reset neighborhood repulsion vector
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

        # Normalize the bounding repulsion vector if it exists
        if bounding_vector[0] != 0 or bounding_vector[1] != 0:
            print("Buoy {0} is out of bounds".format(self.id))
            bounding_vector_magnitude = np.linalg.norm(bounding_vector)
            bound_repulsion_vector = [bounding_vector[0]/bounding_vector_magnitude, 
                                      bounding_vector[1]/bounding_vector_magnitude]
        else:
            bound_repulsion_vector = [0, 0]
    
        # Calculate the repulsion vector due to the nearby neighbors
        for data in data_frame:
            x2 = data['x']
            y2 = data['y']

            # Calculate the distance between the two buoys
            distance = np.sqrt((x2 - self.position[0])**2 + (y2 - self.position[1])**2)
            print("Distance between buoy {0} and buoy {1}: {2}".format(self.id, data['ID'], distance))

            # Compare the distance to the repulsion radius and set the repulsion vector
            if distance < self.repulsion_radius:
                neighbor_repulsion_vector_unnormalized = [self.position[0] - x2, self.position[1] - y2]
                print("Repelling away from buoy {}".format(data['ID']))
                # Normalize the neighbor repulsion vector if it exists
                magnitude = np.linalg.norm(neighbor_repulsion_vector_unnormalized)
                neighbor_repulsion_vector = [neighbor_repulsion_vector_unnormalized[0]/magnitude, 
                                             neighbor_repulsion_vector_unnormalized[1]/magnitude]
            else:
                neighbor_repulsion_vector = [0, 0]
            
            neighborhood_repulsion_vector_unnormalized[0] += neighbor_repulsion_vector[0]
            neighborhood_repulsion_vector_unnormalized[1] += neighbor_repulsion_vector[1]

        # Normalize the neighborhood repulsion vector if it exists
        if neighborhood_repulsion_vector_unnormalized[0] != 0 or neighborhood_repulsion_vector_unnormalized[1] != 0:
            neighborhood_repulsion_vector_magnitude = np.linalg.norm(neighborhood_repulsion_vector_unnormalized)
            neighborhood_repulsion_vector = [neighborhood_repulsion_vector_unnormalized[0]/neighborhood_repulsion_vector_magnitude, 
                                             neighborhood_repulsion_vector_unnormalized[1]/neighborhood_repulsion_vector_magnitude]
        else:
            neighborhood_repulsion_vector = [0, 0]

        # Sum the bounding and neighborhood repulsion vectors
        repulsion_vector = [neighborhood_repulsion_vector[0] + bound_repulsion_vector[0], 
                            neighborhood_repulsion_vector[1] + bound_repulsion_vector[1]]
        
        # Normalize the repulsion vector if it exists
        if repulsion_vector[0] != 0 or repulsion_vector[1] != 0:
            repulsion_vector_magnitude = np.linalg.norm(repulsion_vector)
            self.repulsion_vector = [repulsion_vector[0]/repulsion_vector_magnitude, 
                                     repulsion_vector[1]/repulsion_vector_magnitude]
        else: 
            self.repulsion_vector = [0, 0]
        
        print("Repulsion vector: {0}".format(self.repulsion_vector))
        return self.repulsion_vector

    def random_walk(self):
        random_vector_unnormalized = [random.uniform(-1, 1), random.uniform(-1, 1)]
        random_vector_magnitude = np.linalg.norm(random_vector_unnormalized)
        self.random_vector = [random_vector_unnormalized[0]/random_vector_magnitude, 
                              random_vector_unnormalized[1]/random_vector_magnitude]
        print("Random vector: {0}".format(self.random_vector))
        return self.random_vector

    def read_mail(self, broadcast_data):
        print()
        print("*"*80)
        print("Buoy {0} ({1}) is reading mail and measuring {2:>6.2f} at [{3:>6.2f}, {4:>6.2f}]"
              .format(self.id, self.behv, self.measurement, self.position[0], self.position[1]))
        self.broadcast_data_processed = []

        for data in broadcast_data:
            if data['ID'] != self.id:
                x2 = data['x']
                y2 = data['y']

                # Calculate the distance between the two buoys
                distance = np.sqrt((x2 - self.position[0])**2 + (y2 - self.position[1])**2)

                # Remove data from buoys that are outside the communication radius
                if distance <= self.com_radius:
                    self.broadcast_data_processed.append(data)
                else:
                    print("Removed buoy {0}'s data from buoy {1}'s mail because the distance {2} is greater than the communication radius {3}"
                          .format(data['ID'], self.id, distance, self.com_radius))

        print("The remaining neighbor data for buoy {} is:".format(self.id))
        print("\n".join(str(data) for data in self.broadcast_data_processed)) # Print broadcast data to be read by buoy
        return self.broadcast_data_processed
    
    def memory(self):
        data_frame = self.broadcast_data_processed.copy()

        # If data frame is not empty, find the buoy with the maximum measurement
        if data_frame:
            max_measurement = max(data_frame, key=lambda x: x['Measurement'])
            max_best_known_measurement = max(data_frame, key=lambda x: x['best_measure'])
            print()
            print("max neighbor measurement: {0}".format(max_measurement))
            print()
            print("max neighbor best known measurement: {0}".format(max_best_known_measurement))

           # If neighbor has a better measurement, update best known position and measurement
            if self.best_known_measure < max_measurement['Measurement']:
                self.best_known_position = [max_measurement['x'], max_measurement['y']]
                self.best_known_measure = max_measurement['Measurement']
                self.best_known_id = max_measurement['ID']
            
            # If neighbor has a better best known measurement, update best known position and measurement
            if self.best_known_measure < max_best_known_measurement['best_measure']:
                self.best_known_position = [max_best_known_measurement['best_x'], max_best_known_measurement['best_y']]
                self.best_known_measure = max_best_known_measurement['best_measure']
                self.best_known_id = max_best_known_measurement['best_id']
                
        # If own measurement is better than best known measurement, update best known position and measurement
        if self.measurement > self.best_known_measure:
            self.best_known_position = self.position
            self.best_known_measure = self.measurement
            self.best_known_id = self.id

        print()
        print("Buoy {0} thinks the best known position is {1} and the best known measurement is {2}"
              .format(self.id, self.best_known_position, self.best_known_measure))
        print("Best measurement found by buoy {0}".format(self.best_known_id))
        print()

        return self.best_known_position, self.best_known_measure, self.best_known_id
    
    def update(self):
        self.behavior()
        self.measure()
        self.memory()
        self.motor()
        self.move()
