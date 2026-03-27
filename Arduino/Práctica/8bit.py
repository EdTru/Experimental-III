import numpy as np
import matplotlib.pyplot as plt 

datos_manual = np.array([
    ["00000000", 0],
    ["11111111", 5.08],
])


binario_1 = []
voltaje_1 = []

for i,j  in enumerate(datos_manual):
    binario_1.append(i)
    voltaje_1.append(float(j[1]))



plt.plot(binario_1, voltaje_1, marker='o')
plt.legend(['Manual'])
plt.title('Voltaje vs Binario')
plt.xlabel('Binario')
plt.ylabel('Voltaje')
plt.show()