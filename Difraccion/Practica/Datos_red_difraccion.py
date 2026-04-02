import numpy as np
import tabulate as tb

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (distancia entre m=-1 y m=1)]
#D en cm X_min cm
red600 = np.array([[35, 28, r"$\pm 0.5$", r"$\pm 0.02$"],
					[30, 25.2, r"$\pm 0.5$", r"$\pm 0.02$"],
					[25, 19.6, r"$\pm 0.5$", r"$\pm 0.02$"],
					[20, 15.9, r"$\pm 0.5$", r"$\pm 0.02$"],
					[15, 12, r"$\pm 0.5$", r"$\pm 0.02$"]])

red300 = np.array([[70, 28.4, r"$\pm 0.5$", r"$\pm 0.02$"],
					[60, 23.8, r"$\pm 0.5$", r"$\pm 0.02$"],
					[50, 20.2, r"$\pm 0.5$", r"$\pm 0.02$"],
					[40, 15, r"$\pm 0.5$", r"$\pm 0.02$"],
					[30, 11.9, r"$\pm 0.5$", r"$\pm 0.02$"]])

red100 = np.array([[70, 9.1, r"$\pm 0.5$", r"$\pm 0.02$"],
					[60, 8.4, r"$\pm 0.5$", r"$\pm 0.02$"],
					[50, 6.1, r"$\pm 0.5$", r"$\pm 0.02$"],
					[40, 5, r"$\pm 0.5$", r"$\pm 0.02$"],
					[30, 3.9, r"$\pm 0.5$", r"$\pm 0.02$"]])

distancias_600 = np.transpose(red600)[0]
distancias_300 = np.transpose(red300)[0]
distancias_100 = np.transpose(red100)[0]

r_600 = np.transpose(red600)[1]
r_300 = np.transpose(red300)[1]
r_100 = np.transpose(red100)[1]


indices_tabla = ["D (cm)", "X_{max} (cm)", r"$\Delta D$ (cm)", r"$\Delta X_{max}$ (cm)"]


tabla_red600 = tb.tabulate(red600, headers=indices_tabla, tablefmt="latex_raw")
tabla_red300 = tb.tabulate(red300, headers=indices_tabla, tablefmt="latex_raw")
tabla_red100 = tb.tabulate(red100, headers=indices_tabla, tablefmt="latex_raw")

tablas = [tabla_red600, tabla_red300, tabla_red100]

for i,j  in enumerate(tablas):
	print(j)
	print("\n")

"""
for i in red300:
	print(((i[1]/2)/((640*10**(-9))*i[0]))*10**(-3))

"""

