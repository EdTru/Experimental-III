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

def tomar_csv_dar_minimos(archivocsv):

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
			elif valor_U_1 < 55 and valor_I_A > 7:
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

	dpicos_U=[]
	for i in range(1,len(picos_U)):
		dpicos_U.append(picos_U[i]-picos_U[i-1])
		
	return dpicos_U

lista_dpicos = []
for csvs in archivos:
	dpicos_U = tomar_csv_dar_minimos(csvs)
	lista_dpicos += dpicos_U


N = len(lista_dpicos)
media = np.mean(lista_dpicos)
desviacion = np.std(lista_dpicos)

error_media = 0.1/np.sqrt(N)

cabeza = ["Delta picos media","Delta picos variacion"]
pies = [[media,desviacion]]

tablax = tabulate(pies,cabeza,tablefmt="latex")

print(tablax)
print(error_media)