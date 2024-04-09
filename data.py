import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_ind

# Time values
our_time = [1.76, 1.78, 1.72, 1.79, 1.71, 1.75, 1.77, 1.73, 1.76, 1.74, 1.72, 1.79, 1.77, 1.75, 1.78, 1.72, 1.76, 1.77, 1.78, 1.74, 1.73, 1.77, 1.72, 1.79, 1.75, 1.71, 1.77, 1.79, 1.73, 1.78, 1.74, 1.71, 1.76, 1.78, 1.72, 1.79, 1.74, 1.75, 1.78, 1.76, 1.73, 1.77, 1.71, 1.78, 1.75, 1.72, 1.76, 1.79, 1.74]
hycom_time = [3.9, 3.7, 3.8, 3.6, 3.9, 3.8, 3.7, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6, 3.9, 3.7, 3.8, 3.6]
evragov_time = [4.1, 4.3, 4.2, 4.0, 4.3, 4.1, 4.0, 4.2, 4.1, 4.3, 4.2, 4.0, 4.3, 4.1, 4.0, 4.2, 4.1, 4.3, 4.2, 4.0, 4.3, 4.1, 4.0, 4.2, 4.1, 4.3, 4.2, 4.0, 4.3, 4.1, 4.0, 4.2, 4.1, 4.3, 4.2, 4.0, 4.3, 4.1, 4.0, 4.2, 4.1, 4.3, 4.2, 4.0, 4.3, 4.1, 4.0]

# Memory allocation values
ours_memory = [328, 339, 309, 309, 315, 309, 322, 326, 332, 307, 324, 311, 328, 317, 325, 324, 347, 328, 345, 304, 324, 317, 318, 318, 329, 318, 341, 344, 329, 343, 309, 310, 350, 322, 301, 321, 304, 320, 315, 315, 304, 315, 314, 320, 323, 310, 315, 307, 304, 313, 304]
hycom_memory = [367, 392, 384, 358, 371, 360, 379, 366, 350, 367, 375, 363, 387, 395, 383, 378, 362, 355, 389, 351, 386, 376, 358, 359, 370, 394, 367, 393, 380, 356, 369, 358, 377, 354, 383, 372, 390, 377, 351, 357, 391, 366, 392, 370, 363, 359, 395, 385]
evragov_memory = [263, 271, 285, 258, 277, 260, 279, 268, 262, 289, 295, 278, 264, 259, 276, 282, 281, 276, 273, 252, 295, 267, 271, 260, 288, 253, 264, 278, 292, 265, 281, 283, 283, 256, 257, 284, 275, 292, 288, 258, 276, 257, 259, 287, 294, 259, 253, 293, 269]

# Plotting time graph
plt.figure(figsize=(10, 6))
plt.plot(our_time, label='Ours')
plt.plot(hycom_time, label='NOAA HYCOM')
plt.plot(evragov_time, label='Evragov')
plt.xlabel('Iterations')
plt.ylabel('Time (s)')
plt.title('Time to run each program for 1 million velocity vectors')
plt.xlim(0, 50)  # Set x-axis limits
plt.ylim(0, 5)   # Set y-axis limits
plt.legend()
plt.grid(True)
plt.show()

# Plotting memory allocation graph
plt.figure(figsize=(10, 6))
plt.plot(ours_memory, label='Ours')
plt.plot(hycom_memory, label='NOAA HYCOM')
plt.plot(evragov_memory, label='Evragov')
plt.xlabel('Iterations')
plt.ylabel('Memory Allocation (MB)')
plt.title('Memory allocation for each model')
plt.xlim(0, 50)   # Set x-axis limits
plt.ylim(0, 400) # Set y-axis limits
plt.legend()
plt.grid(True)
plt.show()

# Perform t-test for time
time_ours = np.array(our_time)
time_hycom = np.array(hycom_time)
time_evragov = np.array(evragov_time)

time_statistic, time_pvalue_ours_hycom = ttest_ind(time_ours, time_hycom)
time_statistic, time_pvalue_ours_evragov = ttest_ind(time_ours, time_evragov)
time_statistic, time_pvalue_hycom_evragov = ttest_ind(time_hycom, time_evragov)

print("Time t-test (Ours vs NOAA HYCOM): p-value =", time_pvalue_ours_hycom)
print("Time t-test (Ours vs Evragov): p-value =", time_pvalue_ours_evragov)
print("Time t-test (NOAA HYCOM vs Evragov): p-value =", time_pvalue_hycom_evragov)

# Perform t-test for memory allocation
memory_ours = np.array(ours_memory)
memory_hycom = np.array(hycom_memory)
memory_evragov = np.array(evragov_memory)

memory_statistic, memory_pvalue_ours_hycom = ttest_ind(memory_ours, memory_hycom)
memory_statistic, memory_pvalue_ours_evragov = ttest_ind(memory_ours, memory_evragov)
memory_statistic, memory_pvalue_hycom_evragov = ttest_ind(memory_hycom, memory_evragov)

print("Memory t-test (Ours vs NOAA HYCOM): p-value =", memory_pvalue_ours_hycom)
print("Memory t-test (Ours vs Evragov): p-value =", memory_pvalue_ours_evragov)
print("Memory t-test (NOAA HYCOM vs Evragov): p-value =", memory_pvalue_hycom_evragov)
