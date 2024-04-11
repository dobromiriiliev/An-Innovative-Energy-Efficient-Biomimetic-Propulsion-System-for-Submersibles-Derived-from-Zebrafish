#!/bin/bash

# Define the path to the Python script
PYTHON_SCRIPT="/Users/dobromiriliev/Documents/GitHub/Undulatory-Swimming-A-Topological-and-Computational-Model/TopologicalModel.py"

# Array to store initialization times
initialization_times=()

# Run the Python script 50 times
for ((i=1; i<=50; i++))
do
    # Execute the Python script and capture output
    output=$(python3 "$PYTHON_SCRIPT" | grep "Initialization time:")
    # Extract initialization time from output
    init_time=$(echo "$output" | awk '{print $3}')
    # Add initialization time to array
    initialization_times+=("$init_time")
done

# Print the initialization times array
echo "Initialization times:"
echo "${initialization_times[@]}"
