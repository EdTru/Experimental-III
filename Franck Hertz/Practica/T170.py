import os
import csv
import numpy as np
import matplotlib.pyplot as plt


pat = os.path.dirname(os.path.realpath(__file__))+"/T170"
os.chdir(pat)

archivos = os.listdir(os.getcwd())

datos = []

with open(archivos[2]) as archivo:
	lectura = csv.reader(archivo, delimiter=';')
	lectura = list(lectura)

	lectura.pop(0)
	lectura.pop(0)
	lectura.pop(0)

	datos.append([lectura[0][1].replace(",","."),lectura[0][2].replace(",",".")])


	for i in range(1,len(lectura)):
		valor_x = float(lectura[i][1].replace(",","."))
		valor_y = float(lectura[i][2].replace(",","."))

		if 0.5 < valor_x and valor_x < 5.7 and 6 < valor_y: 
			continue
		elif valor_x < 1:
			continue


		datos.append([float(lectura[i][1].replace(",",".")),float(lectura[i][2].replace(",","."))])

		

datos = np.transpose(np.float64(datos))



import numpy as np
import matplotlib.pyplot as plt
import scipy.io

# Tus datos (curva paramétrica)
A = datos[0]  # coordenada x
B = datos[1]  # coordenada y
N = len(A)

# --- FFT de cada coordenada por separado ---
fft_A = np.fft.fft(A)
fft_B = np.fft.fft(B)

# --- Filtro pasa-ALTO: eliminar frecuencias bajas (< 20% de N/2) ---
fft_A_filt = fft_A.copy()
fft_B_filt = fft_B.copy()

corte = int(0.20 * (N // 2))   # índice de corte = 20% de las frecuencias

# Poner a cero las frecuencias bajas (simétricamente)

for i in range(len(fft_A)):

	if np.abs(fft_A[i]) < 5:
		fft_A_filt[i] = 0 
	if np.abs(fft_B[i]) < 5:
		fft_B_filt[i] = 0 


A_rec = np.fft.ifft(fft_A_filt).real
B_rec = np.fft.ifft(fft_B_filt).real

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

axes[0].scatter(A, B, s=5, label="Original")
axes[0].set_title("Curva original")
axes[0].set_aspect("equal")

axes[1].scatter(A_rec, B_rec, s=5, color='orange', label="Filtrada (pasa-alto)")
axes[1].set_title("Reconstrucción")
axes[1].set_aspect("equal")

plt.tight_layout()
plt.show()
