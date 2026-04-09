import csv
import os
from tabulate import tabulate
import scipy.constants as const
import numpy as np
import matplotlib.pyplot as plt
from adjustText import adjust_text   # pip install adjustText



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
		if int(e2[0])>3:
			continue

		datos_niveles.append([e1,e2,nivel_Esp,J,L,S,E_ev])

datos_inv = np.transpose(datos_niveles)

orb = datos_inv[0]+datos_inv[1]
nivel_Esp = datos_inv[2]
J = datos_inv[3]
L = datos_inv[4]
S = datos_inv[5]

En = np.float64(datos_inv[6])

x = [int(j) + 1 for j in J]

fig, ax = plt.subplots(figsize=(10, 7))

ax.scatter(x, En, s=3000, marker="_", linewidth=5, zorder=6)
ax.set_yscale("log", base=2)

# 1. Guardar todos los textos en una lista para adjust_text
texts = []
for xi, Eni, nom_orbital, H, mom_ang in zip(x, En, orb, nivel_Esp, J):
	nombre = f"{nom_orbital}|{H}|J={mom_ang}"
	t = ax.text(
		xi, Eni, nombre,
		fontsize=10,
		va='bottom',
		bbox=dict(           # 2. Fondo blanco para que no se "pisen"
			boxstyle='round,pad=0.15',
			fc='white',
			ec='none',
			alpha=0.75
		)
	)
	texts.append(t)

# 3. Recolocar automáticamente para evitar solapamientos
adjust_text(
	texts,
	ax=ax,
	expand_text=(1.1, 1.4),      # expansión horizontal / vertical
	arrowprops=dict(             # línea guía si el texto se mueve mucho
		arrowstyle='-',
		color='gray',
		lw=0.5
	)
)

ax.set_xlabel("Momento angular J")
ax.set_ylabel("Energía ->>")
ax.set_title("Niveles de energía del Helio hasta n=3")
ax.grid(True, axis='y', alpha=0.2)

plt.tight_layout()
plt.savefig("EspectroHelioTeo.svg")
plt.show()