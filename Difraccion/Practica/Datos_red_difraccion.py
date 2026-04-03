import numpy as np
import tabulate as tb

#Tablas de la forma [D (distancia rendija-caja), d(m=1 m=-1) (distancia entre m=-1 y m=1)]
#D en cm X_min cm
red600 = np.array([[35, 28, r"$\pm 0.5$", r"$\pm 0.01$"],
					[30, 25.2, r"$\pm 0.5$", r"$\pm 0.01$"],
					[25, 19.6, r"$\pm 0.5$", r"$\pm 0.01$"],
					[20, 15.9, r"$\pm 0.5$", r"$\pm 0.01$"],
					[15, 12, r"$\pm 0.5$", r"$\pm 0.01$"]])

red300 = np.array([[70, 28.4, r"$\pm 0.5$", r"$\pm 0.01$"],
					[60, 23.8, r"$\pm 0.5$", r"$\pm 0.01$"],
					[50, 20.2, r"$\pm 0.5$", r"$\pm 0.01$"],
					[40, 15, r"$\pm 0.5$", r"$\pm 0.01$"],
					[30, 11.9, r"$\pm 0.5$", r"$\pm 0.01$"]])

red100 = np.array([[70, 9.1, r"$\pm 0.5$", r"$\pm 0.01$"],
					[60, 8.4, r"$\pm 0.5$", r"$\pm 0.01$"],
					[50, 6.1, r"$\pm 0.5$", r"$\pm 0.01$"],
					[40, 5, r"$\pm 0.5$", r"$\pm 0.01$"],
					[30, 3.9, r"$\pm 0.5$", r"$\pm 0.01$"]])

distancias_600 = np.transpose(red600)[0]
distancias_300 = np.transpose(red300)[0]
distancias_100 = np.transpose(red100)[0]

r_600 = np.transpose(red600)[1]
r_300 = np.transpose(red300)[1]
r_100 = np.transpose(red100)[1]

"""

indices_tabla = ["D (cm)", "X_{max} (cm)", r"$\Delta D$ (cm)", r"$\Delta X_{max}$ (cm)"]


tabla_red600 = tb.tabulate(red600, headers=indices_tabla, tablefmt="latex_raw")
tabla_red300 = tb.tabulate(red300, headers=indices_tabla, tablefmt="latex_raw")
tabla_red100 = tb.tabulate(red100, headers=indices_tabla, tablefmt="latex_raw")

tablas = [tabla_red600, tabla_red300, tabla_red100]

for i,j  in enumerate(tablas):
	print(j)
	print("\n")
"""

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

print("Media 100:", round(sum(resultados_100)/len(resultados_100), 2))
print("Media 300:", round(sum(resultados_300)/len(resultados_300), 2))
print("Media 600:", round(sum(resultados_600)/len(resultados_600), 2))
print("Media_errores_100:", round(sum(errores_100)/len(errores_100), 2))
print("Media_errores_300:", round(sum(errores_300)/len(errores_300), 2))
print("Media_errores_600:", round(sum(errores_600)/len(errores_600), 1))