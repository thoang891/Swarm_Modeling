"""
Author: Thinh Hoang

Description: This file contains the experiment runner script that runs a series of experiments by modifying the settings file and running the main script. The script defines a list of experiments by varying the parameters of the simulation. The script then iterates over each experiment, modifies the settings file, runs the main script, and saves the logs to a folder with a timestamp label. The script also creates a summary text file that contains a summary of the experiments run.

Contact:
- Email: hoangt@mit.edu
- GitHub: thoang891
"""

import os
import shutil
import importlib
from datetime import datetime
import experiment_analyzer

def experiment_setup():
    # Parameters for experiments
    population = 25

    # Create a empty list to define experiments
    experiments = []

    # populate experiments dictionary with variable name as key and experiment parameters as value
    # Key values must exactly match keys in settings.py
    for i in range(population):

        Ni = i
        
        for j in range(population - i):
            Ne = j
            Ns = population - i - j

            experiment = {
                'seeker_population': Ns,
                'explorer_population': Ne,
                'isocontour_population': Ni,
            }

            # Append the experiment to the list of experiments
            experiments.append(experiment)

    return experiments

def run_experiments(experiments=experiment_setup()):
    settings_file = 'settings.py'

    # Iterate over each experiment
    for experiment in experiments:
        # make a copy of the original settings file
        shutil.copy(settings_file, 'settings_backup.py')

        # open the settings file for modification
        with open(settings_file, 'r') as file:
            settings_content = file.read()

        for key, value in experiment.items():
            start_index = settings_content.find("{}".format(key))
            end_index = settings_content.find(',', start_index)
            settings_content = settings_content[:start_index] + '{}": {},'.format(key, value) + settings_content[end_index+1:]
        

        # write the modified settings content to the settings file
        with open(settings_file, 'w') as file:
            file.write(settings_content)

        # Run main.py
        os.system('python main.py')

        # Restore the original settings file
        shutil.copy('settings_backup.py', settings_file)

    # Clean up the backup settings file
    os.remove('settings_backup.py')

def create_folder():
     # Check if the "experiments" folder exists, if not, create it
    experiments_folder = "experiments"
    if not os.path.exists(experiments_folder):
        os.makedirs(experiments_folder)

    # Create a folder with a timestamp label inside the "experiments" folder
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_name = os.path.join(experiments_folder, f"experiment_{timestamp}")
    os.makedirs(folder_name)

    # Create a text file that contains a summary of experiments run
    with open(os.path.join(folder_name, 'summary.txt'), 'w') as file:
        file.write("Summary of Experiments:\n")
        for i, experiment in enumerate(experiment_setup()):
            file.write(f"Experiment {i+1}: {experiment}\n")

    return folder_name

def move_logs():
    # Get the paths to logs folder and experiments folder
    logs_folder = "logs"
    experiments_folder = create_folder()

    # Move contents of logs folder to experiments folder
    for root, dirs, files in os.walk(logs_folder):
        for dir in dirs:
            shutil.move(os.path.join(root, dir), experiments_folder)

if __name__ == '__main__':
    os.system('./clean_logs.sh')
    run_experiments()
    move_logs()
    experiment_analyzer.main()
