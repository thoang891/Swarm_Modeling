import numpy as np
from Buoy import Buoy
from Environment import Env

class Swarm():

    def __init__(self, seeker_pop=2, seeker_speed_number=1, seeker_com_number=1, seeker_repulsion_radius=0.5, 
                seeker_battery=47520, seeker_gps_accuracy=1, seeker_sensor_accuracy=1, seeker_memory_duration=1, 
                explorer_pop=2, explorer_speed_number=1, explorer_com_number=1, explorer_repulsion_radius=5, 
                explorer_battery=47520, explorer_gps_accuracy=1, explorer_sensor_accuracy=1, 
                explorer_memory_duration=1, iso_pop=2, iso_speed_number=1, iso_com_number=1, iso_repulsion_radius=0.5, 
                iso_battery=47520, iso_gps_accuracy=1, iso_sensor_accuracy=1, iso_memory_duration=1, iso_goal=-80, 
                iso_thresh=3, timestep=0.1, map_size=10, external_force_magnitude=0.25, fidelity=100, 
                target_setting="ON", target_speed_number = 1):
        self.seeker_population = seeker_pop
        self.seeker_speed_number = seeker_speed_number
        self.seeker_speed = None
        self.seeker_com_number = seeker_com_number
        self.seeker_com_radius = None
        self.seeker_repulsion_radius = seeker_repulsion_radius
        self.seeker_battery = seeker_battery
        self.seeker_gps_accuracy = seeker_gps_accuracy
        self.seeker_sensor_accuracy = seeker_sensor_accuracy
        self.seeker_memory_duration = seeker_memory_duration
        self.explorer_population = explorer_pop
        self.explorer_speed_number = explorer_speed_number
        self.explorer_speed = None
        self.explorer_com_number = explorer_com_number
        self.explorer_com_radius = None
        self.explorer_repulsion_radius = explorer_repulsion_radius
        self.explorer_battery = explorer_battery
        self.explorer_gps_accuracy = explorer_gps_accuracy
        self.explorer_sensor_accuracy = explorer_sensor_accuracy
        self.explorer_memory_duration = explorer_memory_duration
        self.isocontour_population = iso_pop
        self.isocontour_speed_number = iso_speed_number
        self.isocontour_speed = None
        self.isocontour_com_number = iso_com_number
        self.isocontour_com_radius = None
        self.isocontour_repulsion_radius = iso_repulsion_radius
        self.isocontour_battery = iso_battery
        self.isocontour_gps_accuracy = iso_gps_accuracy
        self.isocontour_sensor_accuracy = iso_sensor_accuracy
        self.isocontour_memory_duration = iso_memory_duration
        self.isocontour_goal = iso_goal
        self.isocontour_threshold = iso_thresh
        self.swarm = []
        self.broadcast_data = []
        self.env = Env(bounds=map_size, dt=timestep, fidelity=fidelity,
                       external_force_magnitude=external_force_magnitude, 
                       Target_Setting=target_setting, target_speed_number=target_speed_number)

    def construct(self):

        # Generate seeker buoys
        if self.seeker_population !=0:
            self.seeker_speed = self.set_speed(self.seeker_speed_number)
            self.seeker_com_radius = self.set_radius(self.seeker_com_number)
            for i in range(self.seeker_population):
                self.swarm.append(Buoy(id=i+1, com_radius=self.seeker_com_radius, 
                                    repulsion_radius=self.seeker_repulsion_radius, 
                                    speed=self.seeker_speed, battery=self.seeker_battery,
                                    behv="seeker", env=self.env))
        # Generate explorer buoys
        if self.explorer_population !=0:
            self.explorer_speed = self.set_speed(self.explorer_speed_number)
            self.explorer_com_radius = self.set_radius(self.explorer_com_number)
            for i in range(self.explorer_population):
                self.swarm.append(Buoy(id=i+1+self.seeker_population, com_radius=self.explorer_com_radius, 
                                    repulsion_radius=self.explorer_repulsion_radius,
                                    speed=self.explorer_speed, battery=self.explorer_battery,
                                    behv="explorer", env=self.env))
        # Generate isocontour buoys
        if self.isocontour_population !=0:   
            self.isocontour_speed = self.set_speed(self.isocontour_speed_number)
            self.isocontour_com_radius = self.set_radius(self.isocontour_com_number)
            for i in range(self.isocontour_population):
                self.swarm.append(Buoy(id=i+1+self.seeker_population+self.explorer_population, 
                                    com_radius=self.isocontour_com_radius, 
                                    repulsion_radius=self.isocontour_repulsion_radius,
                                    speed=self.isocontour_speed, battery=self.isocontour_battery,
                                    iso_thresh=self.isocontour_threshold, iso_goal=self.isocontour_goal,
                                    behv="isocontour", env=self.env))

        for buoy in self.swarm: # set initial measurement for buoys
            self.measure()

        return self.swarm
    
    def measure(self):
        for buoy in self.swarm:
            buoy.measurement = self.env.scalar(buoy.position[0], buoy.position[1])
        return self.swarm
    
    def set_speed(self, speed_number):
        speed = speed_number*np.sqrt((self.env.bounds*2)**2)
        return speed
    
    def set_radius(self, radius_number):
        pop = self.seeker_population + self.explorer_population + self.isocontour_population
        radius = radius_number*np.sqrt(((self.env.bounds*2)**2)/(pop*np.pi))
        return radius

    def broadcast(self):
        broadcast_data = [] # Clear the list for the new iteration

        # Build broadcast data for each buoy from each buoy
        for buoy in self.swarm:
            id = buoy.id
            behavior = buoy.behv
            com_radius = buoy.com_radius

            if behavior == "seeker":
                gps_accuracy = self.seeker_gps_accuracy
                sensor_accuracy = self.seeker_sensor_accuracy
            elif behavior == "explorer":
                gps_accuracy = self.explorer_gps_accuracy
                sensor_accuracy = self.explorer_sensor_accuracy
            elif behavior == "isocontour":
                gps_accuracy = self.isocontour_gps_accuracy
                sensor_accuracy = self.isocontour_sensor_accuracy

            x = round(buoy.position[0], gps_accuracy)
            y = round(buoy.position[1], gps_accuracy)
            z = round(buoy.measurement, sensor_accuracy)
            battery_percent = round(buoy.battery/buoy.full_battery*100, 2)
            battery = round(buoy.battery, 2)
            N = buoy.N
            Ns = buoy.Ns
            Ne = buoy.Ne
            Ni = buoy.Ni
            best_x = round(buoy.best_known_position[0], gps_accuracy)
            best_y = round(buoy.best_known_position[1], gps_accuracy)
            best_measure = round(buoy.best_known_measure, sensor_accuracy)
            best_id = buoy.best_known_id
            
            if battery <= 0:
                battery = 0
                print("ID: {0:>2}, Behavior: {1:8}, Battery: {2:>6.2f}%, Position: {3:>6.2f}, {4:>6.2f}, Measurement: {5:>6.2f}".format(id, behavior, battery_percent, x, y, z))
                buoy_data = {'ID': id, 'com_radius': com_radius, 'behv': behavior, 'Battery': battery, 
                            'Battery Percent': battery_percent, 'x': x, 'y': y, 'Measurement': z,
                            'N': N, 'Ns': Ns, 'Ne': Ne, 'Ni': Ni}

            elif buoy.velocity is not None:
                u = round(buoy.velocity[0], gps_accuracy)
                v = round(buoy.velocity[1], gps_accuracy)
                speed = round(np.sqrt(u**2 + v**2), gps_accuracy)

                print("ID: {0:>2}, Behavior: {1:8}, Battery: {2:>6.2f}%, Position: {3:>6.2f}, {4:>6.2f}, Measurement: {5:>6.2f}, Velocity: {6:>6.2f}, {7:>6.2f}, Speed: {8:>6.2f}, Best Known Position: {9:>6.2f}, {10:>6.2f}, Best Known Measurement: {11:>6.2f}, Best Known ID: {12:>2}"
                    .format(id, behavior, battery_percent, x, y, z, u, v, speed, best_x, best_y, best_measure, best_id))
                
                buoy_data = {'ID': id, 'com_radius': com_radius, 'Battery': battery, 'Battery Percent': battery_percent, 
                            'behv': behavior , 'x': x, 'y': y, 'Measurement': z,
                            'u': u, 'v': v, 'speed': speed, 'best_x': best_x, 'best_y': best_y, 
                            'best_measure': best_measure, 'best_id': best_id,
                            'N': N, 'Ns': Ns, 'Ne': Ne, 'Ni': Ni}
            else:
                print("ID: {0:>2}, Behavior: {1:8}, Battery: {2:>6.2f}%, Position: {3:>6.2f}, {4:>6.2f}, Measurement: {5:>6.2f}, Best Known Position: {6:>6.2f}, {7:>6.2f}, Best Known Measurement: {8:>6.2f}, Best Known ID: {9:>2}"
                      .format(id, behavior, battery_percent, x, y, z, best_x, best_y, best_measure, best_id))
                
                buoy_data = {'ID': id, 'com_radius': com_radius, 'Battery': battery, 'Battery Percent': battery_percent, 
                            'behv': behavior , 'x': x, 'y': y, 'Measurement': z, 'best_x': best_x, 
                            'best_y': best_y, 'best_measure': best_measure, 'best_id': best_id,
                            'N': N, 'Ns': Ns, 'Ne': Ne, 'Ni': Ni}
                
            broadcast_data.append(buoy_data)
        print()
        print("Unfiltered Broadcast Data")
        print("\n".join(str(data) for data in broadcast_data)) # Print broadcast data to be processed by buoy
        self.broadcast_data = broadcast_data
        return self.broadcast_data

    def update(self, current_time):
        # Reset best known parameters after memory_duration period
        if current_time % self.seeker_memory_duration == 0:
            for buoy in self.swarm:
                if buoy.behv == "seeker":
                    buoy.forget()
                    print("Buoy {0:>2} is forgetting at time: {1:>6.2f}".format(buoy.id, current_time))

        if current_time % self.explorer_memory_duration == 0:
            for buoy in self.swarm:
                if buoy.behv == "explorer":
                    buoy.forget()
                    print("Buoy {0:>2} is forgetting at time: {1:>6.2f}".format(buoy.id, current_time))
        
        if current_time % self.isocontour_memory_duration == 0:
            for buoy in self.swarm:
                if buoy.behv == "isocontour":
                    buoy.forget()
                    print("Buoy {0:>2} is forgetting at time: {1:>6.2f}".format(buoy.id, current_time))

        self.env.update()
        self.measure()
        self.broadcast()

        for buoy in self.swarm:
            if buoy.battery > 0:
                buoy.read_mail(self.broadcast_data)
            buoy.update()
