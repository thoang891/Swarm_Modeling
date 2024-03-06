import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def analyze_swarm(folder_path, buoy_log, settings):
    # Input is the path to the buoy_log.csv and settings.csv and log folder path

    # Read buoy_log.csv and settings.csv into a DataFrame
    buoy_log_df = pd.read_csv(buoy_log)
    settings_df = pd.read_csv(settings)

    # Create a new DataFrame to store the target guess
    swarm_df = pd.DataFrame(columns=['Time','best_x_avg', 'best_y_avg', 'target_x', 'target_y', 
                                         'error_x', 'error_y', 'D_error', 'Time/Total Time', 
                                         'Accuracy', 'Battery', 'Non-Dimensional Battery'])

    # Copy the time steps to the target guess DataFrame
    swarm_df['Time'] = buoy_log_df['Time'].unique()

    # Copy the target position to the target guess DataFrame, unique to each time
    target_x = buoy_log_df[buoy_log_df['ID'] == 'Target']['x'].reset_index()
    swarm_df['target_x'] = target_x['x']

    target_y = buoy_log_df[buoy_log_df['ID'] == 'Target']['y'].reset_index()
    swarm_df['target_y'] = target_y['y']

    # Calculate average best_x for each time step
    average_best_x = buoy_log_df.groupby('Time')['best_x'].mean().reset_index()
    swarm_df['best_x_avg'] = average_best_x['best_x'].round(2)

    # Calculate average best_y for each time step
    average_best_y = buoy_log_df.groupby('Time')['best_y'].mean().reset_index()
    swarm_df['best_y_avg'] = average_best_y['best_y'].round(2)

    # Calculate the error in x and y
    swarm_df['error_x'] = (swarm_df['best_x_avg'] - swarm_df['target_x']).round(2)
    swarm_df['error_y'] = (swarm_df['best_y_avg'] - swarm_df['target_y']).round(2)

    # Calculate distance error
    swarm_df['D_error'] = np.sqrt(swarm_df['error_x']**2 + swarm_df['error_y']**2).round(3)

    # Find the row where Setting is "map_size" and get its corresponding Value to calculate bounded area
    map_size_value = float(settings_df[settings_df['Setting'] == 'map_size']['Value'].values[0])
    bounded_area = ((map_size_value) * 2)**2

    # Calculate Time/Total Time
    timesteps = float(settings_df[settings_df['Setting'] == 'timestep']['Value'].values[0])
    iterations = float(settings_df[settings_df['Setting'] == 'iterations']['Value'].values[0])
    total_time = timesteps * iterations
    swarm_df['Time/Total Time'] = (swarm_df['Time'] / total_time).round(3)

    # Calculate Accuracy in L dimension
    swarm_df['Accuracy'] = (1 - (swarm_df['D_error'] / np.sqrt(bounded_area))).round(3)

    # Calculate Accuracy in L^2 dimension
    # swarm_df['Accuracy'] = (1 - (swarm_df['D_error']**2 / bounded_area)).round(3)

    # Calculate maximum swarm battery in w*h
    seeker_battery = float(settings_df[settings_df['Setting'] == 'seeker_battery']
                           ['Value'].values[0])
    seeker_population = float(settings_df[settings_df['Setting'] == 'seeker_population']
                              ['Value'].values[0])

    explorer_battery = float(settings_df[settings_df['Setting'] == 'explorer_battery']
                             ['Value'].values[0])
    explorer_population = float(settings_df[settings_df['Setting'] == 'explorer_population']
                                ['Value'].values[0])

    isocontour_battery = float(settings_df[settings_df['Setting'] == 'iso_battery']
                               ['Value'].values[0])
    isocontour_population = float(settings_df[settings_df['Setting'] == 'isocontour_population']
                                  ['Value'].values[0])

    total_battery = ((seeker_battery * seeker_population) + 
                     (explorer_battery * explorer_population) + 
                     (isocontour_battery * isocontour_population))/(3600) # Convert to w*h from joules
    
    # Sum of all buoy battery at each time step
    battery_sum = buoy_log_df.groupby('Time')['Battery'].sum().reset_index()
    swarm_df['Battery'] = battery_sum['Battery']
    swarm_df['Battery'] = (swarm_df['Battery'] / (3600)).round(5) # Convert to w*h from joules

    # Calculate Non-Dimensional Battery
    swarm_df['Non-Dimensional Battery'] = (swarm_df['Battery'] / total_battery).round(3)

    # Write the DataFrame to a new CSV file
    swarm_csv = os.path.join(folder_path, 'swarm_analysis.csv')
    swarm_df.to_csv(swarm_csv, index=False)

    # plot time/ Total time vs Accuracy
    plt.plot(swarm_df['Time/Total Time'], swarm_df['Accuracy'])
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('Time/Total Time')
    plt.ylabel('Accuracy')
    plt.title('Time/Total Time vs Accuracy')
    
    # Save the plot as a PNG file in the log folder
    plot_file = os.path.join(folder_path, 'accuracy_plot.png')
    plt.savefig(plot_file)
    plt.clf()

    # plot time/ Total time vs Non-Dimensional Battery
    plt.plot(swarm_df['Time/Total Time'], swarm_df['Non-Dimensional Battery'])
    plt.xlim(0, 1)
    plt.xlabel('Time/Total Time')
    plt.ylabel('Non-Dimensional Battery')
    plt.title('Time/Total Time vs Non-Dimensional Battery')
    plot_file = os.path.join(folder_path, 'battery_plot.png')
    plt.savefig(plot_file)
    plt.clf()

    print(swarm_df)

