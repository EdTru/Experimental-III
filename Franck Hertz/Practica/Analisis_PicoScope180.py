import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tabulate import tabulate
from scipy.constants import constants

pat = os.path.dirname(os.path.realpath(__file__))+"/PicoScope_2202/T180"
os.chdir(pat)

archivos = os.listdir(os.getcwd())

datos=[]

with open(archivos[0]) as archivo:
	lectura = csv.reader(archivo, delimiter=';')
	lectura = list(lectura)

	lectura.pop(0)
	lectura.pop(0)
	lectura.pop(0)

	valor_U_1 = float(lectura[0][1].replace(",","."))*10
	valor_I_A = float(lectura[0][2].replace(",","."))*5

	datos.append([valor_U_1,valor_I_A])

	for i in range(1,len(lectura)):
		valor_U_1 = float(lectura[i][1].replace(",","."))*10
		valor_I_A = float(lectura[i][2].replace(",","."))*5

		if valor_U_1<10:
			continue
		elif valor_U_1 < 55 and valor_I_A > 7:
			continue

		datos.append([valor_U_1,valor_I_A])	

datos = np.unique(datos,axis=0)
datos= np.transpose(datos)
U_1 = datos[0]
I_A = datos[1]

I_Ainv = [elemento * -1 for elemento in I_A]


picos_I = find_peaks(I_Ainv,distance=20)[0]
picos_U = []

for pico in picos_I:
	if U_1[pico] > 30:
		picos_U.append(U_1[int(pico)])

plt.scatter(U_1,I_A)

for i in picos_U:
	plt.vlines(i,ymin=-1,ymax=10,colors=str(i.round(1)/100),linestyles="--",label=str(i.round(3)))

cabezas=["n salto","energía (J)", "energía (eV)", "Error (J)","Error (eV)"]

plt.title("Curva de Frank Hertz a T=180º")
plt.ylabel("Intensidad I_A (nA)")
plt.xlabel("Voltaje U_1 (V)")

plt.legend()

plt.show()