import matplotlib.pyplot as plt
import numpy as np

# Data
delta_nu = np.array([49.9, 25.0, 17.0, 12.5, 10.0, 8.0, 7.0, 6.0, 5.8, 4.9])  # kHz
inv_tau = np.array([50.0, 25.0, 16.6, 12.5, 10, 8.3, 7.1, 6.2, 5.5, 5.0])  # 1/ms

# Assume symmetric error estimates
error_delta_nu = np.ones_like(delta_nu) * 0.5  # ±0.5 kHz
error_inv_tau = np.ones_like(inv_tau) * 0.5  # ±0.5 x 10^3 s^-1

# Perform a linear regression: y = mx + b, where x = inv_tau and y = delta_nu
coeffs = np.polyfit(inv_tau, delta_nu, 1)  # Degree 1 for linear fit
m, b = coeffs  # Slope and intercept
trendline = m * inv_tau + b  # Compute trendline values

# Plotting
plt.figure(figsize=(8, 6))
plt.errorbar(inv_tau, delta_nu, xerr=error_inv_tau, yerr=error_delta_nu, 
             fmt='o')
plt.plot(inv_tau, trendline, label=f"Trendline: $y = {m:.3f}x {b:.3f}$", 
         color='red', linestyle='--')

# Labels and title
plt.xlabel(r"$1/\tau \cdot 10^3$ (s$^{-1}$)", fontsize=12)
plt.ylabel(r"$\Delta \nu$ (kHz)", fontsize=12)
plt.grid(True)
plt.legend()

# Show the plot
plt.tight_layout()
plt.savefig('pictures/delta_nu.pdf')

