import matplotlib.pyplot as plt

# Data
frequencies = [300000, 600000, 900000, 1200000, 1500000, 1800000, 2100000, 2400000]
K_values = [0.1644444444, 0.09417040359, 0.05454545455, 0.03870967742, 0.03523809524,
            0.02673267327, 0.02435233161, 0.01467391304]

# Convert frequencies to kHz
frequencies_kHz = [f / 1000 for f in frequencies]

# Create the plot
plt.figure(figsize=(8, 6))
plt.scatter(frequencies_kHz, K_values, color='b')

# Labeling the plot
plt.xlabel('Частота (кГц)', fontsize=12)
plt.ylabel('K', fontsize=12)
plt.grid(True)

# Show the plot
plt.savefig('pictures/rc.pdf')

