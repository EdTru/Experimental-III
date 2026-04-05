import numpy as np
import tabulate
import scipy.constants as cons

h = cons.h
c = cons.c
e = cons.eV
g = np.float64(1.6336317230290944e-06) #Constante red apartado anterior

error_angulo = 0.05
error_angulo_rad = 0.0009
error_g = np.float64(6.254791388988623e-09) #Error medio apartado anterior


#ángulos en grados, el 0 es 325º, error = 0.1

i = 323.5 #Cero
red_600_1 = np.array([[0, "blanco"],
					[338.6-i, "azul oscuro"],
					[339.4-i, "azul claro"],
		 			[340.4-i, "cyan"],
					[340.8-i, "verde"],
					[344-i, "amarillo"],
					[347-i, "rojo"]])


red_600_2 = np.array([[0, "blanco"],#324
					[16, "azul oscuro"],#340
					[17, "azul claro"],#341
		 			[17.5, "cyan"],#341.5
					[18, "verde"],#342
					[21, "amarillo"], #345
					[24, "rojo"]]) #348

i = 323 #Cero
red_600_3 = np.array([[0, "blanco"],
					[339.8-i, "azul oscuro"],#338.4 339.8
					[340.6-i, "azul claro"],
		 			[341.5-i, "cyan"],
					[341.7-i, "verde"],
					[344.2-i, "amarillo"],
					[347.3-i, "rojo"]])

i = 323.9 #Cero
red_600_4 = np.array([[0, "blanco"],
					[338.5-i, "azul oscuro"],#338.4 339.8
					[339.6-i, "azul claro"],
		 			[340.3-i, "cyan"],
					[340.5-i, "verde"],
					[343.8-i, "amarillo"],
					[346.7-i, "rojo"]])



pies = []


for i in range(0,7):
	#TOMA 1
	angulo = red_600_1[i][0]
	angulo_rad = np.float64(angulo)*2*np.pi/360
	lambd = g*np.sin(np.float64(angulo_rad))
	E_h = h*c/e * 1/lambd

	error_lambd = error_g*np.abs(np.sin(angulo_rad))+np.abs(g*np.cos(angulo_rad))*error_angulo_rad
	error_E = h*c/e * error_lambd/(lambd**2)

	pies.append([1, red_600_1[i][1], angulo, angulo_rad, lambd, E_h, error_angulo, error_angulo_rad, error_lambd, error_E])
	#Toma 2
	angulo = red_600_2[i][0]
	angulo_rad = np.float64(angulo)*2*np.pi/360
	lambd = g*np.sin(np.float64(angulo_rad))
	E_h = h*c/e * 1/lambd

	error_lambd = error_g*np.abs(np.sin(angulo_rad))+np.abs(g*np.cos(angulo_rad))*error_angulo_rad
	error_E = h*c/e * error_lambd/(lambd**2)

	pies.append([2, red_600_2[i][1], angulo, angulo_rad, lambd, E_h, error_angulo, error_angulo_rad, error_lambd, error_E])

	#TOMA 3
	angulo = red_600_3[i][0]
	angulo_rad = np.float64(angulo)*2*np.pi/360
	lambd = g*np.sin(np.float64(angulo_rad))
	E_h = h*c/e * 1/lambd

	error_lambd = error_g*np.abs(np.sin(angulo_rad))+np.abs(g*np.cos(angulo_rad))*error_angulo_rad
	error_E = h*c/e * error_lambd/(lambd**2)

	pies.append([3, red_600_1[i][1], angulo, angulo_rad, lambd, E_h, error_angulo, error_angulo_rad, error_lambd, error_E])

	#Toma 4
	angulo = red_600_4[i][0]
	angulo_rad = np.float64(angulo)*2*np.pi/360
	lambd = g*np.sin(np.float64(angulo_rad))
	E_h = h*c/e * 1/lambd

	error_lambd = error_g*np.abs(np.sin(angulo_rad))+np.abs(g*np.cos(angulo_rad))*error_angulo_rad
	error_E = h*c/e * error_lambd/(lambd**2)

	pies.append([4, red_600_1[i][1], angulo, angulo_rad, lambd, E_h, error_angulo, error_angulo_rad, error_lambd, error_E])

cabezas = ["nº medida","Color", "angulo (º)","angulo (rad)","lambda (m)","E (ev)","error angulo (º)", "error angulo (rad)", "error lambda","error E"]

print(tabulate.tabulate(pies, cabezas, tablefmt="latex"))

"""
tabla_niveles=[]
for n in range(1,8):
	for m in range(1,n):
		E_at = -13.6*4*(1/(n**2)-1/(m**2))
		tabla_niveles.append([(m,n),E_at])

print(tabulate.tabulate(tabla_niveles))
"""