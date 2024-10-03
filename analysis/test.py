import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import ttest_rel

def analyze_and_plot_experiment_results(control, modified_design):
    data = np.array([control, modified_design])
    averages = np.mean(data, axis=1)
    std_devs = np.std(data, axis=1)
    _, p_value = ttest_rel(control, modified_design)

    labels = [f'Trial {i+1}' for i in range(len(control))]
    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    bars1 = ax.bar(x - width/2, control, width, yerr=std_devs[0], label='Control', color='#8e9cc3')
    bars2 = ax.bar(x + width/2, modified_design, width, yerr=std_devs[1], label='Modified Design', color='#1e3a8a')

    ax.set_xlabel('Trial')
    ax.set_ylabel('Average Power(kWh)')
    ax.set_title('Propulsion Model')
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha="right")
    
    ax.tick_params(axis='x', which='both', bottom=False, top=False)
    ax.margins(x=0.01)

    print("Average\tControl:", averages[0], "\tModified Design:", averages[1])
    print("Standard Deviation\tControl:", std_devs[0], "\tModified Design:", std_devs[1])
    print("P-Value\t\t", p_value)

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.2), title='Legend')

    plt.show()

control_values_test2 = np.array([0.06167, 0.05667, 0.06015, 0.05969, 0.05688, 0.05733, 0.05904, 0.06092, 0.06092, 0.06044, 0.05752, 0.05902, 0.05789, 0.06173, 0.05554])
modified_design_values_test2 = np.array([0.0516, 0.05508, 0.05035, 0.05138, 0.05016, 0.05421, 0.05245, 0.05315, 0.05411, 0.05411, 0.05462, 0.05113, 0.05385, 0.05262, 0.05051])

analyze_and_plot_experiment_results(control_values_test2, modified_design_values_test2)