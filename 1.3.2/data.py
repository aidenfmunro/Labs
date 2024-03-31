import numpy as np

def mnk(V):
    N = len(V)

    M = np.sum(V) / N

    D = 0

    for R in V:
        D += (R - M) ** 2

    D = np.sqrt(D / N / (N - 1))

    return M, D

a = [20.5, 28.0, 39.9, 53.7, 69.7, 87.2, 106.9, 129.5, 152.5]

b = [3.05900, 3.64400, 4.57900, 5.61700, 6.88000, 8.25400, 9.77100, 11.52600, 13.38800]

A = [0] * 9

for i in range (0, 8):
    A[i] = b[i]/a[i]

res = mnk(A)


print('среднее арифм. = %f, ср.кв.откл. = %f' % res)