import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


pat = os.path.dirname(os.path.realpath(__file__))+"/PicoScope_2202/T180"
os.chdir(pat)

archivos = os.listdir(os.getcwd())

U_1 = []
I_A = []

with open(archivos[0]) as archivo:
	lectura = csv.reader(archivo, delimiter=';')
	lectura = list(lectura)

	lectura.pop(0)
	lectura.pop(0)
	lectura.pop(0)

	valor_U_1 = float(lectura[0][1].replace(",","."))*10
	valor_I_A = float(lectura[0][2].replace(",","."))*5


	U_1.append(valor_U_1)
	I_A.append(valor_I_A)


	for i in range(1,len(lectura)):
		valor_U_1 = float(lectura[i][1].replace(",","."))*10
		valor_I_A = float(lectura[i][2].replace(",","."))*5

		if valor_U_1<10:
			continue
		elif valor_U_1 < 55 and valor_I_A > 7:
			continue

		U_1.append(valor_U_1)
		I_A.append(valor_I_A)		


print(find_peaks(I_A))

# Tus datos (curva paramétrica)
A = U_1  # coordenada x
B = I_A  # coordenada y
N = len(A)
t = range(N)

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

fig, axes = plt.subplots(1, 2, figsize=(15, 7))

axes[0].scatter(A, B, s=5, label="Original")
axes[0].set_title("Curva original")

axes[1].scatter(A_rec, B_rec, s=5, color='orange', label="Filtrada (pasa-alto)")
axes[1].set_title("Reconstrucción")



plt.tight_layout()
plt.show()
