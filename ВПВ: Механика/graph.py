import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(1, 120)
y = 0.01597 / np.sqrt(x)

plt.xlabel("x, м")
plt.ylabel("λ(x), кг/м")
plt.plot(x, y)
plt.show()
