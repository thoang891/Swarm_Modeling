import os
import csv
from datetime import datetime

def log_settings(settings, filename='settings.csv', folder_path=None):
    # If folder path is not provided, create a new folder with a timestamp
    if folder_path is None:
        folder_path = create_log_folder()
    
    # Join the folder path with the filename to get the full path
    file_path = os.path.join(folder_path, filename)

    # Open the CSV file in write mode
    with open(file_path, 'w', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)
        
        # Write the header row
        writer.writerow(['Setting', 'Value'])
        
        # Write each setting and its value to the CSV file
        for setting, value in settings.items():
            writer.writerow([setting, value])

def log_buoy_data(current_time, all_data, folder_path):
    filename = os.path.join(folder_path, 'buoy_log.csv')
    # Open the CSV file in append mode to add new data
    with open(filename, 'a', newline='') as csvfile:
        # Create a CSV writer object
        writer = csv.DictWriter(csvfile, fieldnames=['Time', 'ID', 'behv', 'com_radius', 'Battery', 'Battery Percent', 'x', 'y', 'Measurement', 'u', 'v', 'speed', 'best_x', 'best_y', 'best_measure', 'best_id', 'N', 'Ns', 'Ne', 'Ni'])
        
        # Check if the file is empty and write the header row if needed
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write each buoy's data along with the current time to the CSV file
        for buoy_data in all_data:
            buoy_data['Time'] = current_time
            writer.writerow(buoy_data)

def create_log_folder():
    # Check if the "logs" folder exists, if not, create it
    logs_folder = "logs"
    if not os.path.exists(logs_folder):
        os.makedirs(logs_folder)

    # Create a folder with a timestamp label inside the "logs" folder
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_name = os.path.join(logs_folder, f"log_{timestamp}")
    os.makedirs(folder_name)
    return folder_name
