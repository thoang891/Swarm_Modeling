import pandas as pd
import numpy as np
import csv
import os

def main():
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Specify the path to the CSV file
    csv_file = os.path.join(current_dir, 'buoy_log.csv')
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Create a new DataFrame to store the target guess
    target_guess = pd.DataFrame(columns=['Time', 'best_x_avg', 'best_y_avg', 'target_x', 'target_y'])

    # Copy the time steps to the target guess DataFrame
    target_guess['Time'] = df['Time'].unique()

    # Copy the target position to the target guess DataFrame, unique to each time
    target_x = df[df['ID'] == 'Target']['x'].reset_index()
    target_guess['target_x'] = target_x['x']
    target_y = df[df['ID'] == 'Target']['y'].reset_index()
    target_guess['target_y'] = target_y['y']

    # Calculate average best_x for each time step, but only for seekers
    average_best_x = df[df['behv'] == 'seeker'].groupby('Time')['best_x'].mean().reset_index()
    target_guess['best_x_avg'] = average_best_x['best_x']

    # Calculate average best_y for each time step, but only for seekers
    average_best_y = df[df['behv'] == 'seeker'].groupby('Time')['best_y'].mean().reset_index()
    target_guess['best_y_avg'] = average_best_y['best_y']

    target_guess['error_x'] = target_guess['best_x_avg'] - target_guess['target_x']
    target_guess['error_y'] = target_guess['best_y_avg'] - target_guess['target_y']

    target_guess['error'] = np.sqrt(target_guess['error_x']**2 + target_guess['error_y']**2)


    # Display the resulting DataFrame
    print(target_guess[0:100]) 

    # print the target_guess as a target_localization.csv
    write_csv_file = os.path.join(current_dir, 'target_localization.csv')
    target_guess.to_csv(write_csv_file, index=False)
    # target_guess.to_csv('target_guess.csv') # Need to generate it in the same folder


if __name__ == "__main__":
    main()
