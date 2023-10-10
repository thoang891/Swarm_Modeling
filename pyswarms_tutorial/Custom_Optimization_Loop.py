# Import modules
import numpy as np

# Import sphere function as objective function
from pyswarms.utils.functions.single_obj import sphere as f

# Import backend modules
import pyswarms.backend as P
from pyswarms.backend.topology import Star

# for i in range(iterations):
#     for particle in swarm:
#         # Part 1: If current position is Less than the personal best,
#         if f(current_position[particle] < f(personal_best[particle]):
#              # Update the personal best
#              personal_best[particle] = current_position[particle]
#         # Part 2: If current position is Less than the global best,
#         if f(personal_best[particle]) < f(global_best):
#             # Update the global best
#             global_best = personal_best[particle]
#         # Part 3: Update the velocity and position matrices
#         update_velocity()
#         update_position()

# Initialize attributes of algorithm
my_topology = Star() # Create a topology instance
my_options = {'c1': 0.6, 'c2': 0.3, 'w': 0.4} # Create a options dictionary
my_swarm = P.create_swarm(n_particles=50, dimensions=2, options=my_options) # Create a swarm instance

print("The following are the attributes of our swarm: {}".format(my_swarm.__dict__.keys()))

# Optimization Loop
iterations = 1000
for i in range(iterations):
    # Part 1: Update personal best
    my_swarm.current_cost = f(my_swarm.position) # Compute current cost
    my_swarm.pbest_cost = f(my_swarm.pbest_pos) # Compute personal best pos
    my_swarm.pbest_pos, my_swarm.pbest_cost = P.compute_pbest(my_swarm) # Update and store

    # Part 2: Update global best
    # Note that gbest computation is dependent on your topology
    if np.min(my_swarm.pbest_cost) < my_swarm.best_cost:
        my_swarm.best_pos, my_swarm.best_cost = my_topology.compute_gbest(my_swarm)

    # Print output
    print("Iteration: {} | my_swarm.best_cost: {:.4f}".format(i+1, my_swarm.best_cost))

    # Part 3: Update position and velocity matrices
    # Note that position and velocity updates are dependent on your topology
    my_swarm.velocity = my_topology.compute_velocity(my_swarm)
    my_swarm.position = my_topology.compute_position(my_swarm)

print("The best cost found by our swarm is: {:.4f}".format(my_swarm.best_cost))
print("The best position found by our swarm is: {}".format(my_swarm.best_pos))
