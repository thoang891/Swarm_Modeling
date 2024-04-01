import os
import shutil

def main():
    logs_folder = "logs"
    experiments_folder = "experiments"

    # move folders of logs with folder to experiments folder but keep them contained in their individual folders
    for root, dirs, files in os.walk(logs_folder):
        for dir in dirs:
            shutil.move(os.path.join(root, dir), experiments_folder)
    

if __name__ == "__main__":
    main()