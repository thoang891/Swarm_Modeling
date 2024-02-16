import os
import csv
from datetime import datetime

# from settings import settings

def log_data():
    pass


def log_settings(settings, filename='settings.csv'):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create a folder with a timestamp
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    folder_name = f"logs_{timestamp}"
    folder_path = os.path.join(script_dir, folder_name)

    # Create the folder if it doesn't exist
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

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

# Example usage:
if __name__ == "__main__":
    from settings import settings
    log_settings(settings)