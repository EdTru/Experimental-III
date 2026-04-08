import numpy as np
import tabulate as tb
import matplotlib.pyplot as plt
from scipy.stats import linregress

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (la mitad de la distancia entre m=-1 y m=1)]
#D en cm X_min mm
rendija_1_1 = np.array([[1000, 9/2, r"$\pm 0.02$"],
					    [900, 8.12/2, r"$\pm 0.02$"],
						[800, 6.86/2, r"$\pm 0.02$"],
						[700, 6.35/2, r"$\pm 0.02$"],
						[600, 5.05/2, r"$\pm 0.02$"]])

rendija_1_2 = np.array([[1000, 10.66/2, r"$\pm 0.02$"],
					    [900, 9.57/2, r"$\pm 0.02$"],
						[800, 8.12/2, r"$\pm 0.02$"],
						[700, 7.78/2, r"$\pm 0.02$"],
						[600, 5.87/2, r"$\pm 0.02$"]])

rendija_1_3 = np.array([[1000, 13.48/2, r"$\pm 0.02$"],
						[900, 12.21/2, r"$\pm 0.02$"],
						[800, 10.83/2, r"$\pm 0.02$"],
						[700, 9.63/2, r"$\pm 0.02$"],
						[600, 7.89/2, r"$\pm 0.02$"]])


rendija_1_4 = np.array([[1000, 17.8/2, r"$\pm 0.02$"],
						[900, 15.36/2, r"$\pm 0.02$"],
						[800, 14.28/2, r"$\pm 0.02$"],
						[700, 12.12/2, r"$\pm 0.02$"],
						[600, 10.93/2, r"$\pm 0.02$"]]
)

rendija_1_5 = np.array([[1000, 24.29/2, r"$\pm 0.02$"],
						[900, 21.32/2, r"$\pm 0.02$"],
						[800, 19.82/2, r"$\pm 0.02$"],
						[700, 17.78/2, r"$\pm 0.02$"],
						[600, 13.83/2, r"$\pm 0.02$"]])


rendija_1_6 = np.array([[1000,62.60/2, r"$\pm 0.02$"],
						[900, 56.25/2, r"$\pm 0.02$"],
						[800, 50.34/2, r"$\pm 0.02$"],
						[700, 44.17/2, r"$\pm 0.02$"],
						[600, 37.59/2, r"$\pm 0.02$"]])

distancias = np.transpose(rendija_1_1)[0].astype(float)

r1 = np.transpose(rendija_1_1)[1].astype(float)
r2 = np.transpose(rendija_1_2)[1].astype(float)
r3 = np.transpose(rendija_1_3)[1].astype(float)
r4 = np.transpose(rendija_1_4)[1].astype(float)
r5 = np.transpose(rendija_1_5)[1].astype(float)
r6 = np.transpose(rendija_1_6)[1].astype(float)


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


#ahora representamos gráficamente los resultados obetenidos

pendientes = []
for i in range(1,7):
	r = eval("r"+str(i))
	m, b, r_value, p_value, std_err = linregress(distancias, r)
	pendientes.append(m)

m_media = np.mean(pendientes)
print(round(m_media,3))
"""
plt.scatter(distancias, r6, label="Rendija 6", marker="o")
plt.plot(distancias, m*distancias + b, label="Ajuste lineal", color="red")
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Xmin (mm)")
plt.title("Xmin vs Distancia rendija-caja para la toma 6, m = {:.4f}".format(m))
plt.legend()
plt.grid()
plt.show()
"""

