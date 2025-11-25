# -*- coding: utf-8 -*-
"""
Лабораторная 5.4.1 — обработка данных (без счётчика Гейгера).
Формат и подача как в примере отчёта: /mnt/data/5.4.1.pdf
Данные «зашиты» в скрипт массивами (взяты из Excel-файла пользователя).
Используется библиотека /mnt/data/lab_helper.py.
"""

import os
import sys
import numpy as np
import matplotlib.pyplot as plt

import lab_helper as lh

# --- исходные массивы из Excel (лист "Сцинт") ---
P_scin = [720.0, 710.0, 700.0, 690.0, 680.0, 670.0, 660.0, 650.0, 640.0, 630.0, 620.0, 610.0, 600.0, 590.0, 580.0, 570.0, 560.0, 550.0, 540.0]
N_scin = [3095.0, 2982.0, 2851.0, 2570.0, 4850.0, 4788.0, 4275.0, 3916.0, 3323.0, 3055.0, 2808.0, 3664.0, 3167.0, 2551.0, 2902.0, 2887.0, 2819.0, 2799.0, 2849.0]
t_scin = [10.0, 10.0, 10.0, 10.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 30.0, 30.0, 30.0, 40.0, 50.0, 60.0, 80.0, 100.0]

# --- исходные массивы из Excel (лист "Ион") ---
P_ion = [695.0, 675.0, 660.0, 650.0, 640.0, 620.0, 605.0, 580.0, 560.0, 550.0, 530.0, 510.0, 490.0, 470.0, 445.0, 430.0, 410.0, 390.0, 370.0, 350.0, 330.0, 310.0, 290.0, 280.0, 260.0, 240.0, 220.0, 200.0, 180.0, 160.0, 140.0, 120.0, 100.0, 80.0, 60.0, 210.0, 190.0, 170.0, 150.0, 130.0]
I_ion = [33.0, 61.0, 85.0, 96.0, 112.0, 138.0, 166.0, 196.0, 226.0, 242.0, 278.0, 310.0, 339.0, 372.0, 412.0, 439.0, 468.0, 511.0, 541.0, 577.0, 614.0, 649.0, 684.0, 702.0, 734.0, 762.0, 784.0, 802.0, 808.0, 810.0, 803.0, 794.0, 789.0, 790.0, 783.0, 801.0, 807.0, 811.0, 811.0, 805.0]

# --- параметры оформления/пересчёта ---
T_lab_C = 22.0           # температуа в лаборатории, °C
L_scin_cm = 9.0          # эффективная длина для сцинт. канала (пример)
L_ion_cm  = (10.0-0.5)/2 # эквивалентная длина пути для ионизационной камеры (пример)

# --- служебные функции ---
def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()

def bring_to_NTP_length(L_cm, P_mmHg, T_C):
    # Пересчёт к н.у.: 760 мм рт. ст., 15°C (288 K)
    T_K = 273.15 + T_C
    return L_cm * (P_mmHg/760.0) * (288.0/T_K)

def R_to_E_MeV(R_cm):
    # R[см] ≈ 0.32 * E^(3/2) => E[МэВ] ≈ (R/0.32)^(2/3)
    return (np.asarray(R_cm)/0.32)**(2.0/3.0)

# === 1) Сцинтилляционный метод ===
P_scin = np.asarray(P_scin, float)
N_scin = np.asarray(N_scin, float)
t_scin = np.asarray(t_scin, float)
rate = N_scin / t_scin

# Линейный участок: 580..700 мм
mask_s = (P_scin>=580) & (P_scin<=700)
(k_s, dk_s), (b_s, db_s) = lh.fit_linear(P_scin[mask_s], rate[mask_s])

baseline_low = rate[:4].mean()                 # «низкое плато»
P0_scin = (baseline_low - b_s) / k_s
R_scin_cm = bring_to_NTP_length(L_scin_cm, P0_scin, T_lab_C)
E_scin = R_to_E_MeV(R_scin_cm)

# График N(P)
outdir = os.path.join(os.getcwd(), 'lab_541_arrays_out')
os.makedirs(outdir, exist_ok=True)

plt.figure()
plt.scatter(P_scin, rate, label='Данные')
xx = np.linspace(P_scin.min(), P_scin.max(), 300)
plt.plot(xx, k_s*xx + b_s, label='Лин. участок [580..700]')
plt.axhline(baseline_low, ls='--', label='Базовая линия (низкое плато)')
plt.axvline(P0_scin, ls=':', label=f'P0 ≈ {P0_scin:.1f} мм')
plt.xlabel('P, мм рт. ст.'); plt.ylabel('Скорость счёта, 1/с')
plt.title('Сцинтилляционный счётчик: экстраполяция P0')
plt.legend()
savefig(os.path.join(outdir, 'scint_extrapolation.png'))

# === 2) Ионизационная камера ===
P_ion = np.asarray(P_ion, float)
I_ion = np.asarray(I_ion, float)

mask_i = (P_ion>=600) & (P_ion<=720)           # линейная часть спада
(k_i, dk_i), (b_i, db_i) = lh.fit_linear(P_ion[mask_i], I_ion[mask_i])
baseline_i = I_ion[P_ion<=610].mean()
P0_ion = (baseline_i - b_i) / k_i
R_ion_cm = bring_to_NTP_length(L_ion_cm, P0_ion, T_lab_C)
E_ion = R_to_E_MeV(R_ion_cm)

plt.figure()
plt.scatter(P_ion, I_ion, label='Данные')
xx2 = np.linspace(P_ion.min(), P_ion.max(), 300)
plt.plot(xx2, k_i*xx2 + b_i, label='Лин. участок [600..720]')
plt.axhline(baseline_i, ls='--', label='Базовая линия (≤610)')
plt.axvline(P0_ion, ls=':', label=f'P0 ≈ {P0_ion:.1f} мм')
plt.xlabel('P, мм рт. ст.'); plt.ylabel('I, пА')
plt.title('Ионизационная камера: экстраполяция P0')
plt.legend()
savefig(os.path.join(outdir, 'ion_extrapolation.png'))

# --- печать краткой сводки ---
print('P0 (scint) [мм]:', round(P0_scin,2))
print('R_scin (н.у.) [см]:', round(R_scin_cm,3), '  E_scin [МэВ]:', round(float(E_scin),3))
print('P0 (ion)   [мм]:', round(P0_ion,2))
print('R_ion  (н.у.) [см]:', round(R_ion_cm,3), '   E_ion  [МэВ]:', round(float(E_ion),3))

# Сохранение таблицы результатов
import csv
with open(os.path.join(outdir, 'results.csv'), 'w', newline='', encoding='utf-8') as f:
    w = csv.writer(f)
    w.writerow(['method','P0_mmHg','R_cm_NTP','E_MeV'])
    w.writerow(['scint', P0_scin, R_scin_cm, float(E_scin)])
    w.writerow(['ion',   P0_ion,  R_ion_cm,  float(E_ion)])

print('\nФайлы сохранены в:', outdir)
