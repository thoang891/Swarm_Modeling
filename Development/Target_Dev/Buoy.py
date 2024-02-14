import numpy as np
import random

# Buoys are currently spawned in a uniform distribution within the environment

class Buoy():

    def __init__(self, id, behv="seeker", speed=2, com_radius=7, 
                repulsion_radius=0.5, iso_thresh=5, 
                iso_goal=50, battery=47520, env=None):
        self.id = id
        # self.env = Env(dt=timestep, bounds = bounds, external_force_magnitude=external_force_magitude) # Pass as an argument from Swarm class
        self.env = env
        self.position = [random.uniform(-self.env.bounds, self.env.bounds), 
                         random.uniform(-self.env.bounds, self.env.bounds)] # [m, m]
        # self.position = [random.uniform(self.env.bounds, -self.env.bounds),]
        self.velocity = None # [m/s, m/s]
        self.measurement = None # scalar value
        self.full_battery = battery # Default battery life is movement at 1 m/s for 1 hour. [watt*second]
        self.battery = battery 
        self.com_radius = com_radius # [m]
        self.repulsion_radius = repulsion_radius # [m]
        self.isocontour_threshold = iso_thresh 
        self.isocontour_goal = iso_goal # Goal measurement for isocontour behavior
        self.behv = behv
        self.A = None # Local goal weight
        self.B = None # Global goal weight
        self.C = None # Repulsion weight
        self.D = None # Random walk weight
        self.E = None # Isocontour weight
        self.local_goal_vector = None
        self.global_goal_vector = None
        self.repulsion_vector = None
        self.random_vector = None
        self.isocontour_vector = None
        self.speed = speed # [m/s]
        self.broadcast_data_processed = None
        self.best_known_position = self.position
        self.best_known_measure = self.measurement
        self.best_known_id = self.id
    
    def update_battery(self):
        # Calculate battery discharge based on magnitude of velocity developed by motor function.
        # Velocity is translated into power based on a cubic polynomial fit of buoy drag properties 
        # developed by Brandon Zoss in his thesis. Power is then integrated over the time step to
        # calculate the discharge. Discharge is then subtracted from the battery level.
        
        velocity_magnitude = 0 # Reset velocity magnitude. Unit is m/s
        power = 0 # Reset power. Unit is watts.
        discharge = 0 # Reset discharge

        if self.velocity is not None:
            print("#"*80)
            print("Battery Data for Buoy {0}".format(self.id))
            velocity_magnitude = round(np.linalg.norm(self.velocity), 2) # Rounded to 2 decimal places to prevent negative power values
            print("Velocity magnitude: ", velocity_magnitude)   
            power = 12.545*(velocity_magnitude**3) + 0.662*(velocity_magnitude**2) - 0.007*velocity_magnitude 
            print("Power: ", power)
            discharge = power*self.env.dt
            print("Discharge: ", discharge)
            self.battery -= discharge
            print("Remaining battery: ", self.battery)
            print("Remaining battery percentage: ", (self.battery/self.full_battery)*100, "%")
            print("#"*80)
            return self.battery
    
    def behavior(self):

        def normalize_behavior(A, B, C, D, E):
            sum_behv = sum([A, B, C, D, E])
            self.A = A/sum_behv
            self.B = B/sum_behv
            self.C = C/sum_behv
            self.D = D/sum_behv
            self.E = E/sum_behv
            return self.A, self.B, self.C, self.D, self.E

        if self.behv == "seeker":
            A = 1
            B = 3
            C = 5
            D = 0.5
            E = 0

        elif self.behv == "explorer":
            A = 0.05
            B = 0.05
            D = 1
            C = 2
            E = 0
            self.repulsion_radius = 3

        elif self.behv == "isocontour":
            A = 0
            B = 0
            C = 1.25
            D = 0.4
            E = 1
            
        normalize_behavior(A, B, C, D, E)

        check_sum = sum([self.A, self.B, self.C, self.D, self.E])

        print("Buoy {0} is a {1} with weights A: {2}, B: {3}, C: {4}, D: {5}, E: {6}"
              .format(self.id, self.behv, self.A, self.B, self.C, self.D, self.E))
        print("Check sum: ", check_sum)

        return self.A, self.B, self.C, self.D, self.E, self.repulsion_radius

    def move(self):
        # Determine external force
        F = self.env.external_force(x=self.position[0], y=self.position[1])
        print("External force: ", F)

        # Update position by adding velocity * time step
        self.position[0] += self.velocity[0]*self.env.dt + F[0]*self.env.dt
        self.position[1] += self.velocity[1]*self.env.dt + F[1]*self.env.dt

    def motor(self):
        # Reset velocity vector
        self.velocity = []

        if self.battery <= 0:
            print("Buoy {0} is out of battery".format(self.id))
            self.velocity = [0, 0]
            return self.velocity 

        else:
        # Define behavior vectors
            self.local_goal()
            self.global_goal()
            self.repulse()
            self.random_walk()
            self.isocontour_walk()

            u = (self.A*self.speed*self.local_goal_vector[0] + self.B*self.speed*self.global_goal_vector[0] +
                self.C*self.speed*self.repulsion_vector[0] + self.D*self.speed*self.random_vector[0] +
                self.E*self.speed*self.isocontour_vector[0])
            v = (self.A*self.speed*self.local_goal_vector[1] + self.B*self.speed*self.global_goal_vector[1] +
                self.C*self.speed*self.repulsion_vector[1] + self.D*self.speed*self.random_vector[1] +
                self.E*self.speed*self.isocontour_vector[1])
            
            self.velocity = [u, v]
            self.update_battery()
        
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
            if self.measurement < max_measurement['Measurement']:
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

    def isocontour_walk(self):
        data_frame = self.broadcast_data_processed.copy() # Copy the broadcast data to a local variable
        sum_neighbor_vector = [0, 0] # Reset neighbor vector
        goal_contour = self.isocontour_goal # Goal measurement for isocontour behavior
        self.isocontour_vector = [0, 0] # Reset isocontour vector

        weight_lower_bound = 0.0000001 # Clip the neighbor weight
        seeking_repulsion_rad = 0.4 # Repulsion radius when searching for the contour goal
        spreading_repulsion_rad = 4 # Repulsion radius when within contour goal threshold to promote spreading
        
        lower_bound = goal_contour - self.isocontour_threshold
        upper_bound = goal_contour + self.isocontour_threshold
        
        print("Self Measurement: {0}".format(self.measurement))

        # If within threshold of goal contour, move opposite to neighborhood vector
        if self.measurement >= lower_bound and self.measurement <= upper_bound:
            self.repulsion_radius = spreading_repulsion_rad
            print("Buoy {0} is close enough to the goal".format(self.id))
            print("Buoy {0} is moving away from its neighbors")

            sum_neighbor_vector = [0, 0]
            for data in data_frame:
                x2 = data['x']
                y2 = data['y']
                neighbor_vector_unnormalized = [self.position[0] - x2, self.position[1] - y2]
                sum_neighbor_vector[0] += neighbor_vector_unnormalized[0]
                sum_neighbor_vector[1] += neighbor_vector_unnormalized[1]
            
            # Normalize the sum of the neighbor vectors 
            if sum_neighbor_vector[0] != 0 or sum_neighbor_vector[1] != 0:
                sum_neighbor_vector_magnitude = np.linalg.norm(sum_neighbor_vector)
                self.isocontour_vector = [sum_neighbor_vector[0]/sum_neighbor_vector_magnitude, 
                                        sum_neighbor_vector[1]/sum_neighbor_vector_magnitude]

            print("Moving opposite to neighborhood vector: {0}".format(self.isocontour_vector))

        # Check if the average measurement is greater than goal contour
        elif upper_bound > self.measurement:
            self.repulsion_radius = seeking_repulsion_rad
            print("Buoy {0} is measuring less than the goal".format(self.id))
            # Move towards the average of neighbors measuring greater than goal contour
            sum_neighbor_vector = [0, 0]
            for data in data_frame:
                if data['Measurement'] > self.measurement:
                    x2 = data['x']
                    y2 = data['y']
                    neighbor_vector_unnormalized = [x2 - self.position[0], y2 - self.position[1]]
                    # Assign a penalty weight based on the difference between the average and goal
                    # Buoys measuring further from the goal will have less influence
                    weight = abs(goal_contour - data['Measurement'])
                    if weight < weight_lower_bound: # Testing lower bound for weight
                        weight = weight_lower_bound

                    sum_neighbor_vector[0] += neighbor_vector_unnormalized[0]/weight
                    sum_neighbor_vector[1] += neighbor_vector_unnormalized[1]/weight
                    print("Adding neighbor vector: {0} from buoy {1} because it is measuring {2}".format(neighbor_vector_unnormalized, data['ID'], data['Measurement']))

            # Normalize the sum of the neighbor vectors
            if sum_neighbor_vector[0] != 0 or sum_neighbor_vector[1] != 0:
                sum_neighbor_vector_magnitude = np.linalg.norm(sum_neighbor_vector)
                self.isocontour_vector = [sum_neighbor_vector[0]/sum_neighbor_vector_magnitude, 
                                        sum_neighbor_vector[1]/sum_neighbor_vector_magnitude]
                    
        # Check if the average measurement is less than goal contour
        elif lower_bound < self.measurement:
            self.repulsion_radius = seeking_repulsion_rad
            print("Buoy {0} is measuring greater than the goal".format(self.id))
            # Move towards the average of neighbors measuring less than goal contour
            sum_neighbor_vector = [0, 0]
            for data in data_frame:
                if data['Measurement'] < self.measurement:
                    x2 = data['x']
                    y2 = data['y']
                    neighbor_vector_unnormalized = [x2 - self.position[0], y2 - self.position[1]]
                    # Assign a penalty weight based on the difference between the average and goal
                    # Buoys measuring further from the goal will have less influence
                    weight = abs(data['Measurement'] - goal_contour)
                    if weight < weight_lower_bound:
                        weight = weight_lower_bound
                    sum_neighbor_vector[0] += neighbor_vector_unnormalized[0]/weight
                    sum_neighbor_vector[1] += neighbor_vector_unnormalized[1]/weight
                    print("Adding neighbor vector: {0} from buoy {1} because it is measuring {2}".format(neighbor_vector_unnormalized, data['ID'], data['Measurement']))
                    
            # Normalize the sum of the neighbor vectors
            if sum_neighbor_vector[0] != 0 or sum_neighbor_vector[1] != 0:
                sum_neighbor_vector_magnitude = np.linalg.norm(sum_neighbor_vector)
                self.isocontour_vector = [sum_neighbor_vector[0]/sum_neighbor_vector_magnitude, 
                                        sum_neighbor_vector[1]/sum_neighbor_vector_magnitude]

        print("Isocontour vector: {0}".format(self.isocontour_vector))

        return self.isocontour_vector, self.repulsion_radius

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
    
    def forget(self):
        # Reset best known parameters
        self.best_known_position = self.position
        self.best_known_measure = self.measurement
        self.best_known_id = self.id
    
    def update(self):
        self.behavior()
        # self.measure()
        self.memory()
        self.motor()
        self.move()
