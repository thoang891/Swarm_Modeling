
population = 25

    # Create a empty list to define experiments
experiments = []

    # populate experiments dictionary with experiment name as key and experiment parameters as value
for i in range(population):

        # Define the number of seekers and explorers and isocontours
        # Ni = population - i
        # Ne = i
        # Ns = 0
        
    Ni = i
    
    for j in range(population - i):
        Ne = j
        Ns = population - i - j

        experiment = {
            'seeker_population': Ns,
            'explorer_population': Ne,
            'isocontour_population': Ni,
            'sum': Ns + Ne + Ni,
        }

        # Append the experiment to the list of experiments
        experiments.append(experiment)

print(experiments)