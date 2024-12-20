import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator, AutoMinorLocator

# Данные для предельной петли
B_limit = np.array([1.442043453, 1.249770993, 1.195433124, 1.136915418, 1.107656566, 1.086757385,
                    1.05958845, 1.036599352, 1.001070745, 0.9613623022, 0.9132941871, 0.8067083666, 
                    0.6081661521, 0.3218473794, 0.06896729559, -0.2194413951, -0.4054441014, 
                    -0.6186157423, -0.9049345149, -1.078397713, -1.387705584, -1.657305012, 
                    -1.400245092, -1.21006255, -1.147365009, -1.090937221, -1.061678369, 
                    -1.042869106, -1.01779009, -0.996890909, -0.9613623022, -0.9195639413, 
                    -0.8714958261, -0.7628200876, -0.5600980369, -0.2800490185, -0.02716893463, 
                    0.2633296741, 0.4514222984, 0.6666838574, 0.9425530398, 1.118106156, 
                    1.425324109, 1.690743701])

H_limit = np.array([5.24399622, 3.256469291, 2.714467132, 2.217975329, 1.97699883, 1.804817055, 
                    1.58194443, 1.369544201, 1.036989947, 0.6115767421, 0, -0.6112425167, 
                    -1.036321496, -1.369544201, -1.585063867, -1.803925787, -2.018006881, 
                    -2.213797512, -2.702379314, -3.250898868, -5.234526501, -9.606194478, 
                    -5.240653966, -3.254241121, -2.712796005, -2.215691456, -1.975940449, 
                    -1.804705646, -1.581443092, -1.369767018, -1.036655722, -0.6116324463, 
                    0, 0.6112425167, 1.036265792, 1.369544201, 1.57943774, 1.803925787, 
                    1.974937773, 2.213518991, 2.702936356, 3.25145591, 5.235083543, 9.617335324])

sigma_B_limit = np.array([0, 0.02040535596, 0.02122824692, 0.02214040218, 0.02238093158, 0.0225145407, 
                          0.02272198223, 0.0228761292, 0.02320752092, 0.02360918149, 0.02417521051, 
                          0.0267048862, 0.03401551107, 0.04559658892, 0.05290087247, 0.06110637549, 
                          0.06421623901, 0.06808296489, 0.07454719335, 0.07678792307, 0.08349968861, 
                          0.0882597388, 0.02726531007, 0.03392339576, 0.03458391631, 0.03511278444, 
                          0.03526494464, 0.0353367023, 0.03545193699, 0.03553643596, 0.03575066462, 
                          0.03603925612, 0.0364125711, 0.03820522449, 0.04384500206, 0.05295741916, 
                          0.0593627967, 0.06688063598, 0.06979640636, 0.07343814698, 0.07905164681, 
                          0.08121858051, 0.08750883669, 0.09192528861])

sigma_H_limit = np.array([0.02636749537, 0.01651884406, 0.01385516865, 0.01143428035, 0.01026988376, 
                          0.009444126119, 0.008385768159, 0.007392474963, 0.005885669621, 0.004136188573, 
                          0, 0.004134953262, 0.005882725493, 0.007392474963, 0.008400481515, 
                          0.009439868074, 0.007617479306, 0.01141402158, 0.01379596869, 0.01649139137, 
                          0.02632041214, 0.04811165879, 0.02635087765, 0.01650786282, 0.01384698369, 
                          0.01142320528, 0.01026479029, 0.009443593853, 0.008383403811, 0.007393506962, 
                          0.005884197504, 0.004136394488, 0, 0.004134953262, 0.005882480168, 
                          0.007392474963, 0.008373947245, 0.009439868074, 0.01025996507, 0.01141267108, 
                          0.01379869656, 0.01649413658, 0.02632318172, 0.04816726971])

# Данные для начальной кривой
B_initial = np.array([0, 0.09195639413, 0.2278010673, 0.3929045931, 0.5057601677, 0.6457846769,
                      0.7419209071, 0.8714958261, 1.095117057, 1.266490337, 1.636405832])

H_initial = np.array([0, 0.6102955448, 1.035207412, 1.379236737, 1.578323655, 1.795624687, 1.973210942, 
                      2.212126385, 2.701766567, 3.252012952, 9.23675467])

