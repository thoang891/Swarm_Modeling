import os
import csv
import pandas as pd
    
def compile_csv(experiment_path, log_path):
    experiment_data_path = os.path.join(log_path, 'experiment_data.csv')
    convergence_data_path = os.path.join(log_path, 'convergence_data.csv')
    
    # Check if the CSV files exist
    if os.path.exists(experiment_data_path) and os.path.exists(convergence_data_path):
        experiment_df = pd.read_csv(experiment_data_path)
        convergence_df = pd.read_csv(convergence_data_path)
        
        # Write data to new CSV files
        # Check to see if file already exists, if it does write a new one. If not, append the data.
        if os.path.exists(os.path.join(experiment_path, 'experiment_data_compiled.csv')):
            experiment_df.to_csv(os.path.join(experiment_path, 'experiment_data_compiled.csv'), mode='a', header=False)
        
        else:
            experiment_df.to_csv(os.path.join(experiment_path, 'experiment_data_compiled.csv'))
            
        if os.path.exists(os.path.join(experiment_path, 'convergence_data_compiled.csv')):
            convergence_df.to_csv(os.path.join(experiment_path, 'convergence_data_compiled.csv'), mode='a', header=False)
            
        else:
            convergence_df.to_csv(os.path.join(experiment_path, 'convergence_data_compiled.csv'))
            
def main():
    experiments_dir = "./experiments"
    
    if not os.path.exists(experiments_dir):
        print(f"Error: {experiments_dir} does not exist.")
        return
    
    # Iterate over each experiment folder
    for experiment in os.listdir(experiments_dir):
        experiment_path = os.path.join(experiments_dir, experiment)
        for log in os.listdir(experiment_path):
            log_path = os.path.join(experiment_path, log)
            if os.path.isdir(log_path):
                compile_csv(experiment_path, log_path)

if __name__ == "__main__":
    main()