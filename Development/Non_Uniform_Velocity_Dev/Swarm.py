from Buoy import Buoy

class Swarm():

    def __init__(self, seeker_pop=2, explorer_pop=2, iso_pop=2, com_radius=7, 
                iso_goal=0, iso_thresh=5, speed=2, timestep=0.1, map_size=10):
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

    def construct(self):
        # Generate seeker buoys
        if self.seeker_population !=0:
            for i in range(self.seeker_population):
                self.swarm.append(Buoy(id=i+1, com_radius=self.com_radius, 
                                    speed=self.speed, timestep=self.timestep, 
                                    behv="seeker", bounds=self.map_size))
        # Generate explorer buoys
        if self.explorer_population !=0:
            for i in range(self.explorer_population):
                self.swarm.append(Buoy(id=i+1+self.seeker_population, com_radius=self.com_radius, 
                                    speed=self.speed, timestep=self.timestep, 
                                    behv="explorer", bounds=self.map_size))
        # Generate isocontour buoys
        if self.isocontour_population !=0:   
            for i in range(self.isocontour_population):
                self.swarm.append(Buoy(id=i+1+self.seeker_population+self.explorer_population, 
                                    com_radius=self.com_radius, speed=self.speed, 
                                    timestep=self.timestep, behv="isocontour", bounds=self.map_size,
                                    iso_goal=self.isocontour_goal, iso_thresh=self.isocontour_threshold))

        for buoy in self.swarm:
            buoy.measure()

        return self.swarm

    def broadcast(self):
        broadcast_data = [] # Clear the list for the new iteration

        # Build broadcast data for each buoy from each buoy
        for buoy in self.swarm:
            id = buoy.id
            behavior = buoy.behv
            x = buoy.position[0]
            y = buoy.position[1]
            z = buoy.measure()
            best_x = buoy.best_known_position[0]
            best_y = buoy.best_known_position[1]
            best_measure = buoy.best_known_measure
            best_id = buoy.best_known_id

            print("ID: {0:>2}, Behavior: {1:8}, Position: {2:>6.2f}, {3:>6.2f}, Measurement: {4:>6.2f}, Best Known Position: {5:>6.2f}, {6:>6.2f}, Best Known Measurement: {7:>6.2f}, Best Known ID: {8:>2}"
                  .format(id, behavior, x, y, z, best_x, best_y, best_measure, best_id))

            buoy_data = {'ID': id, 'behv': behavior , 'x': x, 'y': y, 'Measurement': z, 
                         'best_x': best_x, 'best_y': best_y, 'best_measure': best_measure, 'best_id': best_id}
            broadcast_data.append(buoy_data)
        
        print("Broadcast Data")
        print("\n".join(str(data) for data in broadcast_data)) # Print broadcast data to be read by buoy
        self.broadcast_data = broadcast_data
        return self.broadcast_data

    def update(self):
        self.broadcast()
        for buoy in self.swarm:
            buoy.read_mail(self.broadcast_data)
            buoy.update()
 