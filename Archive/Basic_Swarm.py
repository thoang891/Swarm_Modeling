import numpy as np
import matplotlib.pyplot as plt

class Swarm:
    def __init__(self, n_agents, bounds):
        self.n_agents = n_agents
        self.bounds = bounds
        self.positions = np.random.uniform(bounds[0], bounds[1], size=(n_agents, 2))
        self.velocities = np.random.uniform(-1, 1, size=(n_agents, 2))

    def update(self, dt):
        # Update positions based on velocities
        self.positions += self.velocities * dt
        
        # Boundary conditions: Wrap-around
        self.positions = np.where(self.positions < self.bounds[0], self.bounds[1], self.positions)
        self.positions = np.where(self.positions > self.bounds[1], self.bounds[0], self.positions)

def visualize(swarm):
    plt.figure(figsize=(8, 8))
    plt.scatter(swarm.positions[:, 0], swarm.positions[:, 1], color='blue', s=10)
    plt.xlim(swarm.bounds[0][0], swarm.bounds[1][0])
    plt.ylim(swarm.bounds[0][1], swarm.bounds[1][1])
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Swarm Simulation')
    plt.grid(True)
    plt.show()

# Parameters
n_agents = 50
bounds = [(0, 0), (100, 100)]
dt = 0.1

# Create swarm
swarm = Swarm(n_agents, bounds)

# Main loop
for _ in range(100):
    swarm.update(dt)
    visualize(swarm)
