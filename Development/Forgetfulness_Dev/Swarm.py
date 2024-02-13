import numpy as np
from Buoy import Buoy

class Swarm():

    def __init__(self, seeker_pop=2, explorer_pop=2, iso_pop=2, com_radius=7, 
                iso_goal=0, iso_thresh=5, speed=2, battery=3600, timestep=0.1, map_size=10,
                gps_accuracy=3, sensor_accuracy=3, external_force_magnitude=0.25):
        self.seeker_population = seeker_pop
        self.explorer_population = explorer_pop
        self.isocontour_population = iso_pop
        self.swarm = []
        self.timestep = timestep
        self.map_size = map_size
        self.broadcast_data = []
        self.com_radius = com_radius
        self.speed = speed
        self.isocontour_goal = iso_goal
        self.isocontour_threshold = iso_thresh
        self.battery = battery
        self.gps_accuracy = gps_accuracy # Integer value for decimal places of GPS coordinates. Minumum is 1.
        self.sensor_accuracy = sensor_accuracy # Integer value for decimal places of sensor measurements. Minimum is 1.
        self.external_force_magitude = external_force_magnitude # Scalar for how strong external forces are.

    def construct(self):
        # Generate seeker buoys
        if self.seeker_population !=0:
            for i in range(self.seeker_population):
                self.swarm.append(Buoy(id=i+1, com_radius=self.com_radius, 
                                    speed=self.speed, timestep=self.timestep, 
                                    battery=self.battery, behv="seeker", bounds=self.map_size,
                                    external_force_magitude=self.external_force_magitude))
        # Generate explorer buoys
        if self.explorer_population !=0:
            for i in range(self.explorer_population):
                self.swarm.append(Buoy(id=i+1+self.seeker_population, com_radius=self.com_radius, 
                                    speed=self.speed, timestep=self.timestep, 
                                    battery=self.battery, behv="explorer", bounds=self.map_size, 
                                    external_force_magitude=self.external_force_magitude))
        # Generate isocontour buoys
        if self.isocontour_population !=0:   
            for i in range(self.isocontour_population):
                self.swarm.append(Buoy(id=i+1+self.seeker_population+self.explorer_population, 
                                    com_radius=self.com_radius, speed=self.speed, 
                                    timestep=self.timestep, battery=self.battery, behv="isocontour", 
                                    bounds=self.map_size, iso_goal=self.isocontour_goal, 
                                    iso_thresh=self.isocontour_threshold, 
                                    external_force_magitude=self.external_force_magitude))

        for buoy in self.swarm:
            buoy.measure()

        return self.swarm

    def broadcast(self):
        broadcast_data = [] # Clear the list for the new iterationcdd

        # Build broadcast data for each buoy from each buoy
        for buoy in self.swarm:
            id = buoy.id
            behavior = buoy.behv
            x = round(buoy.position[0], self.gps_accuracy)
            y = round(buoy.position[1], self.gps_accuracy)
            z = round(buoy.measurement, self.sensor_accuracy)
            battery = buoy.battery/buoy.full_battery*100
            best_x = round(buoy.best_known_position[0], self.gps_accuracy)
            best_y = round(buoy.best_known_position[1], self.gps_accuracy)
            best_measure = round(buoy.best_known_measure, self.sensor_accuracy)
            best_id = buoy.best_known_id

            if buoy.velocity is not None:
                u = round(buoy.velocity[0], self.gps_accuracy)
                v = round(buoy.velocity[1], self.gps_accuracy)
                speed = round(np.sqrt(u**2 + v**2), self.gps_accuracy)

                print("ID: {0:>2}, Behavior: {1:8}, Battery: {2:>6.2f}%, Position: {3:>6.2f}, {4:>6.2f}, Measurement: {5:>6.2f}, Velocity: {6:>6.2f}, {7:>6.2f}, Speed: {8:>6.2f}, Best Known Position: {9:>6.2f}, {10:>6.2f}, Best Known Measurement: {11:>6.2f}, Best Known ID: {12:>2}"
                    .format(id, behavior, battery, x, y, z, u, v, speed, best_x, best_y, best_measure, best_id))
                
                buoy_data = {'ID': id, 'Battery': battery, 'behv': behavior , 'x': x, 'y': y, 'Measurement': z,
                            'u': u, 'v': v, 'speed': speed, 'best_x': best_x, 'best_y': best_y, 
                            'best_measure': best_measure, 'best_id': best_id}
            else:
                print("ID: {0:>2}, Behavior: {1:8}, Battery: {2:>6.2f}%, Position: {3:>6.2f}, {4:>6.2f}, Measurement: {5:>6.2f}, Best Known Position: {6:>6.2f}, {7:>6.2f}, Best Known Measurement: {8:>6.2f}, Best Known ID: {9:>2}"
                      .format(id, behavior, battery, x, y, z, best_x, best_y, best_measure, best_id))
                
                buoy_data = {'ID': id, 'Battery': battery, 'behv': behavior , 'x': x, 'y': y, 'Measurement': z, 
                            'best_x': best_x, 'best_y': best_y, 'best_measure': best_measure, 'best_id': best_id}
                
            broadcast_data.append(buoy_data)
        print()
        print("Unfiltered Broadcast Data")
        print("\n".join(str(data) for data in broadcast_data)) # Print broadcast data to be processed by buoy
        self.broadcast_data = broadcast_data
        return self.broadcast_data

    def update(self):
        self.broadcast()
        for buoy in self.swarm:
            buoy.read_mail(self.broadcast_data)
            buoy.update()
 