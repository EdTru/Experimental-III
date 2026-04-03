import numpy as np
import tabulate as tb

#ángulos en grados, el 0 es 324º

red_100 = np.array([[0,  "blanco"],#324
					[2.5,  "azul"],#326.5
					[3,  "verde"],#327
					[3.5,"amarillo"],#327.5
					[4,  "rojo"],#328 #332
					[8,  "violeta"]])#332

red_300 = np.array([[0, "blanco"], #324
					[7.5, "azul oscuro"],#331.5
					[8 ,  "azul claro"], #332
					[9, "verde"],#333
					[10, "amarillo"],#334
					[11.5, "rojo"]])

red_600 = np.array([[0, "blanco"],#324
					[16, "azul oscuro"],#340
					[17, "azul claro"],#341
		 			[17.5, "cyan"],#341.5
					[18, "verde"],#342
					[21, "amarillo"], #345
					[24, "rojo"]]) #348

angulos_100 = np.transpose(red_100)[0]
angulos_300 = np.transpose(red_300)[0]
angulos_600 = np.transpose(red_600)[0]

colores_100 = np.transpose(red_100)[1]
colores_300 = np.transpose(red_300)[1]
colores_600 = np.transpose(red_600)[1]

error_angulos = [r"\pm 0.01"] * 6
parametro_red_100 = 101.09

parametro_red_300 = 309.07

parametro_red_600 = 627.97

error_medio_100 = 0.11

error_medio_300 = 0.34

error_medio_600 = 1.4

lambda_100 = []
lambda_300 = []
lambda_600 = []

error_lambda_100 = []
error_lambda_300 = []
error_lambda_600 = []

for i in red_100:
	lambdai = float((np.sin(float(i[0])*2*np.pi /360) / parametro_red_100) * 1e+6)
	lambda_100.append(lambdai)

	error_lambda_100.append(r"\pm " + str(round(((1/parametro_red_100) * 0.01 + (float(i[0])*2*np.pi /360)/parametro_red_100**2 * error_medio_100), 5)))

for i in red_300:
	lambdai = float((np.sin(float(i[0])*2*np.pi /360) / parametro_red_300) * 1e+6)
	lambda_300.append(lambdai)

	error_lambda_300.append(r"\pm " + str(round(((1/parametro_red_300) * 0.01 + (float(i[0])*2*np.pi /360)/parametro_red_300**2 * error_medio_300), 5)))

for i in red_600:
	lambdai = float((np.sin(float(i[0])*2*np.pi /360) / parametro_red_600) * 1e+6)
	lambda_600.append(lambdai)

	error_lambda_600.append(r"\pm " + str(round(((1/parametro_red_600) * 0.01 + (float(i[0])*2*np.pi /360)/parametro_red_600**2 * error_medio_600), 5)))
"""
print(lambda_100)
print(lambda_300)
print(lambda_600)
"""


titulos_tablas = [r"$\theta$ (grados)", r"$\lambda$ (nm)", r"$\Delta$ $\theta$ (grados)", r"$\Delta$ $\lambda$ (nm)"]

datos_100 = [list(i) for i in zip(angulos_100, lambda_100, error_angulos, error_lambda_100)]
datos_300 = [list(i) for i in zip(angulos_300, lambda_300, error_angulos, error_lambda_300)]
datos_600 = [list(i) for i in zip(angulos_600, lambda_600, error_angulos, error_lambda_600)]


tabla_100 = tb.tabulate(datos_100, headers=titulos_tablas, tablefmt="latex_raw")
tabla_300 = tb.tabulate(datos_300, headers=titulos_tablas, tablefmt="latex_raw")
tabla_600 = tb.tabulate(datos_600, headers=titulos_tablas, tablefmt="latex_raw")

print(r"\begin{table}[H]")
print(r"\centering")
print(tabla_600)
print(r"\caption{Resultados para la red de 300 líneas por milímetro.}")
print(r"\end{table}")
print("\n")

