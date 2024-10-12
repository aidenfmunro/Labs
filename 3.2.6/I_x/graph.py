import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

output_dir = "graphs"

# Data
x = np.array([242.0, 211.0, 187.5, 169.0, 153.0, 141.0, 130.5, 121.0, 113.0, 106.0])
I = np.array([240.5, 211.5, 188.7, 170.3, 155.2, 142.6, 131.8, 122.6, 114.6, 107.5])
sigma_x = np.array([0.5] * 10)  # errors in x
sigma_I = np.array([10.9, 8.2, 6.4, 5.2, 4.3, 3.6, 3.1, 2.6, 2.3, 2.0])  # errors in I

# Perform linear regression to get slope and intercept
slope, intercept, r_value, p_value, std_err = linregress(x, I)

# Create a range for the fitted line
x_fit = np.linspace(min(x), max(x), 100)
I_fit = slope * x_fit + intercept

# Create plot
plt.figure(figsize=(10, 6))
plt.errorbar(x, I, xerr=sigma_x, yerr=sigma_I, fmt='o', label='Data points', capsize=5, color='blue')

# Plot the best fit line
plt.plot(x_fit, I_fit, 'r-', label=f'Fit Line: I = {slope:.2f} * x + {intercept:.2f}')

# Annotate slope
plt.annotate(f'Slope: {slope:.2f}', xy=(0.05, 0.9), xycoords='axes fraction', fontsize=12, color='red')

# Labels and title
plt.xlabel('x, мм')
plt.ylabel('I, нА')
plt.legend()
plt.grid()

# Save the plot to a file
output_file = f"{output_dir}/combined_graph.png"
plt.savefig(output_file)

