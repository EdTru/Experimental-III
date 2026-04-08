import numpy as np
import tabulate as tb
import matplotlib.pyplot as plt
from scipy.stats import linregress

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (distancia entre m=-1 y m=1)]
#D en mm X_min mm
red600 = np.array([[350, 280/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[300, 252/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[250, 196/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[200, 159/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[150, 120/2, r"$\pm 0.5$", r"$\pm 0.5$"]])

red300 = np.array([[700, 284/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[600, 238/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[500, 202/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[400, 150/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[300, 119/2, r"$\pm 0.5$", r"$\pm 0.5$"]])

red100 = np.array([[700, 91/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[600, 84/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[500, 61/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[400, 50/2, r"$\pm 0.5$", r"$\pm 0.5$"],
					[300, 39/2, r"$\pm 0.5$", r"$\pm 0.5$"]])

distancias_600 = np.transpose(red600)[0].astype(float)
distancias_300 = np.transpose(red300)[0].astype(float)
distancias_100 = np.transpose(red100)[0].astype(float)


r_600 = np.transpose(red600)[1].astype(float)
r_300 = np.transpose(red300)[1].astype(float) 
r_100 = np.transpose(red100)[1].astype(float) 

distancias_arcoiris_600 = [round(float(i), 2) * 10**(-3) for i in distancias_600] #Convertimos a metros para los calculos posteriores
xmax_600 = [round(float(i), 2) * 10**(-3) for i in r_600] #Convertimos a metros para los calculos posteriores

print(distancias_arcoiris_600)
print(xmax_600)

"""
indices_tabla = ["D (mm)", r"$X_{max} (mm)$", r"$\Delta D$ (cm)", r"$\Delta X_{max}$ (cm)"]


tabla_red600 = tb.tabulate(red600, headers=indices_tabla, tablefmt="latex_raw")
tabla_red300 = tb.tabulate(red300, headers=indices_tabla, tablefmt="latex_raw")
tabla_red100 = tb.tabulate(red100, headers=indices_tabla, tablefmt="latex_raw")

tablas = [tabla_red600, tabla_red300, tabla_red100]

for i,j  in enumerate(tablas):
	print(j)
	print("\n")


resultados_600 = []
resultados_300 = []
resultados_100 = []

errores_600 = []
errores_300 = []
errores_100 = []

for i in red100:
	resultados_100.append(((float(i[1])/2)/((640*10**(-9))*float(i[0])))*10**(-3))

	errores_100.append(1/(float(i[0]*10) * 640*10**(-6)) * 0.02 + (float(i[1])*10/2)/((float(i[0])*10)**2 * 640*10**(-6)) * 0.5)

for i in red300:
	resultados_300.append(((float(i[1])/2)/((640*10**(-9))*float(i[0])))*10**(-3))

	errores_300.append(1/(float(i[0]*10) * 640*10**(-6)) * 0.02 + (float(i[1])*10/2)/((float(i[0])*10)**2 * 640*10**(-6)) * 0.5)

for i in red600:
	resultados_600.append(((float(i[1])/2)/((640*10**(-9))*float(i[0])))*10**(-3))

	errores_600.append(1/(float(i[0]*10) * 640*10**(-6)) * 0.02 + (float(i[1])*10/2)/((float(i[0])*10)**2 * 640*10**(-6)) * 0.5)

error_medio_600 = np.mean(errores_600)
error_medio_300 = np.mean(errores_300)
error_medio_100 = np.mean(errores_100)


m, b, r_value, p_value, std_err = linregress(distancias_600, r_600)
plt.scatter(distancias_600, r_600, label="Red de 600 l/mm", marker="o", s=15, zorder=3)
plt.plot(distancias_600, m*distancias_600 + b, label="Ajuste lineal", color="red")
plt.errorbar(distancias_600, r_600, yerr=0.5, xerr=0.5, fmt='none', ecolor='black', elinewidth=1.2, capsize=5, zorder=2)
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Xmax (mm)")
plt.title(f"Xmax vs Distancia rendija-caja para la red de 600 l/mm, m = {round(m,3)} ± {round(std_err,3)}")
plt.legend()
plt.grid()
plt.show()


m, b, r_value, p_value, std_err = linregress(distancias_300, r_300)
plt.scatter(distancias_300, r_300, label="Red de 200 l/mm", marker="o", s=15, zorder=3)
plt.plot(distancias_300, m*distancias_300 + b, label="Ajuste lineal", color="red")
plt.errorbar(distancias_300, r_300, yerr=0.5, xerr=0.5, fmt='none', ecolor='black', elinewidth=1.2, capsize=5, zorder=2)
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Xmax (mm)")
plt.title(f"Xmax vs Distancia rendija-caja para la red de 300 l/mm, m = {round(m,4)} ± {round(std_err,4)}")
plt.legend()
plt.grid()
plt.show()


m, b, r_value, p_value, std_err = linregress(distancias_100, r_100)
plt.scatter(distancias_100, r_100, label="Red de 100 l/mm", marker="o", s=15, zorder=3)
plt.plot(distancias_100, m*distancias_100 + b, label="Ajuste lineal", color="red")
plt.errorbar(distancias_100, r_100, yerr=0.5, xerr=0.5, fmt='none', ecolor='black', elinewidth=1.2, capsize=5, zorder=2)
plt.xlabel("Distancia rendija-caja (mm)")
plt.ylabel("Xmax (mm)")
plt.title(f"Xmax vs Distancia rendija-caja para la red de 100 l/mm, m = {round(m,4)} ± {round(std_err,4)}")
plt.legend()
plt.grid()
plt.show()
"""