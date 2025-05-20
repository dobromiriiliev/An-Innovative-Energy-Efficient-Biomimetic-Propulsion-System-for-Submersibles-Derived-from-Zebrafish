#!/bin/bash

# Loop 50 times
for ((i=1; i<=50; i++))
do
    echo "Running analysis $i"
    memray run python TopologicalModel.py
    echo "-------------------------------------"
done
