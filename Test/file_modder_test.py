import os
import shutil
import importlib

def main():

    settings_file = 'settings.py'

    # Overwrite seeker_population value in settings.py

    shutil.copy(settings_file, 'settings_backup.py')

    with open(settings_file, 'r') as file:
        settings_content = file.read()

    # Modify the "seeker_population" key,value pair in settings_content
    start_index = settings_content.find("seeker_population")
    end_index = settings_content.find(',', start_index)
    settings_content = settings_content[:start_index] + 'seeker_population": 10,' + settings_content[end_index+1:]

    with open(settings_file, 'w') as file:
        file.write(settings_content)

if __name__ == '__main__':
    main()