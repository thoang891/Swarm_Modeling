# Example of PSO algorithm
# Not working as anticipated...

import random
import numpy as np
from tkinter import messagebox

# Define Class Particles
class Particle:
    def __init__ (self, position):
        self.position = position
        self.velocity = np.zeros_like(position)
        self.best_position = position
        self.best_fitness = float('inf')

def PSO(ObjF,Pop_Size,D,MaxT):
    swarm_best_position = None
    swarm_best_fitness = float('inf')
    particles = []

    # Position Initialization
    position = np.random.uniform(-0.5, 0.5, D)
    particle = Particle(position)
    particles.append(particle)

    # Fitness Update
    fitness = ObjF(position)
    if fitness < swarm_best_fitness:
        swarm_best_fitness = fitness
        swarm_best_position = position

        particle.best_position = position
        particle.best_fitness = fitness

    # PSO Main Loop
    for itr in range(MaxT):
        for particle in particles:
            # Update Velocity
            w = 0.8
            c1 = 1.2
            c2 = 1.2

            r1 = random.random()
            r2 = random.random()

            particle.velocity = (w * particle.velocity + c1 * r1 (particle.best_position-particle.position) + 
                                c2 * r1 + (swarm_best_position - particle.position))
            # New Position
            particle.position += particle.velocity

            # Evaluate Fitness
            fitness = ObjF(particle.position)

            # Update Personal Best
            if fitness < particle.best_fitness:
                particle.best_fitness = fitness
                particle.best_position = particle.position

            # Update Global Best
            if fitness < swarm_best_fitness:
                swarm_best_fitness = fitness
                swarm_best_position = particle.position
                
            return swarm_best_position, swarm_best_fitness
        
        # Parameters
        Pop_size = 100
        MaxT = 100
        D = 2

        # Define Objective Function
        def F1(x):
            return np.sum(x**2)
        
        Objective_Function = {
            'F1': F1,
        }

        # Iteration over ObjF using PSO

        for funName, ObjF in Objective_Function.items():
            Output = "Running function = " + funName + "\n"
            best_position, best_fitness = PSO(ObjF, Pop_size, D, MaxT)
            Output += "Best position found: " + str(best_position) + "\n"
            Output += "Best fitness found: " + str(best_fitness) + "\n"
            Output += "\n"

            messagebox.showinfo("Output", Output)