sigma_B_initial = np.array([0, 0.01509863393, 0.02364263321, 0.02682309459, 0.03099982427, 0.03286162256, 
                            0.03589259015, 0.04339420599, 0.04731431141, 0.06188249943, 0.07256202108])

sigma_H_initial = np.array([0.00413145488, 0.005877819558, 0.007437388825, 0.008368694171, 0.00705148824, 
                            0.01025165541, 0.01140591871, 0.01379296805, 0.0164968818, 0.02633149046, 
                            0.04818951414])

# Построение графика с предельной петлей и начальной кривой с погрешностями
plt.figure(figsize=(8, 6))

# Предельная петля
plt.errorbar(H_limit, B_limit, yerr=sigma_B_limit, xerr=sigma_H_limit, fmt='o', color='red', markersize=4, zorder=5)
plt.plot(H_limit, B_limit, color='blue', linestyle='-')

# Начальная кривая
plt.errorbar(H_initial, B_initial, yerr=sigma_B_initial, xerr=sigma_H_initial, fmt='o', color='green', markersize=4, zorder=5)
plt.plot(H_initial, B_initial, color='orange', linestyle='-')

# Calculate slopes and find the maximum slope
slopes = []
for i in range(len(H_initial) - 1):
    slope = (B_initial[i + 1] - B_initial[i]) / (H_initial[i + 1] - H_initial[i])
    slopes.append(slope)

max_slope_index = np.argmax(slopes)
max_slope = slopes[max_slope_index]
x1, x2 = H_initial[max_slope_index], H_initial[max_slope_index + 1]
y1, y2 = B_initial[max_slope_index], B_initial[max_slope_index + 1]

# Print the maximum slope value
print(f'Maximum slope: {max_slope}')

# Extend the line across the graph
# Define the extension range (adjust as necessary)
extension_range = np.linspace(min(H_initial) - 1, max(H_initial) - 6, 100)
# Calculate the corresponding B values using the maximum slope
y_ext = y1 + max_slope * (extension_range - x1)

# Plot initial curve
plt.errorbar(H_initial, B_initial, fmt='o', color='green', markersize=4)
plt.plot(H_initial, B_initial, color='orange', linestyle='-')

# Plot the line of maximum slope extended
plt.plot(extension_range, y_ext, color='purple', linestyle='--', linewidth=2, label=f'Slope: {max_slope:.2f}')

# Определение B_s, B_r, H_c и M_s
B_s = np.max(B_initial)  # Индукция насыщения
B_r = B_initial[np.where(H_initial == 0)[0][0]]  # Остаточная индукция

# Находим коэрцитивное поле H_c
H_c_index = np.where(np.diff(np.sign(B_limit)))[0]  # Индексы, где B меняет знак
H_c = H_limit[H_c_index[0]] if len(H_c_index) > 0 else 0  # Коэрцитивное поле

# Плотная линия и точки
plt.plot(H_initial, B_initial, color='blue', linestyle='-', label='Кривая гистерезиса')
plt.axhline(y=B_s, color='orange', linestyle='--', label=f'$B_s = {B_s:.2f}$ Тл')
plt.axvline(x=H_c, color='red', linestyle='--', label=f'$H_c = {H_c:.2f}$ кА/м')

# Добавление аннотаций
plt.text(H_c - 4, 0.05, f'$H_c = {H_c:.2f}$', color='red', fontsize=10)
plt.text(0.5, B_s + 0.1, f'$B_s = {B_s:.2f}$', color='orange', fontsize=10)


# Настройка основных и вспомогательных осей
ax = plt.gca()
ax.xaxis.set_major_locator(MultipleLocator(2))
ax.xaxis.set_minor_locator(AutoMinorLocator(4))
ax.yaxis.set_major_locator(MultipleLocator(0.5))
ax.yaxis.set_minor_locator(AutoMinorLocator(5))

# Добавление осей
plt.axhline(0, color='gray', linestyle='--', linewidth=1)  # minor axis (horizontal)
plt.axvline(0, color='gray', linestyle='--', linewidth=1)  # minor axis (vertical)

# Добавление заголовков и решетки
plt.title('График предельной петли и начальной кривой')
plt.xlabel('H, кА/м')
plt.ylabel('B, Тл')
plt.grid(True, which='both', linestyle=':', linewidth=0.5)
plt.legend()


# Показать график
plt.show()

