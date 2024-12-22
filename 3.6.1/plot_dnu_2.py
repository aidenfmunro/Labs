import matplotlib.pyplot as plt
import numpy as np

# Data
nu = np.array([5, 4, 3, 2, 1.5, 1, 0.8, 0.5, 0.2])  # kHz
delta_nu = np.array([4.970, 4.090, 3.000, 2.000, 1.500, 1.000, 0.820, 0.495, 0.200])  # kHz

# Symmetric error estimates
error_nu = np.ones_like(nu) * 0.1  # Example ±0.1 kHz for demonstration
error_delta_nu = np.ones_like(delta_nu) * 0.05  # Example ±0.05 kHz for demonstration

# Perform a linear regression: y = mx + b, where x = nu and y = delta_nu
coeffs = np.polyfit(nu, delta_nu, 1)  # Degree 1 for linear fit
m, b = coeffs  # Slope and intercept
trendline = m * nu + b  # Compute trendline values

# Plotting
plt.figure(figsize=(8, 6))

# Add data points
plt.scatter(nu, delta_nu, color='blue')

# Add explicit error crosses
for x, y, xerr, yerr in zip(nu, delta_nu, error_nu, error_delta_nu):
    plt.plot([x - xerr, x + xerr], [y, y], color='black', linewidth=1)  # Horizontal error
    plt.plot([x, x], [y - yerr, y + yerr], color='black', linewidth=1)  # Vertical error

# Add trendline
plt.plot(nu, trendline, label=f"Trendline: $y = {m:.3f}x + {b:.3f}$", 
         color='red', linestyle='--')

# Labels and title
plt.xlabel(r"$\nu$ (kHz)", fontsize=12)
plt.ylabel(r"$\delta \nu$ (kHz)", fontsize=12)
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.savefig('pictures/delta_nu_2.pdf')

