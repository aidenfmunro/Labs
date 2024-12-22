import numpy as np
import matplotlib.pyplot as plt

# Данные
boc_osn = [
    0.05117117117,
    0.1005405405,
    0.1531531532,
    0.2504504505,
    0.2990990991,
    0.354954955,
    0.4540540541,
    0.5045045045,
]
depth_percent = [10, 20, 30, 50, 60, 70, 90, 100]
depth_decimal = [x / 100 for x in depth_percent]

# Линейная аппроксимация
coefficients = np.polyfit(depth_decimal, boc_osn, 1)
poly = np.poly1d(coefficients)
line = poly(depth_decimal)

# Построение графика
plt.figure(figsize=(10, 5))
plt.plot(depth_decimal, line, marker="o", label=f"Прямая: $y = {coefficients[0]:.3f}x + {coefficients[1]:.3f}$", color='red')

# Добавление текста с уравнением прямой

# Оформление
plt.xlabel("Глубина (доли)")
plt.ylabel("$a_{бок}/a_{осн}$")
plt.grid()
plt.legend()
plt.savefig('pictures/depth.pdf')

