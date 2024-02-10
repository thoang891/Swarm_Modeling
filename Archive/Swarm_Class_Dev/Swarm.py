from Buoy import Buoy

class Swarm():

    def __init__(self, seeker_pop = 2, explorer_pop = 2, timestep = 0.1, map_size = 10):
        self.seeker_population = seeker_pop
        self.explorer_population = explorer_pop
        self.swarm = []
        self.timestep = timestep
        self.map_size = map_size
        self.broadcast_data = []

    def construct(self):
        for i in range(self.seeker_population):
            self.swarm.append(Buoy(i+1, timestep=self.timestep, behv="seeker", bounds=self.map_size))
        
        for i in range(self.explorer_population):
            self.swarm.append(Buoy(i+1+self.seeker_population, timestep=self.timestep, behv="explorer", bounds=self.map_size))

        return self.swarm

    def broadcast(self):
        broadcast_data = [] # Clear the list for the new iteration

        for buoy in self.swarm:
            id = buoy.id
            behavior = buoy.behv
            x = buoy.position[0]
            y = buoy.position[1]
            z = buoy.measure()
            print("ID: {0:>2}, Behavior: {1}, Position: {2:>6.2f}, {3:>6.2f}, Measurement: {4:>6.2f}".format(id, behavior, x, y, z))

            buoy_data = {'ID': id, 'behv': behavior , 'x': x, 'y': y, 'Measurement': z}
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
 