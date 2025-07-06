population_max = 50
index = 0
experiments = []

for population in range(1, population_max+1):
    for i in range(population):

        Ni = i

        for j in range(population - i):
            Ne = j
            Ns = population - i - j
            index += 1

            experiment = {
                "index": index,
                "Ni": Ni,
                "Ne": Ne,
                "Ns": Ns,
                "sum": Ni + Ne + Ns
            }

            experiments.append(experiment)

for num in experiments:
    print(num)