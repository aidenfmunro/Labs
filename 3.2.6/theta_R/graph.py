import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# Data
R_plus_R0_squared = np.array([590.9761, 740.3841, 961.6201, 1211.7361, 1490.7321,
                              1798.6081, 2135.3641, 2895.5161, 3771.1881,
                              4762.3801, 5869.0921])
inv_theta_squared = np.array([0.2977648442, 0.3990576272, 0.4904148618,
                               0.6029295135, 0.7120827516, 0.8500411318,
                               0.9265275017, 1.202724527, 1.473638085,
                               1.656250108, 2.159018888])
sigma_R_plus_R0_squared = np.array([8.842586231, 9.87680453, 12.55277229,
                                     15.543977, 19.14350221, 23.18402896,
                                     28.55975819, 39.84222688, 54.46880484,
                                     73.6971589, 92.21645372])
sigma_inv_theta_squared = np.array([0.003769401857, 0.00442809976, 0.005365082256,
                                     0.006515107737, 0.007756452485, 0.009346791847,
                                     0.01068283989, 0.01440192375, 0.01871224695,
                                     0.02278650229, 0.0302499799])

# Perform linear regression considering errors in y
slope, intercept, r_value, p_value, std_err = linregress(R_plus_R0_squared, inv_theta_squared)

# Generate fitted line
fit_line = slope * R_plus_R0_squared + intercept

# Create the plot
plt.figure(figsize=(10, 6))
plt.errorbar(R_plus_R0_squared, inv_theta_squared,
             xerr=sigma_R_plus_R0_squared,
             yerr=sigma_inv_theta_squared,
             fmt='o',
             label='Data points with errors',
             color='blue',
             capsize=5)

plt.plot(R_plus_R0_squared, fit_line,
         color='red',
         label=f'Fit line: y = {slope:.4f}x + {intercept:.4f}')

plt.title('Plot of (R + R_0)^2 vs 1/Θ^2')
plt.xlabel('(R + R_0)^2, кОм^2')
plt.ylabel('1/Θ^2')
plt.legend()
plt.grid()

# Show the plot
plt.show()
