import numpy as np
import matplotlib.pyplot as plt 

#hecho manualmente, no con arduino vfuente = 4.8V
datos_manual = np.array([
    ["0000", 0],
    ["0001", 0.31],
    ["0010", 0.63],
    ["0011", 0.95],
    ["0100", 1.26],
    ["0101", 1.58],
    ["0110", 1.9],
    ["0111", 2.22],
    ["1000", 2.54],
    ["1001", 2.85],
    ["1010", 3.17],
    ["1011", 3.49],
    ["1100", 3.88],
    ["1101", 4.12],
    ["1110", 4.44],
    ["1111", 4.76]
])


datos_arduino = np.array([
    ["0000", 0],
    ["0001", 0.29],
    ["0010", 0.58],
    ["0011", 0.87],
    ["0100", 1.16],
    ["0101", 1.46],
    ["0110", 1.75],
    ["0111", 2.05],
    ["1000", 2.34],
    ["1001", 2.63],
    ["1010", 2.92],
    ["1011", 3.22],
    ["1100", 3.51],
    ["1101", 3.80],
    ["1110", 4.10],
    ["1111", 4.39]
])



binario_1 = []
voltaje_1 = []

binario_2 = []
voltaje_2 = []

for i,j  in enumerate(datos_arduino):
    binario_1.append(i)
    voltaje_1.append(float(j[1]))

for i,j  in enumerate(datos_manual):
    binario_2.append(i)
    voltaje_2.append(float(j[1]))


plt.plot(binario_1, voltaje_1, marker='o')
plt.plot(binario_2, voltaje_2, marker='o')
plt.legend(['Arduino', 'Manual'])
plt.title('Voltaje vs Binario')
plt.xlabel('Binario')
plt.ylabel('Voltaje')
plt.show()
