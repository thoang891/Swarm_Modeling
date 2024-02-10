from Buoy import Buoy
from Environment import Env

class Swarm():

    def __init__(self, seeker_pop = 5, explorer_pop = 20, timestep = 0.1, map_size = 10):
        self.seeker_population = seeker_pop
        self.explorer_population = explorer_pop
        self.swarm = []
        self.timestep = timestep
        self.map_size = map_size

    def construct(self):
        for i in range(self.seeker_population):
            self.swarm.append(Buoy(i+1, timestep=self.timestep, behv="seeker", bounds=self.map_size))
        
        for i in range(self.explorer_population):
            self.swarm.append(Buoy(i+1+self.seeker_population, timestep=self.timestep, behv="explorer", bounds=self.map_size))

        return self.swarm

    def broadcast(self):
        pass

    def update(self):
        pass


### TESTING ###

def main():
    swarm = Swarm()
    swarm.construct()

    # i want to print out the ID for each buoy in the swarm
    for buoy in swarm.swarm:
        print(buoy.id, buoy.behv, buoy.position, buoy.measure())


if __name__ == "__main__":
    main()
    # env = Env()
    # swarm = Swarm(env)
    # swarm.construct()
    # swarm.broadcast()
    # swarm.update()