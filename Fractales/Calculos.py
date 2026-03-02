import scipy.io
import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

papel_suave_2 = np.array([[1,14.6],
                        [2, 22.2],
                        [4, 35.8],
                        [8, 38.5],
                        [16, 54.8],
                        [32, 78.2],
                        [64, 119]])

print(papel_suave_2)

t_medido = np.transpose(papel_suave_2)[0]
y_medido = np.transpose(papel_suave_2)[1]

print(t_medido, y_medido)

log_t = np.copy(t_medido)
log_y = np.copy(y_medido)

for i in range(7):
    log_t[i] = np.log(t_medido[i])
    log_y[i] = np.log(y_medido[i])

print(log_t, log_y)

def test_function(x,a,b):
    return a*x+b

param, param_cov = curve_fit(test_function, log_t, log_y)

fit_f = param[0]* t_medido +param[1]

# Graficar la señal original y la reconstruida
plt.subplot(2, 1, 1)
plt.plot(t_medido, y_medido)
plt.title('Señal original en el dominio del tiempo')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')

plt.subplot(2, 1, 2)
plt.plot(log_t, fit_f)
plt.title('Señal original en el dominio del tiempo')
plt.xlabel('Tiempo [s]')
plt.ylabel('Amplitud')

plt.tight_layout()
plt.show()
