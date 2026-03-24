import numpy as np
import tabulate
import scipy.constants as cons

h = cons.h
print(h)
c = cons.c
e = cons.eV

#ángulos en grados, el 0 es 325º, error = 0.1

i = 323.5
g = np.float64(1.6197290939428308e-06)
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
i = 323
red_600_3 = np.array([[0, "blanco"],
					[339.8-i, "azul oscuro"],#338.4 339.8
					[340.6-i, "azul claro"],
		 			[341.5-i, "cyan"],
					[341.7-i, "verde"],
					[344.2-i, "amarillo"],
					[347.3-i, "rojo"]])

#usamos otra red de difracción de 600 / mm

i = 323.9
red_600_4 = np.array([[0, "blanco"],
					[338.5-i, "azul oscuro"],#338.4 339.8
					[339.6-i, "azul claro"],
		 			[340.3-i, "cyan"],
					[340.5-i, "verde"],
					[343.8-i, "amarillo"],
					[346.7-i, "rojo"]])



tabla_lambas = []
for ang,color in zip(np.transpose(red_600_4)[0], np.transpose(red_600_4)[1]):
	ang= np.float64(ang)*2*np.pi/360
	lambd = g*np.sin(np.float64(ang))
	E_h = h*c/e * 1/lambd
	tabla_lambas.append([color,ang,lambd,E_h])

print(tabulate.tabulate(tabla_lambas))

tabla_niveles=[]
for n in range(1,8):
	for m in range(1,n):
		E_at = -13.6*4*(1/(n**2)-1/(m**2))
		tabla_niveles.append([(m,n),E_at])

print(tabulate.tabulate(tabla_niveles))
