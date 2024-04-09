
# Path to the program 
PROGRAM=/Users/dobromiriliev/Documents/GitHub/Undulatory-Swimming-A-Topological-and-Computational-Model/TopologicalModel.py

# Number of times to run the program
NUM_RUNS=50

# Array to store execution times
declare -a execution_times

# Run the program NUM_RUNS times
for ((i=1; i<=$NUM_RUNS; i++))
do
    # Capture the output of the time command
    output=$(time -p $PROGRAM 2>&1)
    
    # Extract the real time (execution time) from the output
    execution_time=$(echo "$output" | grep -oP "(?<=real\s)\d+(\.\d+)?" | tail -n 1)
    
    # Store execution time in the array
    execution_times+=($execution_time)
    
    echo "Run $i: Execution time = $execution_time seconds"
done

