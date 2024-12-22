import numpy as np
import matplotlib.pyplot as plt

# Given data points
n = np.array([1, 2, 3, 4, 5, 6, 7])  # Actual values
f = np.array([3.9, 7.9, 11.9, 15.9, 19.9, 23.9, 27.9])  # Predicted values
f_error = 0.05  # Error in predicted values (f)

# Perform linear regression to find the slope and intercept of the trendline
slope, intercept = np.polyfit(n, f, 1)

# Generate the trendline using the equation y = mx + b
trendline = slope * n + intercept

# Calculate the error in intercept (simplified estimate based on error in f)
# Note: The error in the intercept is typically derived from the covariance matrix of the regression.
# This is a simplified estimation. A more accurate calculation would require more advanced statistics.
intercept_error = f_error * np.sqrt(np.sum((n - np.mean(n))**2)) / np.sum((n - np.mean(n))**2)

# Plot the data points with error bars
plt.errorbar(n, f, yerr=f_error, fmt='o', color='blue', markersize=5)

# Plot the trendline
plt.plot(n, trendline, color='red', label=f'Trendline: y = {slope:.2f}x + ({intercept:.2f} ± {intercept_error:.2f})')

# Add labels and title
plt.xlabel('n')
plt.ylabel('f, MHz')

plt.xticks(np.arange(min(n), max(n) + 1, 1))  # Major ticks on x-axis
plt.yticks(np.arange(min(f) - 1, max(f) + 2, 2))  # Major ticks on y-axis

# Add grid lines for better visibility
plt.grid(True, which='both', linestyle='--', linewidth=0.5)

# Display the slope, intercept, and intercept error in the plot
# Show legend
plt.legend()
plt.savefig('pictures/fig1.png')

# Display the plot
plt.show()

