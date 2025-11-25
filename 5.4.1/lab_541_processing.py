# -*- coding: utf-8 -*-
"""
Лабораторная 5.4.1 — обработка (без счётчика Гейгера).
Используется структура и приёмы из примера отчёта (фиты логистикой/линейной частью, пересчёт к н.у.).
Источник примера: /mnt/data/5.4.1.pdf
Входные данные: /mnt/data/8196effd-a7b6-4053-8664-5a98b9512b9b.xlsx (листы "Сцинт", "Ион")
Пользовательская библиотека: /mnt/data/lab_helper.py
Выход: графики PNG, сводка CSV/MD.
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# --- пользовательская библиотека с погрешностями/фитами ---
sys.path.append('/mnt/data')
import lab_helper as lh  # должен содержать fit_linear, err helpers, savefig, etc.

# ---- Параметры пересчёта и геометрии (редактируемые) ----
# Температура в лаборатории (°C) и атмосферное давление (мм рт. ст.)
T_lab_C = 22.0
P_atm_mmHg = 728.0

# Сцинтилляционный канал: расстояние источник—люминофор (см) при P≈760 мм рт. ст. и 15°C.
# В примере отчёта принят L_scin = 9 см (стр. 7).
L_scin_cm = 9.0

# Ионизационная камера: эквивалентная длина пути согласно геометрии (стр. 7): (10 - 0.5)/2 см.
L_ion_cm = (10.0 - 0.5) / 2.0

# Файл с данными
XLSX_PATH = '/mnt/data/8196effd-a7b6-4053-8664-5a98b9512b9b.xlsx'

# --- Утилиты ---
def to_mmHg(col):
    """Нормализовать колонку давления, вернуть float (мм рт. ст.)."""
    return pd.to_numeric(col, errors='coerce')

def ensure_dir(path):
    os.makedirs(path, exist_ok=True)
    return path

def savefig(path):
    plt.tight_layout()
    plt.savefig(path, dpi=140)
    plt.close()

def R_to_E_MeV(R_cm):
    """Энергия по эмпирическому закону R[см] ≈ 0.32 * E^(3/2) (воздух, ~15°C).
    E = (R/0.32)^(2/3)
    """
    return (np.asarray(R_cm) / 0.32) ** (2.0/3.0)

def bring_to_NTP_length(L_exp_cm, P_mmHg, T_C):
    """Пересчёт измеренной эффективной длины к н.у. (760 мм рт. ст., 15°C).
    R_nu = L_exp * (P/760) * (288K / T_K),
    где T_K = 273.15 + T_C, 288K соответствует 15°C.
    См. формулы на стр. 7 примера.
    """
    T_K = 273.15 + T_C
    return L_exp_cm * (P_mmHg / 760.0) * (288.0 / T_K)

# --- Чтение данных ---
xls = pd.ExcelFile(XLSX_PATH)
df_scin = pd.read_excel(xls, sheet_name='Сцинт')
df_ion  = pd.read_excel(xls, sheet_name='Ион')

# === 1) Сцинтилляционный счётчик: N(P) -> P0 -> R -> E ===
# Подготовка
sc = df_scin.copy()
# Скорость счета (1/с)
sc['rate'] = pd.to_numeric(sc.get('N'), errors='coerce') / pd.to_numeric(sc.get('t, c'), errors='coerce')
# Давление
if 'P, мм. рт. ст' in sc.columns:
    sc['P_mmHg'] = to_mmHg(sc['P, мм. рт. ст'])
else:
    sc['P_mmHg'] = to_mmHg(sc.iloc[:, 0])

sc = sc.dropna(subset=['P_mmHg', 'rate']).sort_values('P_mmHg').reset_index(drop=True)

# Выбор линейного участка спада/подъёма.
# В реальных данных наблюдается почти линейный рост rate с P в интервале ~580..700 мм.
mask_lin = (sc['P_mmHg'] >= 580) & (sc['P_mmHg'] <= 700)
desc = sc[mask_lin].copy()

x = desc['P_mmHg'].to_numpy(dtype=float)
y = desc['rate'].to_numpy(dtype=float)
(k_s, dk_s), (b_s, db_s) = lh.fit_linear(x, y)  # линейная аппроксимация

# Плато для пересечения — возьмём «низкое» плато при малых давлениях (первые 4 точки),
# как в методике определения P_экстр через пересечение.
baseline_low = sc.head(4)['rate'].mean()

# Давление отсечки (экстраполяция)
P0_scin = (baseline_low - b_s) / k_s

# Пересчёт в пробег: свободный путь равен L_scin при P≈760 и 15°C;
# при другом давлении/температуре пробег масштабируется пропорционально (стр. 7).
R_scin_cm = bring_to_NTP_length(L_scin_cm, P0_scin, T_lab_C)

# Энергия
E_scin_MeV = R_to_E_MeV(R_scin_cm)

# Графики
outdir = ensure_dir('/mnt/data/lab_541_out')
plt.figure()
plt.scatter(sc['P_mmHg'], sc['rate'], label='Данные', zorder=2)
xx = np.linspace(sc['P_mmHg'].min(), sc['P_mmHg'].max(), 300)
plt.plot(xx, k_s*xx + b_s, label='Лин. участок [580..700]', zorder=3)
plt.axhline(baseline_low, ls='--', label='Базовая линия (низкое плато)', zorder=1)
plt.axvline(P0_scin, ls=':', label=f'P0 ≈ {P0_scin:.1f} мм', zorder=1)
plt.xlabel('P, мм рт. ст.')
plt.ylabel('Скорость счёта, 1/с')
plt.title('Сцинтилляционный счётчик: экстраполяция P0')
plt.legend()
savefig(os.path.join(outdir, 'scint_extrapolation.png'))

# === 2) Ионизационная камера: I(P) -> P0 -> R -> E ===
ion = df_ion.copy()
ion['P_mmHg'] = to_mmHg(ion['P, мм рт ст'])
ion['I_pA']   = to_mmHg(ion['I, pA'])
ion = ion.dropna(subset=['P_mmHg', 'I_pA']).sort_values('P_mmHg').reset_index(drop=True)

# Для линейного участка берём область спада тока на высоких давлениях (~600..720 мм).
mask_lin2 = (ion['P_mmHg'] >= 600) & (ion['P_mmHg'] <= 720)
incl = ion[mask_lin2].copy()

x2 = incl['P_mmHg'].to_numpy(dtype=float)
y2 = incl['I_pA'].to_numpy(dtype=float)
(k_i, dk_i), (b_i, db_i) = lh.fit_linear(x2, y2)

# Базовая линия — среднее по «плато» до ~610 мм (ток почти постоянен).
baseline2 = ion[ion['P_mmHg'] <= 610]['I_pA'].mean()
P0_ion = (baseline2 - b_i) / k_i

# Пересчёт к н.у. (стр. 7): L_ion_cm — эффективная длина в геометрии камеры
R_ion_cm = bring_to_NTP_length(L_ion_cm, P0_ion, T_lab_C)
E_ion_MeV = R_to_E_MeV(R_ion_cm)

# Графики
plt.figure()
plt.scatter(ion['P_mmHg'], ion['I_pA'], label='Данные', zorder=2)
xx2 = np.linspace(ion['P_mmHg'].min(), ion['P_mmHg'].max(), 300)
plt.plot(xx2, k_i*xx2 + b_i, label='Лин. участок [600..720]', zorder=3)
plt.axhline(baseline2, ls='--', label='Базовая линия (≤610 мм)', zorder=1)
plt.axvline(P0_ion, ls=':', label=f'P0 ≈ {P0_ion:.1f} мм', zorder=1)
plt.xlabel('P, мм рт. ст.')
plt.ylabel('I, пА')
plt.title('Ионизационная камера: экстраполяция P0')
plt.legend()
savefig(os.path.join(outdir, 'ion_extrapolation.png'))

# === Сводка результатов ===
rows = [
    ['scint', 'P0_mmHg', P0_scin],
    ['scint', 'R_cm_NTP', R_scin_cm],
    ['scint', 'E_MeV', E_scin_MeV],
    ['ion',   'P0_mmHg', P0_ion],
    ['ion',   'R_cm_NTP', R_ion_cm],
    ['ion',   'E_MeV', E_ion_MeV],
]
res = pd.DataFrame(rows, columns=['method', 'quantity', 'value'])
res_path_csv = os.path.join(outdir, 'results.csv')
res.to_csv(res_path_csv, index=False, float_format='%.6g')

# Markdown-итог
md = f"""# Лаб. 5.4.1 — обработка (без Гейгера)

- Источник методики и примера оформления: *отчёт 5.4.1* (логистическая аппроксимация, пересчёт к н.у.).
- Данные: листы "Сцинт" и "Ион" из Excel.
- Температура T = {T_lab_C:.1f} °C, Pатм = {P_atm_mmHg:.1f} мм рт. ст.

## Итоги
| Метод | P0, мм | R (н.у.), см | E, МэВ |
|---|---:|---:|---:|
| Сцинт | {P0_scin:.2f} | {R_scin_cm:.3f} | {E_scin_MeV:.3f} |
| Ион   | {P0_ion:.2f}  | {R_ion_cm:.3f}  | {E_ion_MeV:.3f}  |

Графики: `scint_extrapolation.png`, `ion_extrapolation.png`.
"""
with open(os.path.join(outdir, 'README.md'), 'w', encoding='utf-8') as f:
    f.write(md)

print('Done. Files saved to:', outdir)
print(res)
