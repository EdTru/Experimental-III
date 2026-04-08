import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tabulate import tabulate
from scipy.constants import constants

pat = os.path.dirname(os.path.realpath(__file__))+"/PicoScope_2202/T170"
os.chdir(pat)

archivos = os.listdir(os.getcwd())

datos=[]

with open(archivos[1]) as archivo:
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
		elif valor_U_1 < 59 and valor_I_A > 30:
			continue

		datos.append([valor_U_1,valor_I_A])	

datos = np.unique(datos,axis=0)
datos= np.transpose(datos)
U_1 = datos[0]
I_A = datos[1]

I_Ainv = [elemento * -1 for elemento in I_A]

def encontrar_minimo(lista,distancia_busqueda):
	minimos = [0]

	for i in range(distancia_busqueda, len(lista)):
		actual = lista[i]
		lista_buscar_min_local = lista[i-distancia_busqueda:i+distancia_busqueda]
		if actual == min(lista_buscar_min_local):
			if lista[i]-lista[minimos[-1]] > 0.5: 
				minimos.append(i)
	
	minimos.pop(0)
	return minimos


picos_I = encontrar_minimo(I_A,8)
picos_U = []

for pico in picos_I:
	if U_1[pico] < 30:
		continue
	picos_U.append(U_1[int(pico)])
	

plt.scatter(U_1,I_A)

for i in picos_U:
	plt.vlines(i,ymin=-1,ymax=30,colors=str(i.round(1)/100),linestyles="--",label=str(i.round(3)))


cabezas = ["n salto ",   "Delta U",    "Delta U",    "Error (J)",    "Error (eV)"]
pies = []

for i in range(1,len(picos_U)):
	pies.append([i,picos_U[i]-picos_U[i-1],0,0,0])

tabla_DeltaU = tabulate(pies,cabezas)

print(tabla_DeltaU)
plt.title("Curva de Frank Hertz a T=170º")
plt.ylabel("Intensidad I_A (nA)")
plt.xlabel("Voltaje U_1 (V)")

plt.legend()
plt.savefig("PicoScopeT170.svg")
plt.show()