#!/bin/bash

# Navigate to the parent directory of the logs folder
cd "$(dirname "$0")"

# Define the path to the experiments folder
experiments_folder="experiments"

# Check if the logs folder exists
if [ -d "$experiments_folder" ]; then
    # Remove all log folders within the logs folder
    rm -rf "$experiments_folder"/*
    echo "Experiments folders cleaned."
else
    echo "No experiment folders found."
fi
