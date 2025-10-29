# -*- coding: utf-8 -*-
"""
ЛР 5.8.1 — График ln(W/ε_T) = ln(σS) + n ln T
С погрешностями по обеим осям:
  X: ΔT = ±20 K  =>  Δ(lnT) = ΔT / T
  Y: ΔW/W = 4%   =>  Δ ln(W/ε_T) = ΔW/W   (ε_T табличная, без ошибки)
Данные (T_C, U, I) и таблица ε_T(T) вбиты вручную.
"""

import numpy as np
import matplotlib.pyplot as plt

# --------------------------- ДАННЫЕ ---------------------------
# Температуры по пирометру (°C) — из твоей таблицы
T_C = np.array([959, 1069, 1162, 1234, 1334, 1478, 1550, 1650], dtype=float)
# Перевод в Кельвины
T_K = T_C + 273.15

# Измеренные напряжение (В) и ток (А)
U = np.array([1.73, 2.40, 3.06, 4.48, 5.74, 6.85, 8.44, 8.88], dtype=float) * 10
I = np.array([0.481, 0.556, 0.624, 0.755, 0.859, 0.942, 1.053, 1.087], dtype=float)

# Электрическая мощность (Вт)
W = U * I

print(W)

# Таблица полной (термодинамической) эмиссивности ε_T(T) для вольфрама (из методички)
T_tab = np.array([800, 900, 1000, 1100, 1200, 1300, 1400, 1500,
                  1600, 1700, 1800, 1900, 2000], dtype=float)
eps_T_tab = np.array([0.067, 0.081, 0.105, 0.119, 0.133, 0.144, 0.164, 0.179,
                      0.195, 0.209, 0.223, 0.236, 0.249], dtype=float)

# Интерполяция ε_T на наши температуры
eps_T = np.interp(T_K, T_tab, eps_T_tab)

# ---------------------- ЛОГАРИФМЫ И ОШИБКИ --------------------
# Логарифмы
lnT = np.log(T_K)
lnW_over_eps = np.log(W / eps_T)

# Погрешности:
dT = 50.0                                      # K
dlnT = dT / T_K                                

rel_dW = 0.04                                   # 4% на W
dlnW_over_eps = np.full_like(lnW_over_eps, rel_dW) 

# ---------------------- ЛИНЕЙНАЯ АППРОКСИМАЦИЯ ----------------
# ln(W/ε_T) = n * lnT + c  (обычный МНК; ошибки используются для усиков)
X = np.vstack([lnT, np.ones_like(lnT)]).T
coef, residuals, rank, s = np.linalg.lstsq(X, lnW_over_eps, rcond=None)
n, c = coef

# Качество аппроксимации
yhat = n * lnT + c
ss_res = np.sum((lnW_over_eps - yhat)**2)
ss_tot = np.sum((lnW_over_eps - lnW_over_eps.mean())**2)
R2 = 1 - ss_res / ss_tot

# Оценка стандартных ошибок коэффициентов
N = len(lnT)
sigma2 = ss_res / (N - 2)
Sxx = np.sum((lnT - lnT.mean())**2)
se_n = np.sqrt(sigma2 / Sxx)
se_c = np.sqrt(sigma2 * (1/N + (lnT.mean()**2) / Sxx))

# --------------------------- ГРАФИК ---------------------------
plt.figure(figsize=(8,6))

# Точки с погрешностями по обеим осям
plt.errorbar(lnT, lnW_over_eps,
             xerr=dlnT, yerr=dlnW_over_eps,
             fmt='o', capsize=4, label="Экспериментальные точки")

# Прямая
xg = np.linspace(lnT.min(), lnT.max(), 200)
plt.plot(xg, n*xg + c, label=rf"$\ln(W/\varepsilon_T) = ({n:.2f}\pm{se_n:.2f})\,\ln T + ({c:.2f}\pm{se_c:.2f})$"
                         )

# Подписи и сетка
plt.xlabel(r"$\ln T, T (K)$")
plt.ylabel(r"$\ln(W/\varepsilon_T), W (мВт)$")
plt.title("Проверка закона Стефана–Больцмана")
plt.grid(True, linestyle='--', alpha=0.5)
plt.legend(loc="best")
plt.tight_layout()
plt.savefig("SB_lnW_over_eps_with_errors.png", dpi=200)
plt.show()

# -------------------------- ВЫВОД ----------------------------
print("=== Результаты аппроксимации ===")
print(f"n = {n:.3f} ± {se_n:.3f}")
print(f"c = {c:.3f} ± {se_c:.3f}")
print(f"R² = {R2:.4f}")
print("График сохранён в SB_lnW_over_eps_with_errors.png")

