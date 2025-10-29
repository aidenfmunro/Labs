# -*- coding: utf-8 -*-
"""
ЛР 5.8.1 — Проверка закона Стефана–Больцмана
График W = f2(T): зависимость мощности от температуры (в Кельвинах)
"""

import numpy as np
import matplotlib.pyplot as plt

# --------------------- Данные ---------------------
# Пирометрические температуры (°C)
T_C = np.array([959, 1069, 1162, 1234, 1334, 1478, 1550, 1650])
# Перевод в Кельвины
T_K = T_C + 273.15

# Напряжение (В)
U = np.array([1.73, 2.40, 3.06, 4.48, 5.74, 6.85, 8.44, 8.88])
# Ток (А)
I = np.array([0.481, 0.556, 0.624, 0.755, 0.859, 0.942, 1.053, 1.087])
# Мощность (Вт)
W = U * I

# --------------------- График ---------------------
plt.figure(figsize=(7,4.5))
plt.plot(T_K, W, 'o-', color='royalblue', linewidth=2, markersize=5)
plt.xlabel(r"$T$, K", fontsize=12)
plt.ylabel(r"$W$, мВт", fontsize=12)
plt.title(r"График $W = f_2(T)$", fontsize=13)
plt.grid(True, linestyle="--", alpha=0.5)
plt.tight_layout()
plt.savefig("W_f2_T.png", dpi=200)
plt.show()