def analyze_seekers(folder_path, buoy_log, settings):
    buoy_log_df = pd.read_csv(buoy_log)
    settings_df = pd.read_csv(settings)

    seeker_df = pd.DataFrame(columns=['Time', 'ID', 'x', 'y', 'u', 'v'])

    Proximity_Threshold = 0.05
    Ns = int(settings_df[settings_df['Setting'] == 'seeker_population']['Value'].values[0]) # Number of seekers
    Speed_Seeker = float(settings_df[settings_df['Setting'] == 
                                     'seeker_speed']['Value'].values[0]) # Speed of seekers
    Speed_Target = float(settings_df[settings_df['Setting'] == 
                                     'target_speed']['Value'].values[0]) # Speed of target

    # Remove all rows that are not "seeker" in behv column of buoy_log_df
    seeker_data = buoy_log_df[buoy_log_df['behv'] == 'seeker'].reset_index()

    seeker_df['Time'] = seeker_data['Time']
    seeker_df['ID'] = seeker_data['ID']
    seeker_df['x'] = seeker_data['x']
    seeker_df['y'] = seeker_data['y']
    seeker_df['u'] = seeker_data['u']
    seeker_df['v'] = seeker_data['v']

    # Extract the target position
    target_position = buoy_log_df.loc[buoy_log_df['ID'] == 'Target', ['Time', 'x', 'y']]

    # Merge the seeker DataFrame with the target position DataFrame on the 'Time' column
    seeker_df = pd.merge(seeker_df, target_position, on='Time', how='left', suffixes=('', '_target'))

    # Calculate the error in x and y
    seeker_df['error_x'] = (seeker_df['x_target'] - seeker_df['x']).round(2)
    seeker_df['error_y'] = (seeker_df['y_target'] - seeker_df['y']).round(2)

    # Calculate the distance error
    seeker_df['Distance to Target'] = np.sqrt(seeker_df['error_x']**2 + seeker_df['error_y']**2).round(3)

    # Calculate time/total time
    timestep = float(settings_df[settings_df['Setting'] == 'timestep']['Value'].values[0])
    iterations = float(settings_df[settings_df['Setting'] == 'iterations']['Value'].values[0])
    total_time = timestep * iterations
    seeker_df['Time/Total Time'] = (seeker_df['Time'] / total_time).round(3)

    # Calculate Non-Dimensional Target Proximity
    # Find the row where Setting is "map_size" and get its corresponding Value to calculate bounded area
    map_size_value = float(settings_df[settings_df['Setting'] == 'map_size']['Value'].values[0])
    bounded_area = ((map_size_value) * 2)**2

    seeker_df['Non-Dimensional Target Proximity'] = (seeker_df['Distance to Target'] / 
                                                     np.sqrt(bounded_area)).round(3)

    # Report the first first time Non-Dimenionsal Target Proximity is less than Proximity_Threshold if it exists
    filtered_df = seeker_df[seeker_df['Non-Dimensional Target Proximity'] < Proximity_Threshold]
    if not filtered_df.empty:
        first_time = filtered_df.iloc[0]['Time/Total Time']
        print("First time Non-Dimensional Target Proximity is less than Proximity Threshold: ", first_time)
        # Save this as a .txt file in the log folder
        seeker_time_file = os.path.join(folder_path, 'Seeker_Time.txt')
        with open(seeker_time_file, 'w') as file:
            file.write(f"First time Non-Dimensional Target Proximity is less than Proximity Threshold: {first_time}\n")
    else:
        print("No rows found where Non-Dimensional Target Proximity is less than Proximity Threshold.")
        seeker_time_file = os.path.join(folder_path, 'Seeker_Time.txt')
        with open(seeker_time_file, 'w') as file:
            file.write("No rows found where Non-Dimensional Target Proximity is less than Proximity Threshold.\n")

    # Calculate the total time spent within the threshold for all seekers
    if not filtered_df.empty:
        total_time_on_target = 0
        for idx in range(len(filtered_df) - 1):
            total_time_on_target += timestep
        
        time_on_target_percentage = (total_time_on_target / total_time) * 100
        average_time_on_target = total_time_on_target / Ns
        adjusted_time_on_target = average_time_on_target * (Speed_Target / Speed_Seeker) # Adjusted for speed difference
        print("Total time on target (as percentage of total simulation time):", time_on_target_percentage)
        print("Average time on target:", average_time_on_target)
        print("Adjusted time on target:", adjusted_time_on_target)
        # Save this as a .txt file in the log folder
        with open(seeker_time_file, 'a') as file:
            file.write(f"Total time Non-Dimensional Target Proximity is less than Proximity Threshold(as percentage of total simulation time): {time_on_target_percentage}\n")
            file.write(f"Average time on target: {average_time_on_target}\n")
            file.write(f"Adjusted time on target: {adjusted_time_on_target}\n")
    else:
        print("No rows found where Non-Dimensional Target Proximity is less than Proximity Threshold.")
        # time_on_target_file = os.path.join(folder_path, 'Time_on_Target.txt')
        with open(seeker_time_file, 'a') as file:
            file.write("No rows found where Non-Dimensional Target Proximity is less than Proximity Threshold.\n")

    # Heading-Bearing Correlation
    # Normalize the error x and error y vectors
    seeker_df['error_x_norm'] = (seeker_df['error_x'] / seeker_df['Distance to Target']).round(3)
    seeker_df['error_y_norm'] = (seeker_df['error_y'] / seeker_df['Distance to Target']).round(3)

    # Calculate the dot product of the normalized error vectors and the velocity vectors and divide by the magnitude of the velocity vector
    magnitude = np.sqrt(seeker_df['u']**2 + seeker_df['v']**2)
    seeker_df['Heading-Bearing Correlation'] = (seeker_df['error_x_norm']*seeker_df['u'] +
                                                seeker_df['error_y_norm']*seeker_df['v'])/magnitude.round(3)
    
    # Write the DataFrame to a new CSV file
    seeker_csv = os.path.join(folder_path, 'seeker_analysis.csv')
    seeker_df.to_csv(seeker_csv, index=False)

    # plot time/Total time vs Non-Dimensional Target Proximity for each unique ID
    for ID in seeker_df['ID'].unique():
        seeker_ID = seeker_df[seeker_df['ID'] == ID]
        plt.plot(seeker_ID['Time/Total Time'], seeker_ID['Non-Dimensional Target Proximity'], label=ID)

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xlabel('Time/Total Time')
    plt.ylabel('Non-Dimensional Target Proximity')
    plt.title('Time/Total Time vs Non-Dimensional Target Proximity')
    plt.legend(title='ID', bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plot_file = os.path.join(folder_path, 'seeker_proximity_plot.png')
    plt.savefig(plot_file, bbox_inches='tight')
    plt.clf()

    # Build bar graph of Heading-Bearing Correlation normalized by iterations and number of seekers, if there is a target
    if settings_df[settings_df['Setting'] == 'target_setting']['Value'].values[0] == 'ON':
        hist, bins, _ = plt.hist(seeker_df['Heading-Bearing Correlation'], 
                                bins=10, alpha=0.5, label='Heading-Bearing Correlation')
        hist = hist / (iterations * Ns)
        plt.clf()
        plt.bar(bins[:-1], hist, width=(bins[1]-bins[0]), alpha=0.5, label='Heading-Bearing Correlation')
        plt.xlabel('Heading-Bearing Correlation')
        plt.ylabel('Normalized Frequency')
        plt.title('Normalized Heading-Bearing Correlation')
        plt.legend(loc='upper center')  # Place the legend in the upper center

        # Add upper and lower bound of each bin to x-axis labels
        bin_labels = [f'{bins[i]:.2f} - {bins[i+1]:.2f}' for i in range(len(bins)-1)]
        plt.xticks(bins[:-1], bin_labels, rotation=45, ha='right')  # Rotate labels at 45-degree angle

        # Add y-value at the top of each bar
        for i, v in enumerate(hist):
            plt.text(bins[i], v, f'{v:.2f}', ha='center', va='bottom')

        plot_file = os.path.join(folder_path, 'heading_bearing_correlation.png')
        plt.savefig(plot_file, bbox_inches='tight')  # Add bbox_inches='tight' to prevent cutting off axis labels
        plt.tight_layout()  # Adjust subplot parameters to prevent overlapping
        plt.clf()

    print(seeker_df)
    
def analyze_coverage(folder_path, buoy_log, settings):
    buoy_log_df = pd.read_csv(buoy_log)
    settings_df = pd.read_csv(settings)

    # Obtain the communication radius for seekers
    rc_s = float(settings_df[settings_df['Setting'] == 'seeker_com_radius']['Value'].values[0])
    com_area_s = np.pi * (rc_s**2)

    # Obtain the communication radius for explorers and calculate the communication area
    rc_e = float(settings_df[settings_df['Setting'] == 'explorer_com_radius']['Value'].values[0])
    com_area_e = np.pi * (rc_e**2)

    # Obtain the communication radius for isocontours and calculate the communication area
    rc_i = float(settings_df[settings_df['Setting'] == 'iso_com_radius']['Value'].values[0])
    com_area_i = np.pi * (rc_i**2)

    # Create a mapping of behavior to communication area
    com_area_map = {'seeker': com_area_s, 
                    'explorer': com_area_e, 
                    'isocontour': com_area_i}

    # Obtain the bounded area
    map_size_value = float(settings_df[settings_df['Setting'] == 'map_size']['Value'].values[0])
    bounded_area = ((map_size_value) * 2)**2

    # Create a new DataFrame to store the coverage data
    coverage_df = pd.DataFrame(columns=['Time', 'ID', 'behv', 'N'])
    coverage_composite_df = pd.DataFrame(columns=['Time', 'Time/Total Time', 'Non-Dimensional Area Coverage'])

    coverage_df['Time'] = buoy_log_df['Time']
    coverage_df['ID'] = buoy_log_df['ID']
    coverage_df['behv'] = buoy_log_df['behv']
    coverage_df['N'] = buoy_log_df['N']
    
    # Calculate area coverage as behavior specfic communication area divided by number of neighbors "N" plus self
    coverage_df['comm_area'] = coverage_df['behv'].map(com_area_map)
    coverage_df['Area Coverage'] = (coverage_df['comm_area'] / (coverage_df['N'] + 1)).round(3)

    # Sum Area Coverage for each unique time
    coverage_composite_df = coverage_df.groupby('Time')['Area Coverage'].sum().round(2).reset_index()

    # Calculate time/total time
    timestep = float(settings_df[settings_df['Setting'] == 'timestep']['Value'].values[0])
    iterations = float(settings_df[settings_df['Setting'] == 'iterations']['Value'].values[0])
    total_time = timestep * iterations
    coverage_composite_df['Time/Total Time'] = (coverage_composite_df['Time'] / total_time).round(3)

    # Rename column for consistency
    coverage_composite_df = coverage_composite_df.rename(columns={'Area Coverage': 'Sum Area Coverage'})

    # Calculate Non-Dimensional Area Coverage
    coverage_composite_df['Non-Dimensional Area Coverage'] = (coverage_composite_df['Sum Area Coverage'] / bounded_area).round(3)

    # Write the DataFrame to a new CSV file
    coverage_csv = os.path.join(folder_path, 'coverage_analysis.csv')
    coverage_df.to_csv(coverage_csv, index=False)

    coverage_composite_csv = os.path.join(folder_path, 'coverage_composite_analysis.csv')
    coverage_composite_df.to_csv(coverage_composite_csv, index=False)

    # plot time/Total time vs Non-Dimensional Area Coverage
    plt.plot(coverage_composite_df['Time/Total Time'], coverage_composite_df['Non-Dimensional Area Coverage'])
    plt.xlim(0, 1)
    plt.xlabel('Time/Total Time')
    plt.ylabel('Non-Dimensional Area Coverage')
    plt.title('Time/Total Time vs Non-Dimensional Area Coverage')

    # Add dashed red line at y=1 and label it as "Ideal"
    plt.axhline(y=1, color='r', linestyle='--')
    plt.text(0.5, 1.05, 'Ideal', horizontalalignment='center', verticalalignment='center')
    
    plot_file = os.path.join(folder_path, 'coverage_plot.png')
    plt.savefig(plot_file)
    plt.clf()

    print(coverage_df)
    print(coverage_composite_df)

def analyze_isocontours(folder_path, buoy_log, settings):
    buoy_log_df = pd.read_csv(buoy_log)
    settings_df = pd.read_csv(settings)
    
    # Obtain the isocontour and communucations radius goal from settings
    iso_goal = float(settings_df[settings_df['Setting'] == 'isocontour_goal']['Value'].values[0])
    rc = float(settings_df[settings_df['Setting'] == 'iso_com_radius']['Value'].values[0])

    # Create a new DataFrame to store the isocontour data
    isocontour_df = pd.DataFrame(columns=['Time', 'ID', 'z'])

    isocontour_data = buoy_log_df[buoy_log_df['behv'] == 'isocontour'].reset_index()
    isocontour_df['Time'] = isocontour_data['Time']
    isocontour_df['ID'] = isocontour_data['ID']
    isocontour_df['Measurement'] = isocontour_data['Measurement']
    isocontour_df['x'] = isocontour_data['x']
    isocontour_df['y'] = isocontour_data['y']
    isocontour_df['Ni'] = isocontour_data['Ni']

    # Calculate linear coverage as 2 x communications radius divided by number of neighbor isocontours plus self
    isocontour_df['Linear Coverage'] = (2 * rc / (isocontour_df['Ni'] + 1)).round(3)

    # Calculate absolute fraction of measurement over isocontour goal where z is the scalar measurement
    isocontour_df['Abs(zi/z_goal)'] = (np.abs(isocontour_df['Measurement'] / iso_goal)).round(3)

    # Take natural log of the absolute fraction
    isocontour_df['Log10(Abs(zi/z_goal))'] = abs(np.log10(isocontour_df['Abs(zi/z_goal)'])).round(3)

    # Create a new dataframe for averaging the performance of the isocontour behavior at each timestep
    Ni = int(settings_df[settings_df['Setting'] == 'isocontour_population']['Value'].values[0])
    isocontour_performance_df = isocontour_df.groupby('Time')['Log10(Abs(zi/z_goal))'].sum().reset_index()
    isocontour_performance_df['Log10(Abs(zi/z_goal))'] = (isocontour_performance_df['Log10(Abs(zi/z_goal))'] / Ni).round(3)
    isocontour_performance_df = isocontour_performance_df.rename(columns={'Log10(Abs(zi/z_goal))': 'Average Abs(Log10(Abs(zi/z_goal)))'})

    # Sum linear coverage for each unique time
    sum_linear_coverage_df = isocontour_df.groupby('Time')['Linear Coverage'].sum().round(2).reset_index()
    isocontour_performance_df['Sum Linear Coverage'] = sum_linear_coverage_df['Linear Coverage']

    # Calculate time/total time
    timestep = float(settings_df[settings_df['Setting'] == 'timestep']['Value'].values[0])
    iterations = float(settings_df[settings_df['Setting'] == 'iterations']['Value'].values[0])
    total_time = timestep * iterations
    isocontour_performance_df['Time'] = isocontour_df['Time'].unique()
    isocontour_performance_df['Time/Total Time'] = (isocontour_performance_df['Time'] / total_time).round(3)

    # At each time step, find the maximum and minimum x and y coordinates
    max_x = isocontour_df.groupby('Time')['x'].max().reset_index()
    max_y = isocontour_df.groupby('Time')['y'].max().reset_index()
    min_x = isocontour_df.groupby('Time')['x'].min().reset_index()
    min_y = isocontour_df.groupby('Time')['y'].min().reset_index()
    isocontour_performance_df['max_x'] = max_x['x']
    isocontour_performance_df['max_y'] = max_y['y']
    isocontour_performance_df['min_x'] = min_x['x']
    isocontour_performance_df['min_y'] = min_y['y']

    # Estimate the perimeter of the isocontour at each time step as a rectangle
    isocontour_performance_df['Perimeter'] = 2 * (isocontour_performance_df['max_x'] - isocontour_performance_df['min_x'])
    isocontour_performance_df['Perimeter'] += 2 * (isocontour_performance_df['max_y'] - isocontour_performance_df['min_y'])
    isocontour_performance_df['Perimeter'] = isocontour_performance_df['Perimeter'].round(2)

    # Calculate Sum Linear Coverage/Perimeter for each time
    isocontour_performance_df['Sum Linear Coverage/Perimeter'] = (isocontour_performance_df['Sum Linear Coverage'] /
                                                                isocontour_performance_df['Perimeter']).round(3)

    # Write the DataFrames to a new CSV file
    isocontour_csv = os.path.join(folder_path, 'isocontour_analysis.csv')
    isocontour_df.to_csv(isocontour_csv, index=False)

    performance_csv = os.path.join(folder_path, 'isocontour_performance_analysis.csv')
    isocontour_performance_df.to_csv(performance_csv, index=False)

    # plot time/Total time vs Average Log(Abs(zi/z_goal))
    plt.plot(isocontour_performance_df['Time/Total Time'], isocontour_performance_df['Average Abs(Log10(Abs(zi/z_goal)))'])
    plt.xlim(0, 1)
    plt.xlabel('Time/Total Time')
    plt.ylabel('Average Log10(Abs(zi/z_goal))')
    plt.title('Time/Total Time vs Relative Isocontour Accuracy)')

    # Add dashed red line at y=0
    plt.axhline(y=0, color='r', linestyle='--')
    plt.text(0.5, 0.05, 'Ideal', horizontalalignment='center', verticalalignment='center', color='r')

    plot_file = os.path.join(folder_path, 'isocontour_accuracy_plot.png')
    plt.savefig(plot_file)
    plt.clf()

    # plot time/Total time vs Sum Linear Coverage/Perimeter
    plt.plot(isocontour_performance_df['Time/Total Time'], isocontour_performance_df['Sum Linear Coverage/Perimeter'])
    plt.xlim(0, 1)
    plt.ylim(0, 1.5)
    plt.xlabel('Time/Total Time')
    plt.ylabel('Sum Linear Coverage/Perimeter')
    plt.title('Time/Total Time vs Relative Fractional Spreading')

    plt.axhline(y=1, color='r', linestyle='--')
    plt.text(0.5, 1.05, 'Ideal', horizontalalignment='center', verticalalignment='center', color='r')

    plot_file = os.path.join(folder_path, 'isocontour_spreading_plot.png')
    plt.savefig(plot_file)
    plt.clf()

    print(isocontour_df)
    print(isocontour_performance_df)

# Function to analyze log data in a specific folder
def analyze_log_folder(folder_path):
    print("Analyzing logs in folder:", folder_path)
    buoy_log_path = os.path.join(folder_path, "buoy_log.csv")
    settings_path = os.path.join(folder_path, "settings.csv")
    
    # Check if buoy_log.csv exists in the folder
    if not os.path.exists(buoy_log_path):
        print("buoy_log.csv not found in folder:", folder_path)
        return
    
    print("Analyzing swarm data...")
    analyze_swarm(folder_path, buoy_log_path, settings_path)

    print("Analyzing seeker data...")
    analyze_seekers(folder_path, buoy_log_path, settings_path)
    
    print("Analyzing coverage data...")
    analyze_coverage(folder_path, buoy_log_path, settings_path)

    print("Analyzing isocontour data...")
    analyze_isocontours(folder_path, buoy_log_path, settings_path)

    print("Analysis complete for folder:", folder_path)

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
