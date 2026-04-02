import numpy as np
import tabulate as tb

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (la mitad de la distancia entre m=-1 y m=1)]
#D en cm X_min mm
rendija_1_1 = np.array([[100, 9, r"$\pm 0.02$"],
					    [90, 8.12, r"$\pm 0.02$"],
						[80, 6.86, r"$\pm 0.02$"],
						[70, 6.35, r"$\pm 0.02$"],
						[60, 5.05, r"$\pm 0.02$"]])

rendija_1_2 = np.array([[100, 10.66, r"$\pm 0.02$"],
					    [90, 9.57, r"$\pm 0.02$"],
						[80, 8.12, r"$\pm 0.02$"],
						[70, 7.78, r"$\pm 0.02$"],
						[60, 5.87, r"$\pm 0.02$"]])

rendija_1_3 = np.array([[100, 13.48, r"$\pm 0.02$"],
						[90, 12.21, r"$\pm 0.02$"],
						[80, 10.83, r"$\pm 0.02$"],
						[70, 9.63, r"$\pm 0.02$"],
						[60, 7.89, r"$\pm 0.02$"]])


rendija_1_4 = np.array([[100, 17.8, r"$\pm 0.02$"],
						[90, 15.36, r"$\pm 0.02$"],
						[80, 14.28, r"$\pm 0.02$"],
						[70, 12.12, r"$\pm 0.02$"],
						[60, 10.93, r"$\pm 0.02$"]]
)

rendija_1_5 = np.array([[100, 24.29, r"$\pm 0.02$"],
						[90, 21.32, r"$\pm 0.02$"],
						[80, 19.82, r"$\pm 0.02$"],
						[70, 17.78, r"$\pm 0.02$"],
						[60, 13.83, r"$\pm 0.02$"]])


rendija_1_6 = np.array([[100,62.60, r"$\pm 0.02$"],
						[90, 56.25, r"$\pm 0.02$"],
						[80, 50.34, r"$\pm 0.02$"],
						[70, 44.17, r"$\pm 0.02$"],
						[60, 37.59, r"$\pm 0.02$"]])

distancias = np.transpose(rendija_1_1)[0]

r1 = np.transpose(rendija_1_1)[1]
r2 = np.transpose(rendija_1_2)[1]
r3 = np.transpose(rendija_1_3)[1]
r4 = np.transpose(rendija_1_4)[1]
r5 = np.transpose(rendija_1_5)[1]
r6 = np.transpose(rendija_1_6)[1]


indices_tabla = ["D (cm)", "Xmin (mm)", r"$\Delta D$ (mm)"]

tabla_r1 = tb.tabulate(rendija_1_1, headers=indices_tabla, tablefmt="latex_raw")
tabla_r2 = tb.tabulate(rendija_1_2, headers=indices_tabla, tablefmt="latex_raw")
tabla_r3 = tb.tabulate(rendija_1_3, headers=indices_tabla, tablefmt="latex_raw")
tabla_r4 = tb.tabulate(rendija_1_4, headers=indices_tabla, tablefmt="latex_raw")
tabla_r5 = tb.tabulate(rendija_1_5, headers=indices_tabla, tablefmt="latex_raw")
tabla_r6 = tb.tabulate(rendija_1_6, headers=indices_tabla, tablefmt="latex_raw")

tablas = [tabla_r1, tabla_r2, tabla_r3, tabla_r4, tabla_r5, tabla_r6]

for i,j  in enumerate(tablas):
	print(j)
