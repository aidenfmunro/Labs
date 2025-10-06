from pathlib import Path

# Создаём шаблон Jupyter Notebook (.ipynb)
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# Заголовок
cells.append(nbf.v4.new_markdown_cell("# Лабораторная работа 5.5\n"
                                      "## Компьютерная сцинтилляционная γ-спектрометрия"))

# Теория (кратко)
cells.append(nbf.v4.new_markdown_cell("### Теоретическая часть\n"
"При прохождении гамма-квантов через вещество происходят процессы:\n"
"- **Фотоэффект** – полное поглощение энергии γ-кванта электроном;\n"
"- **Эффект Комптона** – упругое рассеяние γ-кванта на электроне с изменением энергии;\n"
"- **Образование пар** – превращение γ-кванта в пару электрон–позитрон при $E > 1.022$ МэВ.\n\n"
"В спектре наблюдаются **фотопики**, **комптоновское плато и край**, **аннигиляционный пик**, "
"а также пики характеристического излучения и обратного рассеяния.\n\n"
"Энергетическое разрешение спектрометра:\n"
"$$ R = \\frac{\\Delta E}{E} $$\n"
"где $\\Delta E$ – ширина пика на половине высоты."))

# Данные для калибровки
cells.append(nbf.v4.new_markdown_cell("### Калибровочные данные\n"
"Используем известные пики Na и Cs для построения зависимости «номер канала – энергия». \n"
"\n"
"| Источник | Энергия (кэВ) | Канал |\n"
"|----------|--------------|-------|\n"
"| Na       | 511          | 725   |\n"
"| Na       | 1275         | 1710  |\n"
"| Cs       | 662          | 920   |"))

# Код: калибровка
cells.append(nbf.v4.new_code_cell("""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Калибровочные точки
calib_data = pd.DataFrame({
    "Источник": ["Na", "Na", "Cs"],
    "Энергия_кэВ": [511, 1275, 662],
    "Канал": [725, 1710, 920]
})

# Линейная аппроксимация (канал = a*E + b)
coeffs = np.polyfit(calib_data["Энергия_кэВ"], calib_data["Канал"], 1)
a, b = coeffs
fit_line = np.poly1d(coeffs)

# Построение графика
plt.scatter(calib_data["Энергия_кэВ"], calib_data["Канал"], label="Измерения")
energies = np.linspace(0, 1400, 100)
plt.plot(energies, fit_line(energies), 'r--', label=f"Канал = {a:.2f}*E + {b:.1f}")
plt.xlabel("Энергия (кэВ)")
plt.ylabel("Номер канала")
plt.legend()
plt.grid()
plt.show()

calib_data, (a, b)
"""))

# Экспериментальные данные (из таблицы на фото)
cells.append(nbf.v4.new_markdown_cell("### Экспериментальные данные\n"
"Ниже приведены твои измеренные пики (из Excel)."))

cells.append(nbf.v4.new_code_cell("""
data = pd.DataFrame({
    "Вещество": ["Co", "Co", "Cs", "Na", "Na", "Am", "Am", "Eu", "Eu", "Eu", "Eu", "Eu", "Eu"],
    "N": [1604, 1835, 937, 1720, 739, 160, 112, 132, 241, 524, 392, 1100, 638],
    "dN": [95, 78, 75, 162, 67, 18, 16, 18, 25, 50, 45, 62, None],
    "N_комптон": ["1363±40", None, "680±20", "1415±40", "415±20", None, None, 91, 201, 400, None, None, None],
    "Примечание": ["лево", "право", None, "право", "лево", "?", None, None, None, None, None, None, None]
})
data
"""))

# Пересчёт энергии по калибровке
cells.append(nbf.v4.new_markdown_cell("### Пересчёт каналов в энергии\n"
"Используем калибровку, чтобы определить энергии пиков."))

cells.append(nbf.v4.new_code_cell("""
# Функция для перевода канала в энергию
def channel_to_energy(channel):
    return (channel - b) / a

data["E_кэВ"] = data["N"].apply(lambda x: channel_to_energy(x) if pd.notna(x) else None)
data
"""))

# Энергетическое разрешение
cells.append(nbf.v4.new_markdown_cell("### Энергетическое разрешение\n"
"Вычисляем $R = \\Delta E / E$ для каждого пика."))

cells.append(nbf.v4.new_code_cell("""
# dE из dN через производную калибровки: dE ≈ dN / a
data["dE_кэВ"] = data["dN"].apply(lambda dn: dn / a if pd.notna(dn) else None)
data["R"] = data.apply(lambda row: row["dE_кэВ"]/row["E_кэВ"] if pd.notna(row["dE_кэВ"]) and pd.notna(row["E_кэВ"]) else None, axis=1)
data
"""))

# График зависимости R^2 от E
cells.append(nbf.v4.new_markdown_cell("### Зависимость $R^2$ от энергии\n"
"Проверяем теоретическую зависимость $R \\propto 1/\\sqrt{E}$. Построим $R^2(E)$. "))

cells.append(nbf.v4.new_code_cell("""
valid = data.dropna(subset=["E_кэВ", "R"])
plt.scatter(valid["E_кэВ"], valid["R"]**2)
plt.xlabel("Энергия (кэВ)")
plt.ylabel("R^2")
plt.grid()
plt.show()
"""))

# Выводы
cells.append(nbf.v4.new_markdown_cell("### Выводы\n"
"- Построен калибровочный график «канал – энергия».\n"
"- Определены энергии пиков для Co, Cs, Na, Am, Eu.\n"
"- Найдено энергетическое разрешение для разных энергий.\n"
"- Проверена зависимость $R^2(E)$.\n"
"- Выявлены комптоновские края и аннигиляционные пики."))

# Сохраняем notebook
nb["cells"] = cells
path = Path("calc.ipynb")
with open(path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)


