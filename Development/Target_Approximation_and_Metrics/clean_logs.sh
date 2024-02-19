#!/bin/bash

# Navigate to the parent directory of the logs folder
cd "$(dirname "$0")"

# Define the path to the logs folder
logs_folder="logs"

# Check if the logs folder exists
if [ -d "$logs_folder" ]; then
    # Remove all log folders within the logs folder
    rm -rf "$logs_folder"/*
    echo "Log folders cleaned."
else
    echo "No log folders found."
fi
