# Undulatory Swimming A Topological Model and Computational Model
Project Created by Ricardo Guardado, Anish Goyal, and Dobromir Iliev
- The MATLab Synaptic Model implements a histogram-based Naive Bayes classifier tailored for analyzing synaptic data. It takes input from a file named "synaptic_data.txt" containing synaptic data, where each line represents a synaptic event with a corresponding time value. The code trains the classifier by binning the time values into a specified number of Gaussian bins and calculating the probability of occurrence for each bin. Then, it calculates the conditional probability of synaptic values given the time bins, considering the number of occurrences
within each time bin. However, it does not account for occurrences where no events are recorded. This model is designed to infer synaptic values based solely on the time of occurrences, 
ignoring periods without events.
