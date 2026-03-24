import os
import csv
import numpy as np
import matplotlib.pyplot as plt

pat = str(os.getcwd())+"/T170"
os.chdir(pat)

archivos = os.listdir(os.getcwd())

datos = []

with open(archivos[0]) as archivo:
	lectura = csv.reader(archivo, delimiter=';')
	lectura = list(lectura)

	lectura.pop(0)
	lectura.pop(0)
	lectura.pop(0)

	datos.append([lectura[0][1],lectura[0][2]])

	for i in range(1,len(lectura)):
		if lectura[i][1] == lectura[i-1][1] and lectura[i][2] == lectura[i-1][2]:
			continue

		datos.append([float(lectura[i][1].replace(",",".")),float(lectura[i][2].replace(",","."))])


print(datos[0])
np.fft.fft(datos[1])