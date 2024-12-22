import matplotlib.pyplot as plt
import numpy as np

# Data points for current (mA) and voltage
current = [0.4998, 0.8105, 1.2105, 1.538, 1.8961, 2.1671, 2.5265, 
           2.8822, 3.3455, 3.6365, 3.9128, 4.2825, 4.6254, 5.0245]
voltage = [35.14, 34.062, 29.483, 26.455, 24.698, 23.639, 22.518, 
           21.379, 20.297, 20.136, 19.944, 19.558, 19.472, 19.22]

# Calculate the slopes (gradients) between consecutive points
slopes = np.diff(voltage) / np.diff(current)

# Find the maximum slope
max_slope = np.max(slopes)
max_slope_index = np.argmax(slopes)

# Corresponding current and voltage points for the maximum slope
max_slope_point1 = (current[max_slope_index], voltage[max_slope_index])
max_slope_point2 = (current[max_slope_index + 1], voltage[max_slope_index + 1])

# Plotting the I-V curve
plt.figure(figsize=(8, 6))
plt.plot(current, voltage, marker='o', linestyle='-', color='b', label='I-V curve')

# Highlight the segment with the maximum slope
plt.plot(
    [max_slope_point1[0], max_slope_point2[0]],
    [max_slope_point1[1], max_slope_point2[1]],
    color='r', linestyle='--', label='Max Slope Segment'
)

# Adding labels and grid
plt.title("Вольт-Амперная Характеристика (ВАХ)", fontsize=14)
plt.xlabel("Ток (мА)", fontsize=12)
plt.ylabel("Напряжение (В)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(fontsize=12)
plt.tight_layout()

# Display the plot
plt.show()

