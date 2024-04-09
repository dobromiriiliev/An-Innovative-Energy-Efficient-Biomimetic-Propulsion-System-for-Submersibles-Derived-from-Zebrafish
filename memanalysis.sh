#!/bin/bash

# Path to the memory analysis tool
MEMORY_TOOL=/Users/dobromiriliev/Documents/GitHub/Undulatory-Swimming-A-Topological-and-Computational-Model/TopologicalModel.py

# Path to the program
PROGRAM=/Users/dobromiriliev/Documents/GitHub/Undulatory-Swimming-A-Topological-and-Computational-Model/TopologicalModel.py

# Loop 50 times
for ((i=1; i<=50; i++))
do
    echo "Running analysis $i"
    memray run /usr/bin/python3 /Users/dobromiriliev/Documents/GitHub/Undulatory-Swimming-A-Topological-and-Computational-Model/TopologicalModel.py
    echo "-------------------------------------"
done
