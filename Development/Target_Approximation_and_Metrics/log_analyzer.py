import os
import pandas as pd
import numpy as np

def accuracy(buoy_log, settings):
    # Input is the path to the buoy_log.csv and settings.csv

    # Read buoy_log.csv into a DataFrame
    buoy_log_df = pd.read_csv(buoy_log)
    settings_df = pd.read_csv(settings)

    # Create a new DataFrame to store the target guess
    target_guess = pd.DataFrame(columns=['Time','best_x_avg', 'best_y_avg', 'target_x', 'target_y', 'error_x', 'error_y', 'D_error', 'Time/Total Time', 'Accuracy'])

    # Copy the time steps to the target guess DataFrame
    target_guess['Time'] = buoy_log_df['Time'].unique()

    # Copy the target position to the target guess DataFrame, unique to each time
    target_x = buoy_log_df[buoy_log_df['ID'] == 'Target']['x'].reset_index()
    target_guess['target_x'] = target_x['x']

    target_y = buoy_log_df[buoy_log_df['ID'] == 'Target']['y'].reset_index()
    target_guess['target_y'] = target_y['y']

    # Calculate average best_x for each time step
    average_best_x = buoy_log_df.groupby('Time')['best_x'].mean().reset_index()
    target_guess['best_x_avg'] = average_best_x['best_x']

    # Calculate average best_y for each time step
    average_best_y = buoy_log_df.groupby('Time')['best_y'].mean().reset_index()
    target_guess['best_y_avg'] = average_best_y['best_y']

    # Calculate the error in x and y
    target_guess['error_x'] = target_guess['best_x_avg'] - target_guess['target_x']
    target_guess['error_y'] = target_guess['best_y_avg'] - target_guess['target_y']

    # Calculate distance error
    target_guess['D_error'] = np.sqrt(target_guess['error_x']**2 + target_guess['error_y']**2)

    # Find the row where Setting is "map_size" and get its corresponding Value
    map_size_value = float(settings_df[settings_df['Setting'] == 'map_size']['Value'].values[0])
    bounded_area = ((map_size_value) * 2)**2

    # Calculate Time/Total Time
    timesteps = float(settings_df[settings_df['Setting'] == 'timestep']['Value'].values[0])
    iterations = float(settings_df[settings_df['Setting'] == 'iterations']['Value'].values[0])
    total_time = timesteps * iterations
    target_guess['Time/Total Time'] = target_guess['Time'] / total_time

    # Calculate Accuracy
    target_guess['Accuracy'] = 1 - (target_guess['D_error'] / np.sqrt(bounded_area))


    print("Map size value:", map_size_value)
    print("Bounded area: {} m^2".format(bounded_area))

    print(target_guess)


# Function to analyze log data in a specific folder
def analyze_log_folder(folder_path):
    print("Analyzing logs in folder:", folder_path)
    buoy_log_path = os.path.join(folder_path, "buoy_log.csv")
    settings_path = os.path.join(folder_path, "settings.csv")
    
    # Check if buoy_log.csv exists in the folder
    if not os.path.exists(buoy_log_path):
        print("buoy_log.csv not found in folder:", folder_path)
        return

    accuracy(buoy_log_path, settings_path)

# Main function to iterate through log folders
def main():
    logs_folder_path = "./logs"  # Assuming logs folder is in the same directory as the script
    if not os.path.exists(logs_folder_path):
        print("Logs folder not found!")
        return

    # Iterate through each folder in the logs directory
    for folder_name in os.listdir(logs_folder_path):
        folder_path = os.path.join(logs_folder_path, folder_name)
        if os.path.isdir(folder_path):
            analyze_log_folder(folder_path)

if __name__ == "__main__":
    main()
