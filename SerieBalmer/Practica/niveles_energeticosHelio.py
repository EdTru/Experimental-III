import csv
import os
from tabulate import tabulate
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt


os.chdir(os.path.dirname(os.path.realpath(__file__)))

terminos_espectroscopicos = {
	"S":1,
	"P":2,
	"D":3,
	"F":4,
	"G":5
}


datos_niveles = []
cabezas = ["e1","e2","Nivel espectroscópico","J","L","S","Energia"]


with open("niveles_energia.csv", "r", newline='', encoding='utf-8') as csvfile:
	reader = csv.reader(csvfile)
	for row in reader:
		e1 = row[0][2:4]
		e2 = row[0][5:7]

		nivel_Esp = row[1][2:4]

		J = row[2][2:3]
		L = terminos_espectroscopicos[nivel_Esp[1]]
		S = int((int(nivel_Esp[0])-1)/2)

		E_ev = np.float64(row[4][2:-1])

		datos_niveles.append([e1,e2,nivel_Esp,J,L,S,E_ev])

datos_inv = np.transpose(datos_niveles)

orb = datos_inv[0]+datos_inv[1]
nivel_Esp = datos_inv[2]
J = datos_inv[3]
L = datos_inv[4]
S = datos_inv[5]

En = np.float64(datos_inv[6])

x = [1]*len(En)
for i in range(len(En)):
	x[i] = int(J[i])+1

plt.scatter(x,En, s=900, marker="_", linewidth=2, zorder=3)
plt.yscale("log",base=2)

for xi, Eni, nom_orbital, H, mom_ang in zip(x,En,orb, nivel_Esp, J):
	nombre = str(nom_orbital)+"|"+str(H)+"|J="+str(mom_ang)
	plt.annotate(nombre, xy=(xi,Eni))

plt.xlabel("Momento angular J")
plt.ylabel("Energía ->>")
plt.title("Niveles de energía del Helio hasta n=5")

plt.show()
